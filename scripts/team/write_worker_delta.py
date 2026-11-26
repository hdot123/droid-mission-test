#!/usr/bin/env python3
"""Emit worker matrix delta JSON for foreman-run merge.

F1 (worker-delta structured session outcome): beyond the job-level
``result``, the delta carries the session death facts the replan input face
and the salvage guard need — all classified from machine evidence only:

- ``session_outcome``: ok | wall_killed | job_wall_cancelled
- ``droid_exit_code``: the session step's own exit code (124 = 900s wall)
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


def classify_session_outcome(
    *,
    droid_exit_code: int | None,
    job_cancelled: bool,
    stream_tail: str | None,
) -> tuple[str, bool]:
    """(session_outcome, stream_tail_marker) from exit code + stream tail.

    stream_tail is the text of the stream's last line (or None when the
    stream is missing/unreadable). The kill is proven by either signal
    independently: exit 124 (GNU timeout) or an interrupted tool_error as
    the final stream event.
    """
    marker = bool(stream_tail) and _is_interrupt_event(stream_tail)
    if job_cancelled:
        return "job_wall_cancelled", marker
    if droid_exit_code == 124 or marker:
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


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--pid", required=True)
    p.add_argument("--result", required=True, choices=["success", "failure", "cancelled"])
    p.add_argument("--out", default="worker-delta.json")
    p.add_argument("--cancel-reason", default="")
    p.add_argument(
        "--stream",
        default="worker-stream.jsonl",
        help="session stream file whose final event is inspected for the interrupt marker",
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
        stream_tail = read_last_stream_line(Path(args.stream))
    except OSError:
        stream_tail = None
    session_outcome, stream_tail_marker = classify_session_outcome(
        droid_exit_code=droid_exit_code,
        job_cancelled=job_cancelled,
        stream_tail=stream_tail,
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
    if not path.is_file():
        return None
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        last: str | None = None
        for line in fh:
            if line.strip():
                last = line
    return last


if __name__ == "__main__":
    raise SystemExit(main())
