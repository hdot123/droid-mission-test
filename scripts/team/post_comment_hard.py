#!/usr/bin/env python3
"""Post issue comment; exit 1 on failure when hard_required (B4/W2)."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

from foreman_run_lib import deep_merge, load_wall, save_wall


def patch_wall_comment(wall_path: str, comment_key: str, posted: bool) -> None:
    try:
        wall = load_wall(wall_path)
    except Exception as exc:
        print(f"::warning::wall patch skipped: {exc}", file=sys.stderr)
        return
    patch = {
        "closeout": {
            "schema_version": "closeout-slice.v1",
            "comments": {comment_key: {"posted": posted}},
        }
    }
    merged = deep_merge(wall, patch)
    save_wall(merged, wall_path)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--issue", required=True)
    p.add_argument("--body-file", required=True)
    p.add_argument("--hard-required", action="store_true")
    p.add_argument(
        "--wall-patch",
        default="",
        help='JSON: {"key":"plan_dispatch","wall":"foreman-run.json"}',
    )
    args = p.parse_args()
    r = subprocess.run(
        ["gh", "issue", "comment", args.issue, "--body-file", args.body_file],
        capture_output=True,
        text=True,
    )
    patch_info: dict = {}
    if args.wall_patch:
        try:
            patch_info = json.loads(args.wall_patch)
        except json.JSONDecodeError:
            print("invalid --wall-patch JSON", file=sys.stderr)
            if args.hard_required:
                return 1

    wall_path = patch_info.get("wall", "foreman-run.json")
    comment_key = patch_info.get("key", "")
    if comment_key:
        patch_wall_comment(wall_path, comment_key, posted=(r.returncode == 0))

    if r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        if args.hard_required:
            return 1
        print("::warning::comment failed (soft)")
        return 0
    print("comment posted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())