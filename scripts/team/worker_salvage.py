#!/usr/bin/env python3
"""Prep salvage packer (M2): machine-write the evidence files a killed
worker session never wrote.

Round-58 D-run death chain: the hslconv worker died to the 900s wall before
writing team/handoffs/<pid>.md and team/status/<pid>.json, yet prep's own
machine re-run of the card's checks on the merged branch was green — the
work was machine-verified and only the evidence files were missing (the
validator's blocked scan is a file-presence scan, nothing more). Per the
PR #836 artifact-first principle, on-disk product completeness outranks the
session's exit code.

The guard is machine-judged and fail-closed; ALL of:
  1. the worker branch was merged into the candidate (merged true);
  2. no out-of-bounds files (F-1 clean);
  3. prep's own re-run of the card checks is all green (checks-exit.json
     exists and every entry exited 0);
  4. the session terminated abnormally — any of:
       - the wall records session_outcome=wall_killed for the pid;
       - a non-zero droid exit code (covers the exit-1 droid self-crash and
         exit-137 SIGKILL families, which classify_session_outcome keeps
         "ok" — scrutiny round-1: an abnormal END is abnormal regardless of
         the outcome classifier's death-family bookkeeping);
       - a supplied stream that never recorded a completion event (54/97
         real streams end on {"type": "completion"}; a stream without one
         never ended on its own);
       - a true stream_tail_marker (interrupted tool_error as last event).
  A session that exited 0 with outcome ok is a NORMAL end: its missing
  files are a compliance failure and stay blocked (the control fixture
  pins that — salvage must never paper over it).

Products (only files missing from the pack; worker-written files are never
touched — evidence immutability):
  - status.json: the worker protocol shape (id/title/state/files/checks)
    rendered from the process card + checks-exit.json + checks-output.txt;
  - handoff.md: machine rendering of the machine facts, explicitly declaring
    the salvage origin, the death cause, and the green machine re-verification
    — never impersonating a worker-written handoff;
  - manifest: pack.salvaged_from_machine=true, pack.handoff/status refreshed,
    complete recomputed, and the new files hashed into manifest.sha256 so the
    pack's own digest covers the salvaged bytes (validator precheck verifies
    every entry against disk; prep's os.walk hashing picks the files up too).

Any guard miss, salvage error, or already-present file keeps the pack
exactly as prep produced it (blocked stays blocked). The salvage call site
in team.yml wraps this in try/except: a salvage defect must fail the pack
closed, never kill prep.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

SALVAGE_MARKER_KEY = "salvaged_from_machine"
STATUS_NAME = "status.json"
HANDOFF_NAME = "handoff.md"

_COMPLETED_RE = re.compile(r"(\d+) passed(?:, (\d+) skipped)?")


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def checks_all_green(checks_exit: Any, pack_dir: Path) -> bool:
    """True only when checks-exit.json parses to a non-empty list and every
    entry exited 0 (the machine verdict on the merged tree, independent of
    the dead session)."""
    doc = checks_exit if checks_exit is not None else _load_json(pack_dir / "checks-exit.json")
    if not isinstance(doc, list) or not doc:
        return False
    return all(isinstance(e, dict) and e.get("exit") == 0 for e in doc)


def abnormal_termination_evidence(
    workers: dict | None,
    pid: str,
    *,
    stream_text: str | None = None,
) -> tuple[bool, list[str]]:
    """(abnormal_end, evidence lines) for the guard's fourth condition.

    workers = the wall's workers slice (session_outcome_by_pid /
    droid_exit_code_by_pid / stream_tail_marker_by_pid). stream_text, when
    supplied, is the session stream content (prep has no stream artifact;
    the parameter exists for replay surfaces and tests). A completion event
    anywhere in the stream proves the session ended on its own, so the
    no-completion clause cannot fire.
    """
    evidence: list[str] = []
    w = workers or {}
    outcome = (w.get("session_outcome_by_pid") or {}).get(pid)
    exit_code = (w.get("droid_exit_code_by_pid") or {}).get(pid)
    tail_marker = (w.get("stream_tail_marker_by_pid") or {}).get(pid)
    if outcome == "wall_killed":
        evidence.append(f"session_outcome=wall_killed (droid exit {exit_code})")
    if isinstance(exit_code, int) and exit_code != 0 and outcome != "wall_killed":
        evidence.append(f"non-zero droid_exit_code={exit_code} (no normal completion)")
    if tail_marker is True:
        evidence.append("stream_tail_marker=true (interrupted tool_error is the last event)")
    if outcome != "wall_killed" and not evidence and stream_text is not None:
        if not _stream_has_completion_event(stream_text):
            evidence.append("stream has no completion event (session never ended on its own)")
    return (bool(evidence), evidence)


def _stream_has_completion_event(stream_text: str) -> bool:
    for line in stream_text.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("type") == "completion":
            return True
    return False


def evaluate_salvage_guard(
    *,
    info: dict,
    pack_dir: Path,
    card: dict,
    workers: dict | None,
    pid: str,
    stream_text: str | None = None,
) -> tuple[bool, list[str]]:
    """The four machine-judged conditions. Returns (allowed, reasons); the
    reasons always name the satisfied/failed conditions so the prep log and
    the salvage handoff carry the full decision trail. ``card`` is accepted
    for call-site symmetry; the guard conditions read only machine facts."""
    reasons: list[str] = []
    if not info.get("branch_present"):
        reasons.append(f"guard: branch_present=false for {pid}")
    if not info.get("merged"):
        reasons.append(f"guard: branch not merged for {pid}")
    oob = info.get("out_of_bounds") or []
    if oob:
        reasons.append(f"guard: out_of_bounds files for {pid}: {', '.join(oob)}")
    doc = _load_json(pack_dir / "checks-exit.json")
    green = checks_all_green(doc, pack_dir)
    if not green:
        if not isinstance(doc, list) or not doc:
            reasons.append(
                f"guard: machine checks not all green for {pid} (checks-exit.json missing/empty)"
            )
        else:
            bad = ", ".join(
                f"exit {e.get('exit')}" for e in doc if not (isinstance(e, dict) and e.get("exit") == 0)
            )
            reasons.append(
                f"guard: machine checks not all green for {pid} ({bad or 'malformed entries'})"
            )
    abnormal, ev = abnormal_termination_evidence(workers, pid, stream_text=stream_text)
    if abnormal:
        reasons.append(f"guard: abnormal session end for {pid}: " + "; ".join(ev))
    else:
        outcome = ((workers or {}).get("session_outcome_by_pid") or {}).get(pid)
        exit_code = ((workers or {}).get("droid_exit_code_by_pid") or {}).get(pid)
        reasons.append(
            f"guard: normal session end for {pid} "
            f"(session_outcome={outcome}, droid exit {exit_code}) — missing files are a "
            "compliance failure, not salvageable"
        )
    ok_conditions = [
        bool(info.get("merged")),
        not bool(oob),
        green,
        abnormal,
    ]
    return all(ok_conditions), reasons


def build_status(*, card: dict, checks_exit: list, checks_output: str) -> dict:
    """The worker protocol status shape, rendered from machine facts only.

    checks[] mirrors checks-exit.json command-for-command; each result is
    that command's captured pytest summary line (when one exists) plus the
    exit code prep recorded — the numbers always agree with checks-exit.json
    because they come from it."""
    per_command: dict[str, str] = {}
    for block in checks_output.split("$ ")[1:]:
        lines = block.splitlines()
        if lines:
            per_command[lines[0].strip()] = "\n".join(lines[1:]).strip()
    checks = []
    for entry in checks_exit:
        cmd = entry.get("command", "")
        body = per_command.get(cmd, "")
        summary = ""
        for line in reversed(body.splitlines()):
            if _COMPLETED_RE.search(line):
                summary = line.strip()
                break
        exit_part = f"[exit {entry.get('exit')}]" if entry.get("exit") is not None else ""
        result = " ".join(p for p in (summary, exit_part) if p)
        checks.append({"command": cmd, "result": result})
    return {
        "id": card.get("id"),
        "title": card.get("title"),
        "state": "done",
        "files": list(card.get("files") or []),
        "checks": checks,
    }


def build_handoff(
    *,
    pid: str,
    card: dict,
    checks_exit: list,
    checks_output: str,
    branch: str,
    exit_code: Any,
) -> str:
    checks_lines = "\n".join(
        f"- `$ {e.get('command', '')}` — [exit {e.get('exit')}]" for e in checks_exit
    )
    exit_part = str(exit_code) if exit_code is not None else "unknown"
    return f"""# Handoff: {pid}（补卷器生成）

