#!/usr/bin/env python3
"""Compute replan_gate.should_replan on wall (Y1)."""
from __future__ import annotations

import argparse
import json
import sys

from foreman_run_lib import deep_merge, load_wall, save_wall

# The 2/2 iteration cap is the workflow graph itself: validate2's gate is the
# terminal one, so its verdict — not round 1's — is the final word on
# should_replan (round-52 C left a stale true on the wall after round 2
# absorbed the loop cleanly).
_TERMINAL_ROUND = 2


class StaleGateError(RuntimeError):
    """Raised when a terminal-round recomputation has no final verdict to read."""


def compute(wall: dict, *, round_num: int = 1) -> dict:
    val = wall.get("validation") or {}
    if round_num >= _TERMINAL_ROUND:
        if (val.get("round") or 0) < _TERMINAL_ROUND:
            raise StaleGateError(
                "terminal gate recomputation requires the round-2 validation slice "
                "on the wall (fail-closed: a killed validate2 never clears the gate)"
            )
        not_cancelled = (wall.get("chain") or {}).get("validate2", {}).get(
            "result"
        ) != "cancelled"
        verdict_key = next(
            (k for k in (wall.get("artifacts") or {}) if k.startswith("team-verdict2-")),
            "",
        )
    else:
        not_cancelled = (wall.get("chain") or {}).get("validate", {}).get(
            "result"
        ) != "cancelled"
        verdict_key = next(
            (k for k in (wall.get("artifacts") or {}) if k.startswith("team-verdict-")),
            "",
        )
    adoption_ok = val.get("adoption_status") == "ok"
    overall = val.get("overall")
    failed_ids = val.get("failed_process_ids") or []
    unattributed = bool(val.get("unattributed_failure"))
    # 52A fix: escalated work-order conflicts (e.g. the round-52 A chaocipher
    # vector contradiction) are an actionable signal — they reopen the order
    # via replan instead of riding a pass through to close-out.
    escalated = bool(val.get("conflicts_escalated"))
    verdict_complete = bool((wall.get("artifacts") or {}).get(verdict_key, {}).get("complete"))
    should = (
        adoption_ok
        and overall != "pass"
        and (len(failed_ids) > 0 or unattributed or escalated)
        and not_cancelled
        and verdict_complete
    )
    # I-5 revalidate chain: adopt_verdict requests the single validator-only
    # retry via should_revalidate; this recomputation carries the flag through
    # (never flips it off — only a successful adoption clears it) and mirrors
    # the run-start marker the revalidate job's guard stamps, so the workflow
    # guard and the wall stay one truth.
    should_revalidate = bool((wall.get("replan_gate") or {}).get("should_revalidate"))
    reasons = []
    if adoption_ok and overall != "pass":
        if failed_ids:
            reasons.append("overall_not_pass")
        if unattributed:
            reasons.append("unattributed_failure")
        if escalated:
            reasons.append("conflicts_escalated")
    gate = {
        "schema_version": "replan-gate.v1",
        "should_replan": should,
        "should_revalidate": should_revalidate,
        "revalidate_run_started": bool(
            (wall.get("replan_gate") or {}).get("revalidate_run_started")
        ),
        "reasons": reasons,
        "inputs_satisfied": {
            "adoption_status_ok": adoption_ok,
            "verdict_artifact_complete": verdict_complete,
            "not_cancelled": not_cancelled,
        },
        "forbidden_legacy": {
            "validate_job_success_only": False,
            "string_compare_failed_processes": False,
        },
    }
    if round_num >= _TERMINAL_ROUND:
        gate["round"] = round_num
    return deep_merge(wall, {"replan_gate": gate})


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--github-output", default="")
    p.add_argument(
        "--round",
        type=int,
        default=1,
        help="validate round whose verdict the gate is computed from; the "
        "terminal round overwrites any stale earlier-round gate value",
    )
    args = p.parse_args()
    wall = load_wall(args.wall)
    merged = compute(wall, round_num=args.round)
    save_wall(merged, args.wall)
    should = merged["replan_gate"]["should_replan"]
    revalidate = merged["replan_gate"]["should_revalidate"]
    print("should_replan:", should)
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as out:
            out.write(f"should_replan={'true' if should else 'false'}\n")
            out.write(f"should_revalidate={'true' if revalidate else 'false'}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())