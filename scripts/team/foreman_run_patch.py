#!/usr/bin/env python3
"""CLI: patch-merge ForemanRun wall (W1)."""
from __future__ import annotations

import argparse
import json
import sys

from foreman_run_lib import deep_merge, load_wall, save_wall, validate_with_jsonschema


def main() -> int:
    p = argparse.ArgumentParser(description="Patch-merge foreman-run.json")
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--patch", required=True, help="JSON patch file or inline JSON")
    p.add_argument("--inline", action="store_true", help="--patch is JSON string")
    p.add_argument("--check-only", action="store_true")
    args = p.parse_args()

    if args.inline:
        patch = json.loads(args.patch)
    else:
        patch = json.loads(open(args.patch, encoding="utf-8").read())

    try:
        wall = load_wall(args.wall)
    except FileNotFoundError:
        print(f"wall missing: {args.wall}", file=sys.stderr)
        return 1

    merged = deep_merge(wall, patch)
    errs = validate_with_jsonschema(merged)
    if errs:
        print("schema errors:", *errs[:30], sep="\n", file=sys.stderr)
        return 1
    if args.check_only:
        print("ok")
        return 0
    save_wall(merged, args.wall)
    print("patched", args.wall)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())