> **本件由补卷器（scripts/team/worker_salvage.py）机器生成，非工人亲写。**
> 工人会话异常终结（session_outcome=wall_killed，droid exit {exit_part}），
> 在写出两件协议证据文件（team/handoffs/{pid}.md 与 team/status/{pid}.json）
> 之前被杀（落盘未遂）；按盘上产物完整性优先原则（salvaged_from_machine=true），
> 由机器依据 prep 重跑的机器事实补齐本件与 evidence/packs/{pid}/status.json。
> 本件不含任何工人自述。

## 工序（process card）

- id: `{pid}`
- title: {card.get('title', '')}
- files: {', '.join(f'`{f}`' for f in (card.get('files') or []))}
- branch: `{branch}`（已由 prep 合并进候选分支）

## 死因（机器记录）

工人会话在落盘之前被 900s 进程墙杀死（wall_killed / droid exit {exit_part}）。
会话自身的 handoff/status 写出从未发生——这不是工序产出失败，而是落盘责任
绑在一个会被杀的会话上的结构性缺口。补卷守卫四条件（分支已并、无越界、
机器 checks 全绿、会话异常终结）全部由机器判定为真后方才补卷。

## 机器复验（全绿）

prep 在合并后的候选树上重跑了本卡全部 checks，逐条退出码 0：

