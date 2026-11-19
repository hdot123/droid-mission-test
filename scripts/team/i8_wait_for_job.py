#!/usr/bin/env python3
"""Poll until a GitHub Actions job name contains a substring."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--run-id", required=True)
    p.add_argument("--name-substr", required=True)
    p.add_argument("--timeout", type=int, default=3600)
    p.add_argument("--interval", type=int, default=20)
    args = p.parse_args()
    deadline = time.time() + args.timeout
    while time.time() < deadline:
        r = subprocess.run(
            ["gh", "run", "view", args.run_id, "--json", "jobs"],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            time.sleep(args.interval)
            continue
        jobs = json.loads(r.stdout).get("jobs") or []
        for j in jobs:
            name = j.get("name") or ""
            if args.name_substr.lower() in name.lower():
                if j.get("status") == "in_progress":
                    print("job in progress:", name)
                    return 0
                if j.get("status") == "completed":
                    print("job already completed:", name)
                    return 0
        time.sleep(args.interval)
    print("timeout waiting for job", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())