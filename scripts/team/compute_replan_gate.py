#!/usr/bin/env python3
"""Compute replan_gate.should_replan on wall (Y1)."""
from __future__ import annotations

import argparse
import json
import sys

from foreman_run_lib import deep_merge, load_wall, save_wall


def compute(wall: dict) -> dict:
    val = wall.get("validation") or {}
    adoption_ok = val.get("adoption_status") == "ok"
    overall = val.get("overall")
    failed_ids = val.get("failed_process_ids") or []
    unattributed = bool(val.get("unattributed_failure"))
    # 52A fix: escalated work-order conflicts (e.g. the round-52 A chaocipher
    # vector contradiction) are an actionable signal — they reopen the order
    # via replan instead of riding a pass through to close-out.
    escalated = bool(val.get("conflicts_escalated"))
    not_cancelled = (wall.get("chain") or {}).get("validate", {}).get("result") != "cancelled"
    verdict_key = next(
        (k for k in (wall.get("artifacts") or {}) if k.startswith("team-verdict-")),
        "",
    )
    verdict_complete = bool((wall.get("artifacts") or {}).get(verdict_key, {}).get("complete"))
    should = (
        adoption_ok
        and overall != "pass"
        and (len(failed_ids) > 0 or unattributed or escalated)
        and not_cancelled
        and verdict_complete
    )
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
    return deep_merge(wall, {"replan_gate": gate})


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--github-output", default="")
    args = p.parse_args()
    wall = load_wall(args.wall)
    merged = compute(wall)
    save_wall(merged, args.wall)
    should = merged["replan_gate"]["should_replan"]
    print("should_replan:", should)
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as out:
            out.write(f"should_replan={'true' if should else 'false'}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())