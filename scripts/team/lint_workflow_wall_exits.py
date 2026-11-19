#!/usr/bin/env python3
"""Batch-2 gate: every chain seat must record wall exit under if: always()."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# chain slot -> workflow job block name in team.yml
CHAIN_EXIT_OWNERS: dict[str, str] = {
    "lead": "lead",
    "worker": "workers-wall-merge",
    "prep": "prep",
    "validate": "validate",
    "replan": "replan",
    "worker2": "workers2-wall-merge",
    "prep2": "prep2",
    "validate2": "validate2",
    "assemble": "assemble",
}

JOB_HEADER = re.compile(r"^  (?P<name>[a-z0-9-]+):\n", re.MULTILINE)


def job_spans(text: str) -> dict[str, tuple[int, int]]:
    hits = [(m.start(), m.group("name")) for m in JOB_HEADER.finditer(text)]
    spans: dict[str, tuple[int, int]] = {}
    for i, (pos, name) in enumerate(hits):
        end = hits[i + 1][0] if i + 1 < len(hits) else len(text)
        spans[name] = (pos, end)
    return spans


def step_chunks(job_text: str) -> list[str]:
    parts = re.split(r"\n      - name:", job_text)
    return [("- name:" + p if i else p) for i, p in enumerate(parts) if p.strip()]


def wall_sync_always_ok(job_text: str, chain_job: str) -> tuple[bool, str]:
    for chunk in step_chunks(job_text):
        if "wall_sync_job.py" not in chunk and "assemble_chain_facts.py" not in chunk:
            continue
        if chain_job == "assemble":
            if "assemble_chain_facts.py" in chunk and "--assemble-exit" in chunk:
                if step_has_always(chunk):
                    return True, ""
            if f"--job {chain_job}" in chunk or f'--job "{chain_job}"' in chunk:
                if step_has_always(chunk):
                    return True, ""
        elif f"--job {chain_job}" in chunk or f'--job "{chain_job}"' in chunk:
            if step_has_always(chunk):
                return True, ""
    return False, f"no wall_sync/assemble-exit step with if: always() for chain.{chain_job}"


def step_has_always(step_text: str) -> bool:
    first_lines = "\n".join(step_text.splitlines()[:12])
    if re.search(r"if:\s*always\(\)", first_lines):
        return True
    if re.search(r"if:\s*\$\{\{\s*always\(\)", first_lines):
        return True
    return bool(re.search(r"if:\s*always\(\)", step_text[:400]))


def upload_always_ok(job_text: str, owner: str) -> tuple[bool, str]:
    """Jobs that patch the unified wall must re-upload under always()."""
    if owner in ("validate", "validate2"):
        for chunk in step_chunks(job_text):
            if "Upload foreman-run wall" in chunk and step_has_always(chunk):
                return True, ""
        return False, f"{owner} missing Upload foreman-run wall with if: always()"
    for chunk in step_chunks(job_text):
        if "Upload foreman-run" in chunk and "wall_sync_job" not in chunk:
            if step_has_always(chunk):
                return True, ""
            return False, f"{owner} foreman-run upload step lacks if: always()"
    if owner == "assemble":
        for chunk in step_chunks(job_text):
            if "Upload foreman-run" in chunk and step_has_always(chunk):
                return True, ""
        return False, "assemble missing Upload foreman-run with if: always()"
    return False, f"{owner} missing Upload foreman-run step"


def lead_not_success_only(job_text: str) -> list[str]:
    errs: list[str] = []
    for chunk in step_chunks(job_text):
        if "wall_sync_job.py" not in chunk or "--job lead" not in chunk:
            continue
        if re.search(r"--result\s+success", chunk) and not step_has_always(chunk):
            errs.append("lead wall_sync hardcodes --result success without always() (W-9)")
        if re.search(r'name:\s*Patch and upload ForemanRun wall \(lead\)', chunk):
            if not step_has_always(chunk):
                errs.append("legacy lead patch step without always() (W-9)")
    return errs


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--workflow", default=".github/workflows/team.yml")
    args = p.parse_args()
    text = Path(args.workflow).read_text(encoding="utf-8")
    spans = job_spans(text)
    errors: list[str] = []

    for chain_job, owner in CHAIN_EXIT_OWNERS.items():
        if owner not in spans:
            errors.append(f"workflow job {owner} not found for chain.{chain_job}")
            continue
        start, end = spans[owner]
        job_text = text[start:end]
        ok, msg = wall_sync_always_ok(job_text, chain_job)
        if not ok:
            errors.append(f"{owner}: {msg}")
        if owner in (
            "lead",
            "workers-wall-merge",
            "prep",
            "replan",
            "workers2-wall-merge",
            "prep2",
            "assemble",
        ):
            up_ok, up_msg = upload_always_ok(job_text, owner)
            if not up_ok:
                errors.append(f"{owner}: {up_msg}")

    if "lead" in spans:
        errors.extend(lead_not_success_only(text[spans["lead"][0] : spans["lead"][1]]))

    if errors:
        print("wall exit lint failures:", *errors, sep="\n", file=sys.stderr)
        return 1
    print("wall exit lint ok (batch-2 death matrix)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())