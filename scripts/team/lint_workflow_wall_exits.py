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

MERGE_UPSTREAM_CANCELLED: dict[str, str] = {
    "workers-wall-merge": "needs.lead.result == 'cancelled'",
    "workers2-wall-merge": "needs.replan.result == 'cancelled'",
}

WALL_ACCOUNTING_MARKERS = (
    "wall_sync_job.py",
    "assemble_chain_facts.py",
    "write_worker_delta.py",
)

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


def step_if_expr(step_text: str) -> str | None:
    """First step-level if: in the chunk (before run:/uses:), not downstream job if."""
    for line in step_text.splitlines()[1:14]:
        if re.match(r"\s+(run:|uses:)", line):
            break
        m = re.match(r"\s+if:\s*\$\{\{([^}]+)\}\}", line)
        if m:
            return m.group(1).strip()
        m2 = re.match(r"\s+if:\s*(.+)", line)
        if m2:
            return m2.group(1).strip()
    return None


def step_has_always(step_text: str) -> bool:
    expr = step_if_expr(step_text)
    if not expr:
        return "if:" not in step_text[:120]
    if "!cancelled()" in expr:
        return False
    return "always()" in expr


def merge_jobs_admit_upstream_cancelled(text: str, spans: dict[str, tuple[int, int]]) -> list[str]:
    errs: list[str] = []
    for job, need_cancelled in MERGE_UPSTREAM_CANCELLED.items():
        if job not in spans:
            errs.append(f"{job}: workflow job not found (cancelled merge gate)")
            continue
        start, end = spans[job]
        job_text = text[start:end]
        m = re.search(r"\n    if:\s*([\s\S]*?)\n    runs-on:", job_text)
        if not m:
            errs.append(f"{job}: missing job-level if (cancelled merge gate)")
            continue
        block = re.sub(r"\s+", " ", m.group(1).replace(">-", " "))
        if need_cancelled.replace(" ", "") not in block.replace(" ", ""):
            errs.append(f"{job}: job if must include {need_cancelled}")
        if "!cancelled()" in block:
            errs.append(f"{job}: merge job if must not use !cancelled() (workflow-cancel wall sync)")
    return errs


def wall_accounting_steps_no_cancelled(text: str) -> list[str]:
    """写账/上传步在 workflow cancel 时仍须可执行；禁止 always() && !cancelled()."""
    errs: list[str] = []
    for part in re.split(r"\n      - name:", text):
        if not part.strip():
            continue
        chunk = "- name:" + part if not part.startswith("- name:") else part
        name_m = re.search(r"name:\s*(.+)", chunk)
        step_name = name_m.group(1).strip() if name_m else "(unknown)"
        is_wall_sync = any(marker in chunk for marker in WALL_ACCOUNTING_MARKERS)
        is_wall_upload = "Upload foreman-run" in step_name or (
            "Upload worker" in step_name and "delta" in step_name.lower()
        )
        if not is_wall_sync and not is_wall_upload:
            continue
        if "assemble_chain_facts.py" in chunk and "--assemble-exit" not in chunk:
            continue
        expr = step_if_expr(chunk)
        if expr and "!cancelled()" in expr:
            errs.append(
                f"wall accounting step must not guard on !cancelled(): {step_name}"
            )
    return errs


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


def derive_chain_sync_not_same_step(text: str) -> list[str]:
    """W-11: bash -e must not skip wall_sync after derive exit 1 in the same run block."""
    errs: list[str] = []
    for part in re.split(r"\n      - name:", text):
        if not part.strip():
            continue
        chunk = "- name:" + part if not part.startswith("- name:") else part
        name_m = re.search(r"name:\s*(.+)", chunk)
        step_name = name_m.group(1).strip() if name_m else "(unknown)"
        run_m = re.search(r"\n\s+run:\s*\|\s*\n([\s\S]*?)(?=\n\s{6}\w|\n\s+env:|\n\s+if:|\Z)", chunk)
        if not run_m:
            continue
        run_body = run_m.group(1)
        has_derive = "compute_validate_conclusion.py" in run_body
        has_sync = "wall_sync_job.py" in run_body and "--job validate" in run_body
        has_sync2 = "wall_sync_job.py" in run_body and "--job validate2" in run_body
        if has_derive and (has_sync or has_sync2):
            errs.append(
                f"W-11: derive and wall_sync must be separate steps (bash -e truncation): {step_name}"
            )
        has_merge_redo = "merge_worker_deltas.py" in run_body
        has_worker_sync = "wall_sync_job.py" in run_body and (
            "--job worker" in run_body or "--job worker2" in run_body
        )
        if has_merge_redo and has_worker_sync:
            errs.append(
                f"W-11: merge re-run and wall_sync must be separate steps (bash -e truncation): {step_name}"
            )
        if (
            "assemble_chain_facts.py" in run_body
            and "--assemble-exit" in run_body
            and re.search(r"\n\s+exit\s+1\b", run_body)
        ):
            errs.append(
                f"W-11: assemble-exit sync must not share run: with exit 1 guard: {step_name}"
            )
    return errs


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

    errors.extend(merge_jobs_admit_upstream_cancelled(text, spans))
    errors.extend(wall_accounting_steps_no_cancelled(text))
    errors.extend(derive_chain_sync_not_same_step(text))

    if errors:
        print("wall exit lint failures:", *errors, sep="\n", file=sys.stderr)
        return 1
    print("wall exit lint ok (batch-2 death matrix)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())