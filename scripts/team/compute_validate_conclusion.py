#!/usr/bin/env python3
"""Derive validate job conclusion from wall fields (W4 / B1)."""
from __future__ import annotations

import argparse
import sys

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
    # I-6: the session outcome is bookkeeping, not a verdict — when the
    # artifacts on disk were complete enough to adopt (a timeout kill after
    # the draft / sealed partial was written, L-6), the round is judged on
    # the artifacts like any other. Two outcomes still never clear the job
    # on their own: a skipped validator session (no judgeable processes —
    # the round-53 C accounting value) and a session that never started.
    session = (wall.get("budgets") or {}).get("session_outcome") or {}
    status = session.get("completion_status")
    session_bad = status in (
        "missing_output",
        "skipped_no_judgeable",
    ) or (status == "droid_failed" and not complete)
    # 52A fix: an escalated work-order conflict keeps the validate job red —
    # a contradiction in the order is never a silent green for downstream.
    escalated = bool(val.get("conflicts_escalated"))
    if adoption == "failed" or not complete or session_bad or escalated:
        conclusion = "failure"
    else:
        conclusion = "success"
    val = dict(val)
    val["job_conclusion_derived"] = conclusion
    merged = deep_merge(wall, {"validation": val})
    if adoption == "failed":
        # I-5 revalidate chain: a draft_timeout with the one validator-only
        # retry still available is not terminal — human_stop stays off so the
        # revalidate job can run. Any other adoption failure, or a draft
        # timeout after the revalidate job already started (its guard stamps
        # revalidate_run_started), terminates fail-closed. I-6: a
        # draft_timeout that nonetheless produced a complete artifact
        # (adoption ok) never reaches this branch. The marker read is the
        # SAME field adopt() consumes — one truth for "the retry is spent".
        gate = merged.get("replan_gate") or {}
        revalidate_pending = (
            val.get("adoption_error") == "draft_timeout"
            and not gate.get("revalidate_run_started")
        )
        if not revalidate_pending:
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