#!/usr/bin/env python3
"""Emit worker matrix delta JSON for foreman-run merge.

F1 (worker-delta structured session outcome): beyond the job-level
``result``, the delta carries the session death facts the replan input face
and the salvage guard need — all classified from machine evidence only:

- ``session_outcome``: ok | wall_killed | job_wall_cancelled
- ``droid_exit_code``: the session step's own exit code (124 = 900s wall,
  137 = its SIGKILL path, 1 = droid self-crash, a different death family)
- ``stream_tail_marker``: worker-stream.jsonl ends on the interrupted
  tool_error (session killed mid-action, never reached its own end)

Job-wall cancellation outranks the session verdict: a cancelled job still
records the session evidence, but the outcome names the 25m envelope.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

STREAM_INTERRUPT_MARKER = "Error: Tool execution was interrupted"

# GNU timeout --signal=TERM --kill-after returns 124 when the process
# honours TERM and 137 when only the --kill-after SIGKILL lands; both are
# the same machine-proven wall kill. Any other non-zero exit whose stream
# never carried a completion event is the same abnormal-termination family
# (a self-ended session always emits completion). Exit 1 (and negative
# codes — not producible in production anyway: bash $? is 0-255 and the
# 128+signal convention yields POSITIVE codes like 137/143) with no
# completion is the droid self-crash death family — a different death,
# kept ok: the salvage guard reads droid_exit_code directly for that family.
# Exits that belong to the session itself, never to a wall: 0 self-ended,
# 1 self-crash. Only these (plus negatives) keep ok with no completion.
SELF_EXIT_CODES = (0, 1)


def classify_session_outcome(
    *,
    droid_exit_code: int | None,
    job_cancelled: bool,
    stream_tail: str | None,
) -> tuple[str, bool]:
    """(session_outcome, stream_tail_marker) from exit code + stream shape.

    ``stream_tail`` names the caller's contract, not the amount scanned: it
    may be the stream's LAST LINE, its full text, or None (stream
    missing/unreadable). The completion-absence clause (scrutiny NC-1)
    scans every line of the given text — a completion event anywhere proves
    the session ended on its own. The interrupt marker alone keys on the
    last non-empty line, since "the last event was interrupted" is a
    tail-shaped fact.
    """
    marker = bool(stream_tail) and _is_interrupt_event(stream_tail)
    if job_cancelled:
        return "job_wall_cancelled", marker
    if droid_exit_code == 124 or marker:
        return "wall_killed", marker
    if droid_exit_code == 137:
        return "wall_killed", marker
    if (
        droid_exit_code is not None
        and droid_exit_code not in SELF_EXIT_CODES
        and droid_exit_code > 0
        and not _stream_has_completion_event(stream_tail)
    ):
        return "wall_killed", marker
    return "ok", marker


def _is_interrupt_event(tail_text: str) -> bool:
    """True when the tail's last non-empty line is the interrupted tool_error."""
    last: str | None = None
    for line in tail_text.splitlines():
        if line.strip():
            last = line
    if last is None:
        return False
    try:
        event = json.loads(last)
    except ValueError:
        return last.strip().endswith(f'"message":"{STREAM_INTERRUPT_MARKER}"}}')
    # JSON-valid but non-object tails ('null', '42', '[1,2]', 'true',
    # '"text"') are not interrupt events; without this guard the .get below
    # raises and main() dies before the delta file is written at all.
    if not isinstance(event, dict):
        return False
    return (event.get("error") or {}).get("message") == STREAM_INTERRUPT_MARKER


def _stream_has_completion_event(stream_tail: str | None) -> bool:
    """True when any event in the stream text is a completion event
    ({"type": "completion", ...} — the healthy terminal event droid emits
    when a session ends on its own)."""
    if not stream_tail:
        return False
    for line in stream_tail.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("type") == "completion":
            return True
    return False


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--pid", required=True)
    p.add_argument("--result", required=True, choices=["success", "failure", "cancelled"])
    p.add_argument("--out", default="worker-delta.json")
    p.add_argument("--cancel-reason", default="")
    p.add_argument(
        "--stream",
        default="worker-stream.jsonl",
        help="session stream file; its full text feeds the completion scan, "
        "its last non-empty line the interrupt marker",
    )
    args = p.parse_args()
    if args.result == "cancelled" and not args.cancel_reason:
        args.cancel_reason = "job_wall_25m"
    job_status = (os.environ.get("JOB_STATUS") or "").strip().lower()
    if job_status == "failure":
        args.result = "failure"
    elif job_status == "cancelled":
        args.result = "cancelled"
    # Infer failure if checks marker exists
    if Path(f"team/status/{args.pid}.checks-failed.marker").exists():
        args.result = "failure"

    raw_exit = (os.environ.get("DROID_EXIT_CODE") or "").strip()
    droid_exit_code: int | None = None
    if raw_exit.lstrip("-").isdigit():
        droid_exit_code = int(raw_exit)
    job_cancelled = args.result == "cancelled"
    try:
        stream_text = read_stream_text(Path(args.stream))
    except OSError:
        stream_text = None
    session_outcome, stream_tail_marker = classify_session_outcome(
        droid_exit_code=droid_exit_code,
        job_cancelled=job_cancelled,
        stream_tail=stream_text,
    )

    payload: dict = {"pid": args.pid, "result": args.result}
    if args.cancel_reason:
        payload["cancel_reason"] = args.cancel_reason
    payload["session_outcome"] = session_outcome
    payload["droid_exit_code"] = droid_exit_code
    payload["stream_tail_marker"] = stream_tail_marker
    Path(args.out).write_text(json.dumps(payload) + "\n", encoding="utf-8")
    print("delta:", payload)
    return 0


def read_last_stream_line(path: Path) -> str | None:
    """Last non-empty line of the session stream, or None when absent."""
    text = read_stream_text(path)
    if text is None:
        return None
    last: str | None = None
    for line in text.splitlines():
        if line.strip():
            last = line
    return last


def read_stream_text(path: Path) -> str | None:
    """The whole session stream text, or None when absent/unreadable."""
    if not path.is_file():
        return None
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


if __name__ == "__main__":
    raise SystemExit(main())
