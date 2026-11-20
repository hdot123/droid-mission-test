#!/usr/bin/env python3
"""End-of-job wall sync: chain result + upload-ready flag."""
from __future__ import annotations

import argparse
import json
import sys

from foreman_run_lib import (
    chain_summary_code_for_result,
    load_wall,
    normalize_chain_job_result,
    patch_chain_job,
    save_wall,
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--job", required=True)
    p.add_argument("--result", required=True)
    p.add_argument("--produced", choices=["true", "false"], default="false")
    p.add_argument("--patch", default="{}", help="extra JSON patch")
    p.add_argument("--detail", default=None, help="override chain_facts.detail")
    args = p.parse_args()
    job_result = normalize_chain_job_result(args.result)
    summary_code = chain_summary_code_for_result(job_result)
    detail = args.detail or f"{args.job} job result={job_result}"
    wall = load_wall(args.wall)
    wall = patch_chain_job(
        wall,
        args.job,
        result=job_result,
        produced_required_artifact=args.produced == "true",
        chain_facts={
            "summary_code": summary_code,
            "detail": detail,
            "forbidden_phrases": [],
        },
    )
    extra = json.loads(args.patch)
    from foreman_run_lib import deep_merge

    wall = deep_merge(wall, extra)
    save_wall(wall, args.wall)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())