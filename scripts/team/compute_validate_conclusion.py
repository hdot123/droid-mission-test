#!/usr/bin/env python3
"""Derive validate job conclusion from wall fields (W4 / B1)."""
from __future__ import annotations

import argparse

from foreman_run_lib import deep_merge, load_wall, save_wall


def derive(wall: dict, *, round_num: int = 1) -> tuple[dict, str]:
    val = wall.get("validation") or {}
    adoption = val.get("adoption_status")
    prefix = "team-verdict2-" if round_num == 2 else "team-verdict-issue-"
    art_key = next(
        (k for k in (wall.get("artifacts") or {}) if k.startswith(prefix)),
        None,
    )
    if art_key is None:
        art_key = next(
            (k for k in (wall.get("artifacts") or {}) if k.startswith("team-verdict")),
            None,
        )
    complete = bool((wall.get("artifacts") or {}).get(art_key or "", {}).get("complete"))
    session = (wall.get("budgets") or {}).get("session_outcome") or {}
    session_bad = session.get("completion_status") in (
        "timeout",
        "droid_failed",
        "missing_output",
        # The round-53 accounting value for "no judgeable processes, droid
        # step skipped": an unstarted validator session never clears the
        # validate job on its own.
        "skipped_no_judgeable",
    )
    # 52A fix: an escalated work-order conflict keeps the validate job red —
    # a contradiction in the order is never a silent green for downstream.
    escalated = bool(val.get("conflicts_escalated"))
    conclusion = "failure" if adoption == "failed" or not complete or session_bad or escalated else "success"
    val = dict(val)
    val["job_conclusion_derived"] = conclusion
    merged = deep_merge(wall, {"validation": val})
    if adoption == "failed":
        merged = deep_merge(
            merged,
            {
                "human_stop": True,
                "closeout": {
                    "schema_version": "closeout-slice.v1",
                    "run_must_fail": True,
                },
            },
        )
    return merged, conclusion


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--round", type=int, default=1)
    p.add_argument("--github-output", default="")
    args = p.parse_args()
    wall = load_wall(args.wall)
    merged, conclusion = derive(wall, round_num=args.round)
    save_wall(merged, args.wall)
    print("validate_job_conclusion:", conclusion)
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as out:
            out.write(f"validate_job_conclusion={conclusion}\n")
    val = merged.get("validation") or {}
    prefix = "team-verdict2-" if args.round == 2 else "team-verdict-issue-"
    art_key = next((k for k in (merged.get("artifacts") or {}) if k.startswith(prefix)), None)
    complete = bool((merged.get("artifacts") or {}).get(art_key or "", {}).get("complete"))
    if val.get("adoption_status") == "failed" or not complete:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
