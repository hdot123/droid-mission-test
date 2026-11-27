"""fix-verify-marker-interaction: the verify marker judged by CONTENT, the
cancelled path preserved, one shared verdict module.

a6f81cf gave the verify steps if: always(). Three interactions broke, each
pinned here at the seam where only a workflow-level test can see it:

- BLK-1: the verify step writes checks-failed.marker whenever problems is
  non-empty, and missing handoff/status alone makes it non-empty even when
  every card check exits 0. The salvage guard and the adopt gate used to
  refuse any pack carrying the marker — the r58 death shape (machine-green
  work, session killed before the two evidence files) became unsalvageable.
  The design ruling: the marker is the worker-side verify record, prep's own
  checks-exit.json is the green authority — every consumer classifies the
  marker by CONTENT (marker_verdict.py): non-zero check exit, a
  malformed-status problem, or unreadable bytes = red; missing-file-only
  problems = not red.
- BLK-2: always() also runs on job cancellation. A verify marker on the 25m
  job-wall path used to flip the delta step's RESULT failure, turning
  cancelled/job_wall_cancelled/cancel_reason=job_wall_25m into
  failure/wall_killed and re-opening prep. The verify guard gains
  !cancelled(); the delta step ranks cancelled above the marker; the delta
  CLI does the same. The cancelled chain is driven here through the step's
  REAL shell logic (extracted from team.yml), not a re-implementation.
- the delta-step RESULT override ordering pin: the marker line must stay
  behind (and guarded by) the cancelled branch, whichever runs first.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from foreman_run_lib import (  # noqa: E402
    init_wall,
    prep_should_run,
    save_wall,
    validate_with_jsonschema,
)
from lint_workflow_wall_exits import job_spans, step_chunks  # noqa: E402
from merge_worker_deltas import apply_deltas  # noqa: E402
from marker_verdict import (  # noqa: E402
    marker_problems,
    marker_red_detail,
    marker_verdict_red,
    write_marker,
)

TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"
FIXTURE = ROOT / "tests" / "fixtures" / "worker-r58d"
PID = "hslconv"

WALL_KILLED_DELTA = json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text())

# The exact bytes the real verify step writes for the r58 death shape
# (scrutiny SV-1): green checks + the two missing evidence files. A
# missing-file-only marker is NOT red — checks-exit.json is the authority.
GREEN_MISSING_MARKER = (
    f"process: {PID}\n"
    "check exit 0: python3 -m pytest tests/test_hslconv.py -q\n"
    "check exit 0: python3 -m pytest tests/ -q\n"
    f"problem: missing expected file: team/handoffs/{PID}.md\n"
    f"problem: missing expected file: team/status/{PID}.json\n"
)
RED_CHECK_MARKER = (
    f"process: {PID}\n"
    "check exit 0: python3 -m pytest tests/test_hslconv.py -q\n"
    "check exit 1: python3 -m pytest tests/ -q\n"
    "problem: check failed (exit 1): python3 -m pytest tests/ -q\n"
)
MALFORMED_STATUS_MARKER = (
    f"process: {PID}\n"
    "check exit 0: python3 -m pytest tests/test_hslconv.py -q\n"
    "problem: status file is not valid JSON: Expecting value: line 1 column 1\n"
    f"problem: missing expected file: team/handoffs/{PID}.md\n"
)

VERIFY_STEP_NAMES = {
    "worker": "Verify process checks and handoff",
    "worker2": "Verify process checks and handoff",
}
DELTA_STEP_NAMES = {
    "worker": "Record worker delta for ForemanRun (W1 matrix)",
    "worker2": "Record worker2 delta for ForemanRun",
}


def _job_text(yml: str, job: str) -> str:
    spans = job_spans(yml)
    start, end = spans[job]
    return yml[start:end]


def _step_chunk(job: str, step_name: str) -> str:
    text = TEAM_YML.read_text(encoding="utf-8")
    for chunk in step_chunks(_job_text(text, job)):
        if f"name: {step_name}" in chunk:
            return chunk
    raise AssertionError(f"step {step_name!r} not found in job {job}")


def _shell_run_block(job: str, step_name: str) -> str:
    """A step's `run: |` block, dedented to a runnable shell script."""
    lines = _step_chunk(job, step_name).splitlines()
    i = next(i for i, ln in enumerate(lines) if ln.strip() == "run: |")
    body = lines[i + 1:]
    return "\n".join(ln[10:] if ln.startswith(" " * 10) else ln for ln in body)