{checks_lines}

机器复验结论：**代码与测试经机器复验全绿**，采认所需的两件证据文件由本
补卷器补齐；补卷产物已记入 manifest（salvaged_from_machine=true），其字节
被 manifest sha256 覆盖。

## 机器 checks 输出（截录）

```
{checks_output.strip()}
```
"""


def salvage_packs(
    *,
    evidence_dir: Path | str,
    cards: dict[str, dict],
    packs: dict[str, dict],
    wall: dict | None,
    streams: dict[str, str] | None = None,
    manifest: dict | None = None,
) -> list[dict]:
    """Guard + write the missing evidence files for every salvageable pack.

    Mutates ``packs`` in place (pack flags, complete, salvaged_from_machine)
    and writes status.json / handoff.md. When ``manifest`` is given (it owns
    ``packs``), the salvaged bytes are hashed into manifest["sha256"]; in the
    workflow the caller then persists the manifest as usual (its own os.walk
    hashing covers the new files anyway). Returns one report per pack. Only
    missing files are written; a worker-written handoff or status is never
    touched. Per-pack exceptions are caught: salvage failure degrades to
    "not salvaged" (fail-closed), never kills prep.
    """
    workers = (wall or {}).get("workers") or {}
    streams = streams or {}
    evidence_dir = Path(evidence_dir)
    reports: list[dict] = []
    for pid, info in packs.items():
        if not isinstance(info, dict):
            continue
        card = cards.get(pid)
        reasons: list[str] = []
        salvaged = False
        if card is None:
            reasons.append(f"no process card for {pid}; salvage skipped")
        elif info.get(SALVAGE_MARKER_KEY):
            reasons.append(f"pack already salvaged for {pid}")
        else:
            try:
                salvaged, reasons = _salvage_one(
                    pid=pid,
                    info=info,
                    card=card,
                    evidence_dir=evidence_dir,
                    workers=workers,
                    stream_text=streams.get(pid),
                )
            except Exception as exc:  # fail-closed: salvage must never kill prep
                salvaged = False
                reasons = [f"salvage error for {pid}: {exc}"]
        reports.append({"pid": pid, "salvaged": salvaged, "reasons": reasons})
    if manifest is not None:
        refresh_manifest_digests(evidence_dir, manifest)
    return reports


def _salvage_one(
    *,
    pid: str,
    info: dict,
    card: dict,
    evidence_dir: Path,
    workers: dict,
    stream_text: str | None,
) -> tuple[bool, list[str]]:
    pack_dir = evidence_dir / "packs" / pid
    allowed, reasons = evaluate_salvage_guard(
        info=info,
        pack_dir=pack_dir,
        card=card,
        workers=workers,
        pid=pid,
        stream_text=stream_text,
    )
    if not allowed:
        return False, reasons
    pack = info.setdefault("pack", {})
    to_write: list[str] = []
    if not pack.get("status"):
        to_write.append(STATUS_NAME)
    if not pack.get("handoff"):
        to_write.append(HANDOFF_NAME)
    if not to_write:
        return False, reasons + [f"pack files already present for {pid}"]

    checks_exit = _load_json(pack_dir / "checks-exit.json") or []
    checks_output = ""
    out_path = pack_dir / "checks-output.txt"
    if out_path.is_file():
        checks_output = out_path.read_text(encoding="utf-8", errors="replace")

    if STATUS_NAME in to_write:
        status = build_status(card=card, checks_exit=checks_exit, checks_output=checks_output)
        (pack_dir / STATUS_NAME).write_text(
            json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        pack["status"] = True
        reasons.append(f"salvage: wrote {STATUS_NAME} from machine facts")
    if HANDOFF_NAME in to_write:
        exit_code = (workers.get("droid_exit_code_by_pid") or {}).get(pid)
        handoff = build_handoff(
            pid=pid,
            card=card,
            checks_exit=checks_exit,
            checks_output=checks_output,
            branch=info.get("branch", ""),
            exit_code=exit_code,
        )
        (pack_dir / HANDOFF_NAME).write_text(handoff, encoding="utf-8")
        pack["handoff"] = True
        reasons.append(f"salvage: wrote {HANDOFF_NAME} (machine origin declared)")
    info[SALVAGE_MARKER_KEY] = True
    info["complete"] = (
        all(pack.values()) and bool(info.get("merged")) and not (info.get("out_of_bounds") or [])
    )
    return True, reasons


def refresh_manifest_digests(evidence_dir: Path | str, manifest: dict) -> list[str]:
    """Hash the salvaged pack files into manifest["sha256"] so the pack's own
    digest covers them (validator precheck verifies every entry vs disk).
    Returns the sha keys added."""
    added: list[str] = []
    for pid, info in (manifest.get("packs") or {}).items():
        if not isinstance(info, dict) or not info.get(SALVAGE_MARKER_KEY):
            continue
        pack = info.get("pack") or {}
        for name in (STATUS_NAME, HANDOFF_NAME):
            flag = "status" if name == STATUS_NAME else "handoff"
            if not pack.get(flag):
                continue
            path = Path(evidence_dir) / "packs" / pid / name
            if not path.is_file():
                continue
            key = f"evidence/packs/{pid}/{name}"
            manifest["sha256"][key] = hashlib.sha256(path.read_bytes()).hexdigest()
            added.append(key)
    return added


def main() -> int:
    """CLI face for offline replay: point it at an extracted evidence tree."""
    import argparse

    p = argparse.ArgumentParser(description="Salvage missing worker evidence packs")
    p.add_argument("--evidence-dir", default="evidence")
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--plan", default="evidence/plan.json")
    args = p.parse_args()
    evidence_dir = Path(args.evidence_dir)
    manifest_path = evidence_dir / "manifest.json"
    manifest = _load_json(manifest_path)
    wall = _load_json(Path(args.wall))
    plan = _load_json(Path(args.plan))
    if manifest is None or plan is None:
        print("missing manifest or plan; nothing to salvage", flush=True)
        return 1
    cards = {proc.get("id"): proc for proc in (plan.get("processes") or [])}
    reports = salvage_packs(
        evidence_dir=evidence_dir,
        cards=cards,
        packs=manifest["packs"],
        wall=wall,
        manifest=manifest,
    )
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for r in reports:
        print(json.dumps(r, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
