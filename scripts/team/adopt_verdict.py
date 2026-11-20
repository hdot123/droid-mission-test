#!/usr/bin/env python3
"""Adoption step: always emit verdict.json + update wall validation slice (P0-1)."""
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
        if expected_sha and actual_sha != expected_sha:
            adoption_status = "failed"
            adoption_error = "evidence_tampered"
        elif droid_exit == 124:
            adoption_status = "failed"
            adoption_error = "draft_timeout"
        elif not merge_step_ran and not draft_path.exists():
            adoption_status = "failed"
            adoption_error = "merge_skipped"
        elif judgeable and not draft_path.exists():
            adoption_status = "failed"
            adoption_error = "missing_draft"
        else:
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
                    overall = (
                        "pass"
                        if all(v["verdict"] == "pass" for v in verdicts.values())
                        and pytest_exit == 0
                        else "fail"
                    )
                    failed = [pid for pid, v in verdicts.items() if v["verdict"] != "pass"]
                    failing_tests: list[str] = []
                    if overall == "fail" and not failed:
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
                        "failing_tests": failing_tests[:50],
                        "unattributed_failure": unattributed,
                        "adoption_status": adoption_status,
                        "adoption_error": adoption_error,
                        "verdict_schema_version": "foreman-run.v1",
                    }
                    if flips:
                        verdict["flips"] = flips
                    Path("verdict.json").write_text(
                        json.dumps(verdict, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                    md_lines = ["## 采认", f"- adoption_status: **{adoption_status}**", ""]
                    if (work_dir / "verdict-droid.md").exists():
                        md_lines.append((work_dir / "verdict-droid.md").read_text(encoding="utf-8"))
                    md_lines.append(f"\n总判定：**{overall}**")
                    Path("verdict.md").write_text("\n".join(md_lines), encoding="utf-8")
    except Exception as exc:
        adoption_status = "failed"
        adoption_error = adoption_error or "droid_step_failed"
        err = detect_droid_failure(work_dir)
        if err:
            adoption_error = err
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
    if adoption_status == "failed":
        patch["human_stop"] = True
        patch["closeout"] = {
            "schema_version": "closeout-slice.v1",
            "run_must_fail": True,
        }
    session_status = adopt_session_completion_status(droid_exit)
    role = "validator" if round_num == 1 else "validator2"
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
    return 0 if complete or adoption_status == "failed" else 1


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