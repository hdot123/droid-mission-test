#!/usr/bin/env python3
"""Emit worker matrix delta JSON for foreman-run merge."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--pid", required=True)
    p.add_argument("--result", required=True, choices=["success", "failure", "cancelled"])
    p.add_argument("--out", default="worker-delta.json")
    p.add_argument("--cancel-reason", default="")
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
    payload = {"pid": args.pid, "result": args.result}
    if args.cancel_reason:
        payload["cancel_reason"] = args.cancel_reason
    Path(args.out).write_text(json.dumps(payload) + "\n", encoding="utf-8")
    print("delta:", payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