# --- BLK-1: marker verdict by content -----------------------------------------


def test_green_checks_missing_files_marker_is_not_red():
    """The r58 anchor shape's own marker: both check exits 0, problems are
    only the missing evidence files. Not red — this exact shape must be
    salvageable (BLK-1)."""
    assert marker_verdict_red(GREEN_MISSING_MARKER) is False
    kinds = [p["kind"] for p in marker_problems(GREEN_MISSING_MARKER)]
    assert kinds == ["missing_file", "missing_file"]
    assert all(f"{PID}" in p["text"] for p in marker_problems(GREEN_MISSING_MARKER))


def test_nonzero_check_exit_marker_is_red():
    assert marker_verdict_red(RED_CHECK_MARKER) is True
    reds = [p for p in marker_problems(RED_CHECK_MARKER) if p["kind"] == "red_check"]
    assert len(reds) == 1 and reds[0]["exit"] == 1
    assert "exit 1" in marker_red_detail(RED_CHECK_MARKER)


def test_malformed_status_problem_marker_is_red():
    assert marker_verdict_red(MALFORMED_STATUS_MARKER) is True
    kinds = [p["kind"] for p in marker_problems(MALFORMED_STATUS_MARKER)]
    assert "malformed_status" in kinds
    assert "missing_file" in kinds


@pytest.mark.parametrize(
    "text",
    [
        "",
        "junk that is not a marker at all",
        "process: x\nno recognizable lines follow\n",
        "process: x\nproblem: some unrecognized red flag\n",
        None,
    ],
)
def test_unreadable_or_unrecognized_marker_is_red_fail_closed(text):
    """Fail-closed: marker bytes that cannot prove their entries green read
    as red, never as a pass-through."""
    assert marker_verdict_red(text) is True


def test_negative_check_exit_is_red():
    text = f"process: {PID}\ncheck exit -1: cmd\n"
    assert marker_verdict_red(text) is True
    assert marker_red_detail(text).startswith("check exit -1")


def test_exit_127_check_line_is_red_here():
    """The adopt-side 127 exception lives in checks-exit.json's gate, not in
    the marker's: a marker only exists when the worker's verify itself
    recorded problems, and a 127 check line in it is a red verify fact."""
    text = f"process: {PID}\ncheck exit 127: pytest -q\nproblem: x\n"
    assert marker_verdict_red(text) is True


def test_write_marker_roundtrips_through_the_verdict():
    """The verify step's writer and every consumer's classifier share the
    same format: what write_marker produces parses back into exactly the
    problems that went in."""
    check_results = [
        ("python3 -m pytest tests/test_hslconv.py -q", 0),
        ("python3 -m pytest tests/ -q", 0),
    ]
    problems = [
        f"missing expected file: team/handoffs/{PID}.md",
        f"missing expected file: team/status/{PID}.json",
    ]
    text = write_marker(PID, check_results, problems)
    assert text.startswith(f"process: {PID}\n")
    assert marker_verdict_red(text) is False
    kinds = [p["kind"] for p in marker_problems(text)]
    assert kinds == ["missing_file", "missing_file"]

    red_results = [("pytest tests/ -q", 1)]
    red_problems = ["check failed (exit 1): pytest tests/ -q"]
    red_text = write_marker(PID, red_results, red_problems)
    assert marker_verdict_red(red_text) is True
    assert "exit 1" in marker_red_detail(red_text)


# --- BLK-1: the workflow's verify steps write through the module --------------


