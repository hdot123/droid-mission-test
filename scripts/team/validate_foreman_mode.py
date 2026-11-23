#!/usr/bin/env python3
"""L6: prod mode caps max_processes=3; production profile requires explicit prod."""
from __future__ import annotations

import argparse
import json
import os
import sys


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--plan", required=True)
    p.add_argument("--mode", default="test")
    args = p.parse_args()
    with open(args.plan, encoding="utf-8") as fh:
        plan = json.loads(fh.read())
    procs = plan.get("processes") or []
    effective_mode = args.mode
    if "foreman_mode" in plan:
        effective_mode = plan["foreman_mode"]
    require_prod = os.environ.get("FOREMAN_REQUIRE_PROD", "").lower() in ("1", "true", "yes")
    if require_prod and effective_mode != "prod":
        print(
            "FOREMAN_REQUIRE_PROD set but foreman_mode is not prod "
            f"(workflow={args.mode!r}, plan={plan.get('foreman_mode', '')!r})",
            file=sys.stderr,
        )
        return 1
    if args.mode == "prod" and len(procs) > 3:
        print(f"prod foreman_mode allows at most 3 processes, got {len(procs)}", file=sys.stderr)
        return 1
    if "foreman_mode" in plan and plan["foreman_mode"] not in ("test", "prod"):
        print("invalid plan foreman_mode", file=sys.stderr)
        return 1
    print("foreman_mode gate ok", effective_mode, "processes", len(procs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
