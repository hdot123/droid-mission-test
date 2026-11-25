#!/usr/bin/env python3
"""CI lint: every needs-context reference in a workflow must be declared.

Scrutiny PR1-0 / PR1-4: the revalidate jobs consumed
`needs.validate.outputs.should_revalidate` while `validate` declared no such
output, and read `needs.prep.outputs.manifest_sha256` without listing prep in
their needs. Both shapes are fail-dead wiring that string-presence tests and
the other lints cannot see: a step output reaches other jobs only through the
job's `outputs:` map, and the needs context only contains declared jobs.

The parser is a scoped structural reader, not a YAML dump: it walks the
two-space job blocks and four-space job keys of the workflow text and checks,
per job:
  - every `needs.<job>.outputs.<name>` reference resolves to a job that is
    listed in the consuming job's `needs` AND declares that output;
  - every `needs.<job>` reference (no outputs path) resolves to a listed job;
  - every entry in a job's `needs` list names an existing job.
Reusable jobs (`uses: ./.github/workflows/...`) are resolved through the
target workflow file's own outputs when it sits next to the checked file.
The whole job body (if, env, steps) is scanned for `needs.*` references, so
env-block misses like PR1-4 are caught. GHA expression syntax `${{ ... }}` is
matched structurally; unknown expression forms are ignored rather than guessed.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

JOB_HEADER = re.compile(r"^  (?P<name>[A-Za-z_][A-Za-z0-9_-]*):\s*$")
JOB_KEY = re.compile(r"^    (?P<key>[A-Za-z_-]+):\s*(?P<value>.*)$")
NEEDS_REF = re.compile(
    r"needs\.([A-Za-z_][A-Za-z0-9_-]*)(?:\.outputs\.([A-Za-z_][A-Za-z0-9_-]*))?"
)
STEP_HEADER = re.compile(r"^      - ")
USES_REF = re.compile(r"^    uses:\s*\./\.github/workflows/([A-Za-z0-9_.-]+\.yml)\s*$")


def parse_jobs(text: str) -> dict[str, dict]:
    """Extract per-job: needs list, declared outputs, uses target, full body."""
    jobs: dict[str, dict] = {}
    lines = text.splitlines()
    current: str | None = None
    for i, line in enumerate(lines):
        m = JOB_HEADER.match(line)
        if m:
            current = m.group("name")
            jobs[current] = {"needs": [], "outputs": {}, "uses": None, "body": [line]}
            continue
        if current is None:
            continue
        job = jobs[current]
        job["body"].append(line)
        um = USES_REF.match(line)
        if um:
            job["uses"] = um.group(1)
            continue
        km = JOB_KEY.match(line)
        if not km:
            continue
        key, value = km.group("key"), km.group("value").strip()
        if key == "needs":
            needs = value
            # collect continuation lines of a block-style needs list
            j = i + 1
            while j < len(lines) and re.match(r"^      - ", lines[j]):
                needs = needs or "[]"
                job["needs"].append(lines[j].lstrip()[2:].strip())
                j += 1
            if needs and needs != "[]":
                for dep in needs.strip("[]").split(","):
                    dep = dep.strip().strip("'\"")
                    if dep:
                        job["needs"].append(dep)
        elif key == "outputs":
            # collect `name: ${{ ... }}` lines until the next job key
            j = i + 1
            while j < len(lines):
                nm = re.match(r"^      ([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", lines[j])
                if not nm:
                    if re.match(r"^    [A-Za-z_-]+:", lines[j]) or JOB_HEADER.match(lines[j]):
                        break
                    j += 1
                    continue
                job["outputs"][nm.group(1)] = nm.group(2).strip()
                j += 1
    for job in jobs.values():
        job["body"] = "\n".join(job["body"])
    return jobs


def lint(text: str, *, resolve_reusable: Path | None = None) -> list[str]:
    errs: list[str] = []
    jobs = parse_jobs(text)
    if not jobs:
        return ["workflow: no job blocks parsed"]
    # reusable-job outputs: parse the target workflow file when available
    reusable: dict[str, dict] = {}
    if resolve_reusable is not None:
        for name, job in jobs.items():
            if job.get("uses"):
                target = resolve_reusable / job["uses"]
                if target.is_file():
                    reusable[name] = parse_jobs(target.read_text(encoding="utf-8"))
    for job_name, job in jobs.items():
        for dep in job["needs"]:
            if dep not in jobs:
                errs.append(f"{job_name}: needs unknown job {dep!r}")
        for m in NEEDS_REF.finditer(job["body"]):
            dep, out_name = m.group(1), m.group(2)
            if dep not in jobs:
                errs.append(
                    f"{job_name}: references needs.{dep} which is not a declared job"
                )
                continue
            if dep not in job["needs"]:
                errs.append(
                    f"{job_name}: references needs.{dep} but {dep} is not in its needs list"
                )
                continue
            if out_name is None:
                continue
            if dep in reusable:
                # reusable job: outputs live on the target workflow's jobs
                target_jobs = reusable[dep]
                declared = any(
                    out_name in tj["outputs"] for tj in target_jobs.values()
                )
                if not declared:
                    errs.append(
                        f"{job_name}: references needs.{dep}.outputs.{out_name} "
                        f"but the reusable workflow {job['uses']} declares no such output"
                    )
                continue
            outputs = jobs[dep]["outputs"]
            if out_name not in outputs:
                errs.append(
                    f"{job_name}: references needs.{dep}.outputs.{out_name} "
                    f"but {dep} declares no such output (undeclared outputs are never true)"
                )
    return errs


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--workflow", default=".github/workflows/team.yml")
    args = p.parse_args()
    path = Path(args.workflow)
    text = path.read_text(encoding="utf-8")
    errs = lint(text, resolve_reusable=path.parent)
    if errs:
        print("needs lint failures:", *errs, sep="\n", file=sys.stderr)
        return 1
    print(f"needs lint ok ({path.name}: every needs reference is declared)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
