"""M3: single-source worker prompt template + verify-step guard.

The round-1 and round-2 worker prompts in team.yml were byte-identical
heredoc copies (the same L-4 disease the validator face was cured of by
validator_prompt_template.py). This file pins the single-source contract
and the two template additions this milestone makes:

- both session steps import build_worker_prompt from
  scripts/team/worker_prompt_template.py and the rendered prompt is
  byte-identical to the module (execution-level, like
  test_render_step_execution.py);
- every current discipline line survives verbatim ("Do not commit or
  push", the two team files, the checks instruction);
- NEW incremental-persistence guidance (P-2-capped wording, layer 2 of the
  cure: start by writing a status skeleton, update each file as each part
  completes) — P-2 verdict is that wording has no runtime force; its value
  is richer intermediate state for the M2 salvage packer;
- the "at most 20 tool calls" arithmetic cap is replaced by I-1-style
  milestone-ordering wording (per the V-3 report: an arithmetic question
  is one more decision the model reasons over, not a limit);
- the verify steps carry if: always() so a wall-killed session step no
  longer skips the job's machine re-check channel (r58: zero output lines
  from that step in the whole job log).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"

sys.path.insert(0, str(ROOT / "scripts" / "team"))

from lint_workflow_wall_exits import job_spans, step_chunks  # noqa: E402
from worker_prompt_template import build_worker_prompt  # noqa: E402

SESSION_STEPS = [
    # (job key, step name)
    ("worker", "Worker executes exactly one process card"),
    ("worker2", "Worker executes exactly one process card (round 2)"),
]
VERIFY_STEPS = [
    ("worker", "Verify process checks and handoff"),
    ("worker2", "Verify process checks and handoff"),
]

# A minimal card with the shapes the r58 heredoc exercised (no retry note).
CARD = {
    "id": "hslconv",
    "title": "RGB ↔ HSL 颜色换算组件与测试",
    "sub_issue_number": 939,
    "files": ["hslconv.py", "tests/test_hslconv.py"],
    "checks": [
        "python3 -m pytest tests/test_hslconv.py -q",
        "python3 -m pytest tests/ -q",
    ],
}
RETRY_CARD = {**CARD, "retry_note": "Verdict blocked this process with reason 'test'."}


# --- team.yml extraction helpers ---------------------------------------------


def _job_text(yml: str, job_key: str) -> str:
    spans = job_spans(yml)
    assert job_key in spans, f"job {job_key} missing"
    start, end = spans[job_key]
    return yml[start:end]


def _step_text(job_text: str, step_name: str) -> str:
    for chunk in step_chunks(job_text):
        if f"name: {step_name}" in chunk:
            return chunk
    raise AssertionError(f"step {step_name!r} not found")


def _run_block(step_text: str) -> str:
    m = re.search(r"^        run: \|\n((?:          .*\n?|\n)*)", step_text, re.MULTILINE)
    assert m, "run: | block missing"
    return "\n".join(
        ln[10:] if ln.startswith(" " * 10) else ln for ln in m.group(1).splitlines()
    )


def _render_from_step(job_key: str, step_name: str) -> bytes:
    """Execute the session step's real shell up to the droid launch and
    return the rendered worker-prompt.txt bytes (execution-level fidelity:
    the heredoc must run on its own, seeding its import path from
    GITHUB_WORKSPACE — the same CI-fidelity contract the validator render
    steps were held to in M2-2)."""
    yml = TEAM_YML.read_text(encoding="utf-8")
    run = _run_block(_step_text(_job_text(yml, job_key), step_name))
    assert "set +e" in run, "guard lost: cannot safely truncate before the session launch"
    script = run[: run.index("set +e")] + "\nexit 0\n"

    work = Path(tempfile.mkdtemp(prefix=f"worker-render-{job_key}-"))
    try:
        env = {
            k: v
            for k, v in os.environ.items()
            if k in ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR")
        }
        env["GITHUB_WORKSPACE"] = str(ROOT)  # a real runner variable
        env["GITHUB_OUTPUT"] = str(work / "gh-output.txt")
        # the step's own env block injects these from the runner; the
        # harness supplies them the same way (the event file carries the
        # work order the prompt embeds)
        event = {"issue": {"number": 929, "title": "第58轮 D 单", "body": ""}}
        (work / "event.json").write_text(json.dumps(event))
        env["GITHUB_EVENT_PATH"] = str(work / "event.json")
        env["PROCESS_JSON"] = json.dumps(CARD)
        env["ISSUE_NUMBER"] = "929"
        proc = subprocess.run(
            ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", script],
            cwd=str(work),
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert proc.returncode == 0, (
            f"{job_key}: render heredoc exited {proc.returncode}\nstderr:\n"
            f"{proc.stderr[-2000:]}"
        )
        return (work / "worker-prompt.txt").read_bytes()
    finally:
        shutil.rmtree(work, ignore_errors=True)


# --- VAL-M3-001: single-source template renders both rounds ------------------


@pytest.mark.parametrize(("job_key", "step_name"), SESSION_STEPS)
def test_session_step_imports_single_source_template(job_key, step_name):
    chunk = _step_text(_job_text(TEAM_YML.read_text(encoding="utf-8"), job_key), step_name)
    assert "from worker_prompt_template import" in chunk, (
        f"{job_key} must build its prompt from the single-source template module"
    )
    assert "build_worker_prompt" in chunk


@pytest.mark.parametrize(("job_key", "step_name"), SESSION_STEPS)
def test_rendered_prompt_matches_module_byte_for_byte(job_key, step_name):
    rendered = _render_from_step(job_key, step_name)
    expected = build_worker_prompt(CARD, issue_number=929, issue_title="第58轮 D 单").encode()
    assert rendered == expected, f"{job_key}: rendered prompt drifted from the module"


@pytest.mark.parametrize(("job_key", "step_name"), SESSION_STEPS)
def test_rendered_prompt_carries_retry_block_when_present(job_key, step_name):
    env_card = {**CARD, "retry_note": "Verdict blocked this process with reason 'test'."}
    yml = TEAM_YML.read_text(encoding="utf-8")
    run = _run_block(_step_text(_job_text(yml, job_key), step_name))
    script = run[: run.index("set +e")] + "\nexit 0\n"
    work = Path(tempfile.mkdtemp(prefix=f"worker-retry-{job_key}-"))
    try:
        env = {
            k: v
            for k, v in os.environ.items()
            if k in ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR")
        }
        env["GITHUB_WORKSPACE"] = str(ROOT)
        env["GITHUB_OUTPUT"] = str(work / "gh-output.txt")
        (work / "event.json").write_text(
            json.dumps({"issue": {"number": 929, "title": "T", "body": ""}})
        )
        env["GITHUB_EVENT_PATH"] = str(work / "event.json")
        env["PROCESS_JSON"] = json.dumps(env_card)
        env["ISSUE_NUMBER"] = "929"
        proc = subprocess.run(
            ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", script],
            cwd=str(work),
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert proc.returncode == 0, proc.stderr[-2000:]
        text = (work / "worker-prompt.txt").read_text(encoding="utf-8")
        assert "Retry context (this card was re-dispatched after validation):" in text
        assert "Verdict blocked this process with reason 'test'." in text
    finally:
        shutil.rmtree(work, ignore_errors=True)


def test_rounds_render_identically_for_same_card():
    r1 = build_worker_prompt(CARD, issue_number=929, issue_title="T")
    r2 = build_worker_prompt(CARD, issue_number=929, issue_title="T")
    assert r1 == r2


def test_prompt_preserves_current_discipline_lines():
    """The two team-file instructions, the checks instruction, and the
    standing discipline lines survive the migration verbatim."""
    text = build_worker_prompt(CARD, issue_number=929, issue_title="T")
    assert "Create or edit only these files: hslconv.py, tests/test_hslconv.py" in text
    assert "Also write exactly these two team files:" in text
    assert (
        "team/handoffs/hslconv.md — a self-contained handoff with: what was requested, "
        "what you did, what you did not do, checks you ran and their results, and "
        "anything the validator must pay attention to." in text
    )
    assert (
        'team/status/hslconv.json — valid JSON with keys: id, title, state ("done"), '
        "files (array), checks (array of objects with command and result)." in text
    )
    assert (
        "Run your process checks before finishing: "
        "python3 -m pytest tests/test_hslconv.py -q; python3 -m pytest tests/ -q" in text
    )
    assert (
        "Checks may run tests across the whole repo. Files like verdict.json or "
        "verdict.md that appear in the repo root because of those checks are pipeline "
        "by-products of the test suite, not your deliverables. They are outside your "
        "card, so delete them before finishing (e.g. rm -f verdict.json verdict.md)."
        in text
    )
    assert "Do not commit or push; the workflow will do that." in text
    assert "Do not modify files owned by other processes." in text
    assert "Execute exactly one process card" in text
    assert "Do not do any other process. Do not expand scope." in text
    assert "Work order: #929" in text


# --- VAL-M3-002: incremental persistence + milestone ordering ----------------


def test_prompt_carries_incremental_persistence_guidance():
    text = build_worker_prompt(CARD, issue_number=929, issue_title="T")
    assert "status skeleton" in text
    assert "before doing anything else" in text
    assert "update both team files as you complete each part" in text
    assert "do not leave both to the end" in text


def test_prompt_replaces_tool_call_cap_with_milestone_ordering():
    text = build_worker_prompt(CARD, issue_number=929, issue_title="T")
    assert "at most 20 tool calls" not in text
    assert "20 tool calls" not in text
    assert "Work through the card as an ordered sequence of milestones" in text
    assert "one tool call per milestone" in text
    assert "persist the completed part" in text


# --- the double heredoc must be gone -----------------------------------------


def test_legacy_inline_worker_heredoc_removed():
    yml = TEAM_YML.read_text(encoding="utf-8")
    assert "You are a WORKER on a development team" not in yml, (
        "the worker prompt f-string must live only in the template module now"
    )


# --- VAL-M3-003: verify step guard -------------------------------------------


@pytest.mark.parametrize(("job_key", "step_name"), VERIFY_STEPS)
def test_verify_step_runs_after_session_failure(job_key, step_name):
    chunk = _step_text(_job_text(TEAM_YML.read_text(encoding="utf-8"), job_key), step_name)
    assert "if: always()" in chunk, (
        f"{job_key}: verify step must run even when the session step was killed"
    )
    # the step's own v2.6.3 semantics are unchanged: it records problems in
    # the per-process marker instead of failing, so the machine re-check
    # channel produces evidence rather than killing the job
    assert "checks-failed.marker" in chunk