@pytest.mark.parametrize("job", ["worker", "worker2"])
def test_verify_step_writes_marker_through_module(job):
    chunk = _step_chunk(job, VERIFY_STEP_NAMES[job])
    # CI import fidelity: the heredoc seeds scripts/team itself (the r58
    # scrutiny round-1 blocking class of defect).
    assert 'os.path.join(os.environ.get("GITHUB_WORKSPACE", "."), "scripts", "team")' in chunk
    assert "from marker_verdict import write_marker" in chunk
    assert "write_marker(" in chunk
    # the step no longer hand-writes the marker lines
    assert 'fh.write(f"process: {proc[' + "'id'" + ']}\\n")' not in chunk
    # v2.6.3 semantics unchanged: missing deliverables are still recorded,
    # the legacy marker name still travels the commit step unchanged
    assert "missing expected file" in chunk
    assert "checks-failed.marker" in chunk


# --- BLK-2: the cancelled path stays byte-identical ---------------------------


@pytest.mark.parametrize("job", ["worker", "worker2"])
def test_verify_step_guard_excludes_cancelled(job):
    chunk = _step_chunk(job, VERIFY_STEP_NAMES[job])
    assert "if: always() && !cancelled()" in chunk, (
        f"{job}: verify must run after a failed session step but never on "
        "the cancelled path (BLK-2)"
    )


@pytest.mark.parametrize("job", ["worker", "worker2"])
def test_delta_step_marker_override_spares_cancelled(job):
    shell = _shell_run_block(job, DELTA_STEP_NAMES[job])
    cancelled_line = 'if [ "$JOB_STATUS" = "cancelled" ]; then RESULT="cancelled"; fi'
    marker_line = (
        'if [ "$RESULT" != "cancelled" ] && '
        '[ -f "team/status/${PROCESS_ID}.checks-failed.marker" ]; then RESULT="failure"; fi'
    )
    assert cancelled_line in shell
    assert marker_line in shell
    assert shell.index(cancelled_line) < shell.index(marker_line), (
        "the cancelled branch must be judged before the marker override"
    )
    # the delta CLI's own ordering must match: cancelled ranks above the
    # marker (the step's --result already encodes it, and a direct CLI call
    # with JOB_STATUS=cancelled behaves the same)
    cli = (ROOT / "scripts" / "team" / "write_worker_delta.py").read_text(encoding="utf-8")
    assert 'args.result != "cancelled"' in cli
    assert cli.index('args.result != "cancelled"') < cli.index("checks-failed.marker")


def _stage_delta_ws(tmp_path: Path, job: str, *, marker: bool) -> Path:
    """A runner-shaped workspace for the delta step: scripts/team, the
    worker stream, and (optionally) the verify marker."""
    ws = tmp_path / f"ws-{job}" / ("marker" if marker else "clean")
    ws.mkdir(parents=True)
    shutil.copytree(
        ROOT / "scripts" / "team",
        ws / "scripts" / "team",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    shutil.copy(FIXTURE / "worker-stream.jsonl", ws / "worker-stream.jsonl")
    if marker:
        marker_dir = ws / "team" / "status"
        marker_dir.mkdir(parents=True)
        (marker_dir / f"{PID}.checks-failed.marker").write_text(
            GREEN_MISSING_MARKER, encoding="utf-8"
        )
    return ws


@pytest.mark.parametrize("job", ["worker", "worker2"])
def test_cancelled_job_with_marker_keeps_cancel_chain(tmp_path, job):
    """BLK-2 driven through the step's REAL shell logic: a verify marker on
    disk + JOB_STATUS=cancelled must record cancelled / job_wall_cancelled /
    cancel_reason=job_wall_25m, keep the pid in cancelled_pids (not
    completed_pids), and keep prep closed — the pre-a6f81cf chain,
    byte for byte."""
    import re

    ws = _stage_delta_ws(tmp_path, job, marker=True)
    script = ws / "delta-step.sh"
    script.write_text(_shell_run_block(job, DELTA_STEP_NAMES[job]), encoding="utf-8")
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith("GITHUB_") and k not in ("JOB_STATUS", "PYTHONPATH")
    }
    env["PATH"] = os.pathsep.join([str(Path(sys.executable).parent), env.get("PATH", "")])
    env["JOB_STATUS"] = "cancelled"
    env["DROID_EXIT_CODE"] = "143"
    env["PROCESS_ID"] = PID
    proc = subprocess.run(
        ["bash", str(script)], cwd=ws, env=env, capture_output=True, text=True, timeout=60
    )
    assert proc.returncode == 0, f"delta step failed:\n{proc.stdout}\n{proc.stderr}"
    assert "delta:" in proc.stdout
    delta = json.loads((ws / "worker-delta.json").read_text(encoding="utf-8"))
    assert delta["result"] == "cancelled"
    assert delta["session_outcome"] == "job_wall_cancelled"
    assert delta["cancel_reason"] == "job_wall_25m"
    assert delta["droid_exit_code"] == 143

    wall = apply_deltas(init_wall(run_id="blk2", issue_number=929), [delta])
    workers = wall["workers"]
    assert workers["cancelled_pids"] == [PID]
    assert workers["completed_pids"] == []
    assert workers["cancel_reason_by_pid"] == {PID: "job_wall_25m"}
    assert workers["session_outcome_by_pid"][PID] == "job_wall_cancelled"
    assert workers["any_cancelled"] is True
    assert prep_should_run(wall) is False
    assert not validate_with_jsonschema(wall), validate_with_jsonschema(wall)


