#!/usr/bin/env python3
"""Post issue comment; exit 1 on failure when hard_required (B4/W2)."""
from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--issue", required=True)
    p.add_argument("--body-file", required=True)
    p.add_argument("--hard-required", action="store_true")
    p.add_argument("--wall-patch", default="", help="JSON patch for closeout.comments.<key>")
    args = p.parse_args()
    r = subprocess.run(
        ["gh", "issue", "comment", args.issue, "--body-file", args.body_file],
        capture_output=True,
        text=True,
    )
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