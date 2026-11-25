#!/usr/bin/env python3
"""Adoption step: always emit verdict.json + update wall validation slice (P0-1).

52B fixes carried here:
- conflicts gating: a non-empty escalated conflicts array annotates the verdict
  (conflicts_escalated) — the round-52 A shape (chaocipher vector contradiction
  escalated, yet a bare pass) can never be emitted again;
- kill recovery: when the validator session was wall-killed, per-process
  conclusions persisted incrementally (salvage_verdict.py) are recovered into
  verdict.json instead of dying with the reasoning that produced them.

Round-53 accounting fix: judgeable==[] means the workflow skipped the droid
session on purpose (the judging `if` gates it off, so no droid-exit.txt is
ever written); budgets.session_outcome then records
completion_status=skipped_no_judgeable with a null exit_code instead of the
missing_output / exit -1 pseudo-artifact that presented an unstarted session
as a failed one.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

from budget_resolve import adopt_session_completion_status
from foreman_run_lib import deep_merge, load_wall, save_wall
from salvage_assemble import assemble_assembled_draft
from salvage_verdict import read_salvage

ADOPTION_ERRORS = {
    "missing_draft",
    "draft_timeout",
    "coverage_mismatch",
    "evidence_tampered",
    "droid_step_failed",
    "merge_skipped",
}


def detect_droid_failure(work_dir: Path) -> str | None:
    stream = work_dir / "validator-stream.jsonl"
    if not stream.exists():
        return None
    for line in stream.read_text(encoding="utf-8", errors="replace").splitlines():
        if "error" in line.lower() or '"type":"error"' in line:
            return "droid_step_failed"
    return None


def compute_flips(
    verdicts: dict[str, dict], round1_path: Path | None
) -> list[dict]:
    if not round1_path or not round1_path.exists():
        return []
    try:
        r1 = {p["id"]: p for p in json.loads(round1_path.read_text()).get("processes", [])}
    except Exception:
        return []
    flips = []
    for pid, v in verdicts.items():
        prev = r1.get(pid)
        if prev and prev.get("verdict") == "pass" and v["verdict"] != "pass":
            flips.append(
                {
                    "id": pid,
                    "round1_verdict": prev["verdict"],
                    "round1_reason": prev.get("reason", ""),
                    "round2_verdict": v["verdict"],
                    "round2_reason": v.get("reason", ""),
                }
            )
    return flips


def conflicts_escalated(conflicts: list[dict] | None) -> bool:
    """True when the validator escalated at least one work-order conflict."""
    return bool(conflicts)


def _recover_salvage(
    work_dir: Path,
    plan: dict,
    blocked: dict,
    adoption_error: str,
    round_num: int,
) -> None:
    """52B fix: always emit a verdict.json when the session died before its draft.

    When the validator session was killed (timeout / merge skipped / missing
    draft), the incremental verdict file written after each finished analysis
    is folded into verdict.json: recovered processes keep their verdict,
    everything never analyzed becomes "blocked" with the factual reason. The
    verdict stays fail-closed — overall=fail, pytest_exit stays None (no
    merged-suite evidence), the wall artifact stays incomplete — so replan
    still fires; only the completed per-process analysis survives instead of
    being lost with the reasoning that produced it.
    """
    salvage = read_salvage(work_dir, round_num=round_num)
    verdicts: dict[str, dict] = {}
    if salvage:
        for entry in salvage["processes"]:
            verdicts[entry["id"]] = {
                "id": entry["id"],
                "verdict": entry["verdict"],
                "reason": entry.get("reason", ""),
                "salvaged": True,
            }
    for pid, missing in (blocked or {}).items():
        verdicts[pid] = {
            "id": pid,
            "verdict": "blocked",
            "reason": "料不齐：缺 " + ", ".join(missing),
        }
    try:
        plan_ids = [p["id"] for p in (plan or {}).get("processes", [])]
    except Exception:
        plan_ids = []
    for pid in plan_ids:
        verdicts.setdefault(
            pid,
            {
                "id": pid,
                "verdict": "blocked",
                "reason": "validator 会话被墙杀，该工序未完成分析（非料不齐）",
            },
        )
    ordered = [verdicts[pid] for pid in plan_ids if pid in verdicts]
    conflicts = salvage["conflicts"] if salvage else []
    verdict = {
        "overall": "fail",
        "pytest_exit": None,
        "iteration": round_num,
        "processes": ordered,
        "conflicts": conflicts,
        "conflicts_escalated": conflicts_escalated(conflicts),
        "failing_tests": [],
        "unattributed_failure": False,
        "adoption_status": "failed",
        "adoption_error": adoption_error,
        "verdict_schema_version": "foreman-run.v1",
    }
    if salvage:
        verdict["salvaged_from"] = "verdict-partial.json"
        verdict["salvaged_count"] = salvage["analyzed_count"]
    Path("verdict.json").write_text(
        json.dumps(verdict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    md_lines = [
        "## 采认",
        f"- adoption_status: **failed**（{adoption_error}）",
    ]
    if salvage:
        md_lines.append(
            f"- 会话被杀前已完成分析并落盘的结论：{salvage['analyzed_count']} 件（从 verdict-partial.json 回收）"
        )
        md_lines.append("")
        for p in ordered:
            md_lines.append(f"- `{p['id']}`：{p['verdict']} — {p['reason'][:200]}")
    if conflicts:
        md_lines += ["", "## 工单层冲突（验收员升级记录）", ""]
        for c in conflicts:
            md_lines.append(
                f"- `{c['process']}`：{c.get('summary', '')}（证据：{c.get('evidence', '')}）"
            )
    md_lines.append("\n总判定：**fail**（采认失败；已回收结论仅供参考，不构成 pass）")
    Path("verdict.md").write_text("\n".join(md_lines), encoding="utf-8")


def adopt(
    work_dir: Path,
    wall_path: Path,
    *,
    droid_exit: int | None,
    merge_step_ran: bool,
    round_num: int = 1,
    round1_verdict: Path | None = None,
) -> int:
    wall = load_wall(wall_path)
    issue = wall["issue_number"]
    run_id = wall["run_id"]
    art_key = (
        f"team-verdict2-issue-{issue}-run-{run_id}"
        if round_num == 2
        else f"team-verdict-issue-{issue}-run-{run_id}"
    )

    adoption_status = "ok"
    adoption_error = None
    overall = "fail"
    failed: list[str] = []
    unattributed = False
    pytest_exit = None
    conflicts: list[dict] = []
    # Assigned before the try so the accounting tail below can never hit an
    # unbound name when this step died before reading the precheck outputs.
    judgeable: list = []
    # Set when adoption proceeded on a machine-assembled draft (I-6): the
    # verdict is then annotated with salvage_assembled for auditability.
    assembled_draft = False

    manifest_path = work_dir / "manifest.json"
    plan_path = work_dir / "plan.json"
    judgeable_path = work_dir / "judgeable.json"
    blocked_path = work_dir / "blocked.json"
    draft_path = work_dir / "verdict-droid.json"

    try:
        if not manifest_path.exists() or not plan_path.exists():
            raise ValueError("missing manifest or plan")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        judgeable = json.loads(judgeable_path.read_text()) if judgeable_path.exists() else []
        blocked = json.loads(blocked_path.read_text()) if blocked_path.exists() else {}

        expected_sha = os.environ.get("EXPECTED_MANIFEST_SHA", "")
        actual_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        proceed_to_judge = False
        if expected_sha and actual_sha != expected_sha:
            adoption_status = "failed"
            adoption_error = "evidence_tampered"
        elif droid_exit == 124:
            # I-6 / L-6 (U-3): artifact completeness outranks the exit code —
            # the wall often kills the session during its censored tail after
            # the draft was already written, or after every conclusion was
            # recorded. A complete draft adopts normally; a sealed partial
            # covering the full judgeable set is machine-assembled into the
            # draft and adopts normally; anything less is the revalidate path.
            if draft_path.exists():
                proceed_to_judge = True
            elif judgeable:
                assembled = assemble_assembled_draft(work_dir, judgeable)
                if assembled is not None:
                    draft_path.write_text(
                        json.dumps(assembled, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                    assembled_draft = True
                    proceed_to_judge = True
                else:
                    adoption_status = "failed"
                    adoption_error = "draft_timeout"
                    _recover_salvage(work_dir, plan, blocked, adoption_error, round_num)
            else:
                adoption_status = "failed"
                adoption_error = "draft_timeout"
                _recover_salvage(work_dir, plan, blocked, adoption_error, round_num)
        elif not merge_step_ran and not draft_path.exists():
            adoption_status = "failed"
            adoption_error = "merge_skipped"
            _recover_salvage(work_dir, plan, blocked, adoption_error, round_num)
        elif judgeable and not draft_path.exists():
            adoption_status = "failed"
            adoption_error = "missing_draft"
            _recover_salvage(work_dir, plan, blocked, adoption_error, round_num)
        else:
            proceed_to_judge = True
        if proceed_to_judge:
            verdicts: dict[str, dict] = {}
            droid = {}
            if judgeable:
                if not draft_path.exists():
                    adoption_status = "failed"
                    adoption_error = "missing_draft"
                else:
                    droid = json.loads(draft_path.read_text(encoding="utf-8"))
                    entries = droid.get("processes", [])
                    if sorted(p.get("id") for p in entries) != sorted(judgeable):
                        adoption_status = "failed"
                        adoption_error = "coverage_mismatch"
                    else:
                        for entry in entries:
                            if entry.get("verdict") not in ("pass", "fail"):
                                adoption_status = "failed"
                                adoption_error = "coverage_mismatch"
                                break
                            verdicts[entry["id"]] = {
                                "id": entry["id"],
                                "verdict": entry["verdict"],
                                "reason": entry.get("reason", ""),
                            }
                        conflicts = [
                            c
                            for c in (droid.get("conflicts") or [])
                            if isinstance(c, dict) and c.get("process")
                        ]
            for pid, missing in blocked.items():
                verdicts[pid] = {
                    "id": pid,
                    "verdict": "blocked",
                    "reason": "料不齐：缺 " + ", ".join(missing),
                }
            if adoption_status == "ok":
                expected_ids = sorted(p["id"] for p in plan["processes"])
                if sorted(verdicts) != expected_ids:
                    adoption_status = "failed"
                    adoption_error = "coverage_mismatch"
                else:
                    pytest_exit = manifest.get("pytest_exit", 1)
                    escalated = conflicts_escalated(conflicts)
                    overall = (
                        "pass"
                        if all(v["verdict"] == "pass" for v in verdicts.values())
                        and pytest_exit == 0
                        and not escalated
                        else "fail"
                    )
                    failed = [pid for pid, v in verdicts.items() if v["verdict"] != "pass"]
                    failing_tests: list[str] = []
                    if overall == "fail" and not failed and not escalated:
                        raw = (work_dir / "pytest-output.txt").read_text(
                            encoding="utf-8", errors="replace"
                        ) if (work_dir / "pytest-output.txt").exists() else ""
                        seen: set[str] = set()
                        for tline in raw.splitlines():
                            tid = None
                            if tline.startswith("FAILED "):
                                tid = tline[len("FAILED ") :].split(" - ")[0].strip()
                            else:
                                m = re.match(r"^_{3,}\s+(\S+)\s+_{3,}$", tline.strip())
                                if m:
                                    tid = m.group(1)
                            if tid and tid not in seen:
                                seen.add(tid)
                                failing_tests.append(tid)
                        unattributed = True
                    else:
                        failing_tests = []
                    flips = compute_flips(verdicts, round1_verdict) if round_num == 2 else []
                    iteration = manifest.get("iteration", round_num)
                    verdict = {
                        "overall": overall,
                        "pytest_exit": pytest_exit,
                        "iteration": iteration,
                        "processes": [verdicts[p["id"]] for p in plan["processes"]],
                        "conflicts": conflicts,
                        # 52A fix: escalated conflicts annotate the verdict — a
                        # bare pass can no longer hide a work-order contradiction.
                        "conflicts_escalated": escalated,
                        "failing_tests": failing_tests[:50],
                        "unattributed_failure": unattributed,
                        "adoption_status": adoption_status,
                        "adoption_error": adoption_error,
                        "verdict_schema_version": "foreman-run.v1",
                    }
                    if flips:
                        verdict["flips"] = flips
                    if assembled_draft:
                        verdict["salvage_assembled"] = True
                    Path("verdict.json").write_text(
                        json.dumps(verdict, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                    md_lines = ["## 采认", f"- adoption_status: **{adoption_status}**", ""]
                    if assembled_draft:
                        md_lines.append(
                            "- 草稿由机器组装（verdict-partial.json 全盖 judgeable＋收口标记），"
                            "会话退出码不参与判定；机器闸照常适用"
                        )
                        md_lines.append("")
                    if (work_dir / "verdict-droid.md").exists():
                        md_lines.append((work_dir / "verdict-droid.md").read_text(encoding="utf-8"))
                    if escalated:
                        md_lines += ["", "## 工单层冲突（验收员升级记录）", ""]
                        for c in conflicts:
                            md_lines.append(
                                f"- `{c['process']}`：{c.get('summary', '')}（证据：{c.get('evidence', '')}）"
                            )
                    md_lines.append(f"\n总判定：**{overall}**")
                    Path("verdict.md").write_text("\n".join(md_lines), encoding="utf-8")
    except Exception as exc:
        adoption_status = "failed"
        adoption_error = adoption_error or "droid_step_failed"
        err = detect_droid_failure(work_dir)
        if err:
            adoption_error = err
        if not Path("verdict.json").exists():
            try:
                plan = json.loads(plan_path.read_text(encoding="utf-8"))
                blocked = json.loads(blocked_path.read_text()) if blocked_path.exists() else {}
                _recover_salvage(work_dir, plan, blocked, adoption_error, round_num)
            except Exception:
                pass
        if not Path("verdict.json").exists():
            verdict = {
                "overall": "fail",
                "pytest_exit": None,
                "iteration": 1,
                "processes": [],
                "adoption_status": adoption_status,
                "adoption_error": adoption_error or "droid_step_failed",
                "adoption_detail": str(exc)[:500],
                "verdict_schema_version": "foreman-run.v1",
            }
            Path("verdict.json").write_text(
                json.dumps(verdict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        Path("verdict.md").write_text(
            f"## 采认失败\n\n`{adoption_error}`\n", encoding="utf-8"
        )

    complete = adoption_status == "ok" and Path("verdict.json").exists()
    missing = [] if complete else ["verdict.json", "verdict.md"]
    patch = {
        "validation": {
            "schema_version": "validation-slice.v1",
            "round": round_num,
            "draft_path": "work/verdict-droid.json",
            "verdict_path": "verdict.json",
            "adoption_status": adoption_status,
            "adoption_error": adoption_error,
            "overall": overall,
            "failed_process_ids": failed,
            "unattributed_failure": unattributed,
            "conflicts_escalated": conflicts_escalated(conflicts),
            "pytest_exit": pytest_exit,
        },
        "artifacts": {
            art_key: {
                "complete": complete,
                "missing": missing,
                "required_members": ["verdict.json", "verdict.md"],
                "forbidden_partial": ["work/validator-stream.jsonl"],
            }
        },
    }
    # I-5 revalidate chain: a first draft_timeout (wall-killed validator, no
    # complete verdict artifact) is retried once by the revalidate job instead
    # of killing the order — the evidence pack is intact and the manifest sha
    # unchanged, so only the validator session needs a second chance. Any
    # other adoption failure, or a draft_timeout AFTER that one retry
    # (revalidate_attempted already true), stays terminal fail-closed.
    revalidate_requested = (
        adoption_status == "failed"
        and adoption_error == "draft_timeout"
        and not ((wall.get("replan_gate") or {}).get("revalidate_attempted"))
    )
    # W-12 session accounting: a timeout is a timeout even when the artifacts
    # on disk were good enough to adopt (I-6) — the budget ledger keeps the
    # real session outcome; only the adoption verdict follows the artifacts.
    session_status = adopt_session_completion_status(droid_exit)
    role = "validator" if round_num == 1 else "validator2"
    if adoption_status == "failed":
        gate_patch = {
            "schema_version": "replan-gate.v1",
            "should_replan": bool(
                (wall.get("replan_gate") or {}).get("should_replan")
            ),
            "should_revalidate": bool(revalidate_requested),
        }
        if revalidate_requested:
            gate_patch["revalidate_attempted"] = True
            # The revalidate request is NOT terminal: no human_stop, no
            # closeout — the retry job consumes the flag.
        else:
            patch["human_stop"] = True
            patch["closeout"] = {
                "schema_version": "closeout-slice.v1",
                "run_must_fail": True,
            }
        patch["replan_gate"] = gate_patch
    else:
        gate_patch = {
            "schema_version": "replan-gate.v1",
            "should_replan": bool(
                (wall.get("replan_gate") or {}).get("should_replan")
            ),
            "should_revalidate": False,
        }
        patch["replan_gate"] = gate_patch
    if judgeable == [] and droid_exit is None and adoption_status == "ok":
        # Round-53 C artifact: with zero judgeable processes the workflow's
        # judging `if` skips the droid session entirely (no droid-exit.txt,
        # no stream), so a bare None here means "never started on purpose",
        # not a missing session output. Record the skip instead of dressing
        # it up as a failed session; the blocked verdict above already keeps
        # the round red downstream.
        session_status = "skipped_no_judgeable"
        patch["budgets"] = {
            "session_outcome": {
                "role": role,
                "completion_status": session_status,
                "exit_code": None,
            }
        }
    else:
        patch["budgets"] = {
            "session_outcome": {
                "role": role,
                "completion_status": session_status,
                "exit_code": droid_exit if droid_exit is not None else -1,
            }
        }
    if round_num == 2:
        patch["round2"] = {
            "validation": patch["validation"],
            "artifacts_verdict2": art_key,
        }
    merged = deep_merge(wall, patch)
    save_wall(merged, wall_path)
    print("adoption:", adoption_status, adoption_error or "")
    # The wall is the truth surface: the step's exit code carries no verdict
    # (job red/green comes from the wall-driven conclusion steps), exactly
    # like the pre-I-6 contract — terminal failures land human_stop on the
    # wall, revalidate requests land the gate flag.
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--work-dir", default="work")
    p.add_argument("--droid-exit", type=int, default=-1)
    p.add_argument("--merge-step-ran", action="store_true")
    p.add_argument("--round", type=int, default=1)
    p.add_argument("--round1-verdict", default="")
    args = p.parse_args()
    r1 = Path(args.round1_verdict) if args.round1_verdict else None
    return adopt(
        Path(args.work_dir),
        Path(args.wall),
        droid_exit=args.droid_exit if args.droid_exit >= 0 else None,
        merge_step_ran=args.merge_step_ran,
        round_num=args.round,
        round1_verdict=r1,
    )


if __name__ == "__main__":
    raise SystemExit(main())