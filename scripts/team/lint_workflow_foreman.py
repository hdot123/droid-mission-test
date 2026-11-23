#!/usr/bin/env python3
"""CI lint: ban legacy replan gates, half-upload patterns, and API wall escape routes."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FORBIDDEN = [
    (re.compile(r"failed_processes\s*!=\s*['\"]\\?\\[\\]['\"]"), "string compare failed_processes != '[]'"),
    (re.compile(r"needs\.validate\.result\s*==\s*['\"]success['\"]"), "replan bound to validate.result success only"),
    (re.compile(r"fail_text\s*=\s*\{"), "static fail_text fallback in assemble"),
    (re.compile(r"备料未启动"), "forbidden static phrase 备料未启动 in workflow"),
    (re.compile(r"状态代偿记录"), "forbidden 状态代偿记录 (I7)"),
    (re.compile(r"状态代偿说明"), "forbidden 状态代偿说明 (I7)"),
    (re.compile(r"adopt_verdict\.py[^\n]*\|\|\s*true"), "adopt_verdict must not use || true (I5)"),
    (re.compile(r"compute_validate_conclusion\.py[^\n]*\|\|\s*true"), "derive must not use || true (I5)"),
    (re.compile(r"init_wall"), "init_wall forbidden in team.yml except via env-check (I3)"),
    (
        re.compile(r"pick_verdict_from_wall\.py[\s\S]{0,800}?--chain-result"),
        "pick_verdict must not inject needs.*_RESULT (I2 fail-closed)",
    ),
    (
        re.compile(r"env_check_wall\.py[^\n]*\|\|\s*true"),
        "env_check_wall must not use || true (W3 fail-closed)",
    ),
]

PREP_GATE = re.compile(
    r"name: prep \(merge and pack evidence\)[\s\S]{0,800}?workers-wall-merge\.outputs\.prep_should_run",
)
PREP2_GATE = re.compile(
    r"name: prep round 2[\s\S]{0,800}?workers2-wall-merge\.outputs\.prep_should_run",
)


def worker_delta_download_lax(text: str) -> list[str]:
    errs: list[str] = []
    for m in re.finditer(r"Download (?:all )?worker2? deltas", text):
        chunk = text[m.start() : m.start() + 220]
        if "continue-on-error: true" in chunk:
            errs.append("worker delta download must not use continue-on-error (W1)")
    return errs


def foreman_run_download_lax(text: str) -> list[str]:
    errs: list[str] = []
    for m in re.finditer(r"Download ForemanRun wall", text):
        chunk = text[m.start() : m.start() + 220]
        if "continue-on-error: true" in chunk:
            errs.append("foreman-run download must not use continue-on-error (I3)")
    return errs


def assemble_closeout_comment_wall_patch(text: str) -> list[str]:
    """Assemble final status card must patch closeout.comments (III-3a / I4)."""
    errs: list[str] = []
    anchor = text.find('body-file final-comment.md')
    if anchor < 0:
        errs.append("assemble closeout post_comment_hard step not found (III-3a)")
        return errs
    chunk = text[max(0, anchor - 400) : anchor + 400]
    if "--wall-patch" not in chunk:
        errs.append("assemble closeout post_comment_hard must include --wall-patch (III-3a)")
    elif "final_status_card" not in chunk:
        errs.append("assemble closeout --wall-patch key must be final_status_card")
    return errs


def post_comment_hard_has_gh_token(text: str) -> list[str]:
    """Every workflow step that invokes post_comment_hard.py must set GH_TOKEN (B4/I4)."""
    errs: list[str] = []
    needle = "post_comment_hard.py"
    for pos in range(len(text)):
        hit = text.find(needle, pos)
        if hit == -1:
            break
        pos = hit
        step_start = text.rfind("\n      - name:", 0, hit)
        if step_start < 0:
            step_start = text.rfind("\n    - name:", 0, hit)
        if step_start < 0:
            errs.append("post_comment_hard.py step chunk not found")
            continue
        step_end = text.find("\n      - name:", hit)
        if step_end < 0:
            step_end = len(text)
        chunk = text[step_start:step_end]
        if not re.search(r"^\s+GH_TOKEN:", chunk, re.MULTILINE):
            name_m = re.search(r"- name:\s*(.+)", chunk)
            step_name = name_m.group(1).strip() if name_m else "(unknown step)"
            errs.append(f"post_comment_hard step missing GH_TOKEN in env: {step_name}")
    return errs


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--workflow", default=".github/workflows/team.yml")
    args = p.parse_args()
    text = Path(args.workflow).read_text(encoding="utf-8")
    errors: list[str] = []
    for rx, msg in FORBIDDEN:
        if rx.search(text):
            errors.append(msg)
    if not PREP_GATE.search(text):
        errors.append("prep job must gate on workers-wall-merge.outputs.prep_should_run (I1)")
    if not PREP2_GATE.search(text):
        errors.append("prep2 job must gate on workers2-wall-merge.outputs.prep_should_run (I1)")
    errors.extend(foreman_run_download_lax(text))
    errors.extend(worker_delta_download_lax(text))
    errors.extend(assemble_closeout_comment_wall_patch(text))
    errors.extend(post_comment_hard_has_gh_token(text))
    repo_root = Path(args.workflow).resolve().parent.parent.parent
    env_check = repo_root / ".github" / "workflows" / "env-check.yml"
    if env_check.is_file():
        env_text = env_check.read_text(encoding="utf-8")
        errors.extend(post_comment_hard_has_gh_token(env_text))
        if re.compile(r"env_check_wall\.py[^\n]*\|\|\s*true").search(env_text):
            errors.append("env_check_wall must not use || true (W3 fail-closed)")
    for m in re.finditer(r"- name: Upload verdict(?: round 2)? artifact", text):
        chunk = text[m.start() : m.start() + 180]
        if re.search(r"if:\s*always\(\)", chunk):
            errors.append("validate upload uses if: always() without wall gate")
    if errors:
        print("lint failures:", *errors, sep="\n", file=sys.stderr)
        return 1
    print("workflow foreman lint ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
