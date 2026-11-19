#!/usr/bin/env python3
"""CI lint: ForemanRun budget slice must match team.yml session wiring (batch-3)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from budget_resolve import assert_validator_job_budget
from foreman_run_lib import default_budgets, init_wall


SESSION_RUNNER = "run_droid_session.py"
BARE_DROID = re.compile(
    r"timeout\s+--signal=TERM\s+--kill-after=30s\s+\d+s\s+~/.local/bin/droid\s+exec"
)


def _validator_job_chunk(text: str) -> str:
    m = re.search(
        r"name:\s*validator \(squad-leader style, evidence only\)([\s\S]*?)(?:\n  [a-z]|\Z)",
        text,
    )
    return m.group(1) if m else ""


def lint_team_yml(workflow: Path) -> list[str]:
    text = workflow.read_text(encoding="utf-8")
    errs: list[str] = []
    wall = init_wall(run_id="lint", issue_number=0)
    errs.extend(assert_validator_job_budget(wall, job_timeout_min=15))

    defaults = default_budgets()["roles"]["validator"]
    configured = wall["budgets"]["roles"]["validator"]
    if configured.get("droid_wall_sec") != defaults["droid_wall_sec"]:
        errs.append("init_wall validator droid_wall_sec drift vs default_budgets")
    if configured.get("adopt_reserve_sec") != defaults.get("adopt_reserve_sec"):
        errs.append("init_wall validator adopt_reserve_sec drift vs default_budgets")

    if BARE_DROID.search(text):
        for hit in BARE_DROID.finditer(text):
            ctx = text[max(0, hit.start() - 80) : hit.end() + 40]
            if "worker" in ctx or "900s" in hit.group(0):
                continue
            if SESSION_RUNNER not in text[hit.start() : hit.start() + 400]:
                errs.append(
                    "bare droid exec for lead/validator/replan; use "
                    f"{SESSION_RUNNER} with wall budgets"
                )
                break

    def _step_chunk(step_name: str) -> str:
        needle = f"name: {step_name}"
        pos = text.find(needle)
        if pos < 0:
            return ""
        end = text.find("\n      - name:", pos + len(needle))
        return text[pos : end if end > 0 else len(text)]

    for step_name in (
        "Foreman splits the order into process cards",
        "Validator judges evidence packs only",
        "Foreman classifies failures and writes plan v2",
    ):
        chunk = _step_chunk(step_name)
        if not chunk:
            errs.append(f"missing step: {step_name}")
            continue
        if SESSION_RUNNER not in chunk:
            errs.append(f"{step_name} must invoke {SESSION_RUNNER}")
        if "FOREMAN_RUN_PATCH=1" not in chunk and "FOREMAN_RUN_PATCH: '1'" not in chunk:
            errs.append(f"{step_name} must set FOREMAN_RUN_PATCH=1")

    vchunk = _validator_job_chunk(text)
    if "ADOPT_RESERVE_SEC" not in vchunk and "adopt_reserve" not in vchunk:
        errs.append("validate job must read adopt reserve from wall (ADOPT_RESERVE_SEC)")
    if vchunk.count(SESSION_RUNNER) < 1:
        errs.append("validate job missing run_droid_session for validator")
    if text.count("Validator judges evidence packs only") >= 2:
        if text.count(f"name: {SESSION_RUNNER}") < 2 and vchunk.count(SESSION_RUNNER) < 2:
            pass  # counted in per-step checks below
    chunk2 = _step_chunk("Validator judges evidence packs only (round 2)")
    if chunk2:
        if SESSION_RUNNER not in chunk2:
            errs.append("validate2 validator step must invoke run_droid_session")
        if "ADOPT_RESERVE_SEC" not in chunk2:
            errs.append("validate2 must read ADOPT_RESERVE_SEC from wall")

    if "DROID_TIMEOUT_SEC=600" in text:
        errs.append("hardcoded validator DROID_TIMEOUT_SEC=600 remains in team.yml")

    return errs


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--workflow", default=".github/workflows/team.yml")
    args = p.parse_args()
    errs = lint_team_yml(Path(args.workflow))
    if errs:
        print("budget lint failures:", *errs, sep="\n", file=sys.stderr)
        return 1
    print("workflow budget lint ok (batch-3)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())