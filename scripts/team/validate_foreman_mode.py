#!/usr/bin/env python3
"""L6: prod mode caps max_processes=3 on plan JSON."""
from __future__ import annotations

import argparse
import json
import sys


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--plan", required=True)
    p.add_argument("--mode", default="test")
    args = p.parse_args()
    plan = json.loads(open(args.plan, encoding="utf-8").read())
    procs = plan.get("processes") or []
    if args.mode == "prod" and len(procs) > 3:
        print(f"prod foreman_mode allows at most 3 processes, got {len(procs)}", file=sys.stderr)
        return 1
    if "foreman_mode" in plan and plan["foreman_mode"] not in ("test", "prod"):
        print("invalid plan foreman_mode", file=sys.stderr)
        return 1
    print("foreman_mode gate ok", args.mode, "processes", len(procs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())