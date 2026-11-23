#!/usr/bin/env python3
"""Pre-upload gate: artifact.complete on ForemanRun (B2)."""
from __future__ import annotations

import argparse
import sys

from foreman_run_lib import load_wall


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--name", required=True, help="artifacts map key")
    args = p.parse_args()
    wall = load_wall(args.wall)
    art = (wall.get("artifacts") or {}).get(args.name)
    if not art:
        print(f"unknown artifact key: {args.name}", file=sys.stderr)
        return 1
    if not art.get("complete"):
        missing = art.get("missing") or ["(unspecified)"]
        print(f"artifact incomplete: missing {missing}", file=sys.stderr)
        return 1
    print(f"artifact {args.name} complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