@pytest.mark.parametrize("job", ["worker", "worker2"])
def test_cancelled_job_without_marker_unchanged(tmp_path, job):
    """The no-marker cancelled shape is the pre-guard baseline: identical
    chain (guard against accidental drift while fixing the marker case)."""
    ws = _stage_delta_ws(tmp_path, job, marker=False)
    script = ws / "delta-step.sh"
    script.write_text(_shell_run_block(job, DELTA_STEP_NAMES[job]), encoding="utf-8")
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith("GITHUB_") and k not in ("JOB_STATUS", "PYTHONPATH")
    }
    env["PATH"] = os.pathsep.join([str(Path(sys.executable).parent), env.get("PATH", "")])
    env["JOB_STATUS"] = "cancelled"
    env["DROID_EXIT_CODE"] = "143"
    env["PROCESS_ID"] = PID
    proc = subprocess.run(
        ["bash", str(script)], cwd=ws, env=env, capture_output=True, text=True, timeout=60
    )
    assert proc.returncode == 0, proc.stderr
    delta = json.loads((ws / "worker-delta.json").read_text(encoding="utf-8"))
    assert delta["result"] == "cancelled"
    assert delta["session_outcome"] == "job_wall_cancelled"
    wall = apply_deltas(init_wall(run_id="blk2c", issue_number=929), [delta])
    assert wall["workers"]["cancelled_pids"] == [PID]
    assert prep_should_run(wall) is False


def test_failure_job_with_marker_still_records_wall_killed(tmp_path):
    """The v2.6.3 semantics the marker override exists for are unchanged: a
    red-checks job failure (marker on disk, JOB_STATUS=failure) still
    records failure/wall_killed through the same shell logic."""
    job = "worker"
    ws = _stage_delta_ws(tmp_path, job, marker=True)
    script = ws / "delta-step.sh"
    script.write_text(_shell_run_block(job, DELTA_STEP_NAMES[job]), encoding="utf-8")
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith("GITHUB_") and k not in ("JOB_STATUS", "PYTHONPATH")
    }
    env["PATH"] = os.pathsep.join([str(Path(sys.executable).parent), env.get("PATH", "")])
    env["JOB_STATUS"] = "failure"
    env["DROID_EXIT_CODE"] = "124"
    env["PROCESS_ID"] = PID
    proc = subprocess.run(
        ["bash", str(script)], cwd=ws, env=env, capture_output=True, text=True, timeout=60
    )
    assert proc.returncode == 0, proc.stderr
    delta = json.loads((ws / "worker-delta.json").read_text(encoding="utf-8"))
    assert delta["result"] == "failure"
    assert delta["session_outcome"] == "wall_killed"
    assert "cancel_reason" not in delta
    wall = apply_deltas(init_wall(run_id="blk2f", issue_number=929), [delta])
    workers = wall["workers"]
    assert workers["completed_pids"] == [PID]
    assert workers["cancelled_pids"] == []
    assert prep_should_run(wall) is True
