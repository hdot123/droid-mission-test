"""Scrutiny round-1 blocking fixes (m1-scrutiny-fixes): the revalidate chain
must actually work end to end.

Scrutiny synthesis (validation/m1-three-prs/scrutiny/synthesis.json) proved by
execution that the PR-1 chain could never fire and that a FIRST timeout still
terminated the order (PR1-0..PR1-4, PR1-6; PR2-1 torn drafts; PR2-2/2b
check-summary). This file pins the library-level semantics on the REAL
adopt() -> compute_replan_gate() -> derive() sequence — no hand-built wall
states for the behavior under test (scrutiny reviewProcessNote: every PR-1
defect passed tests that exercised hand-built walls):

- first draft_timeout: should_revalidate=true and the attempt marker is NOT
  stamped (requesting a retry is not an attempt — the revalidate job stamps
  the marker when it actually starts), and derive() keeps human_stop off;
- only after the marker is stamped does a second draft_timeout terminate
  fail-closed with human_stop;
- the needs-reference lint refuses undeclared outputs / needs entries
  (PR1-0 / PR1-4 are invisible to string-presence tests).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from adopt_verdict import adopt  # noqa: E402
from compute_replan_gate import compute  # noqa: E402
from compute_validate_conclusion import derive  # noqa: E402
from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402

PIDS = ["damm", "easterorthodox", "graph"]


def _minimal_work(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text(json.dumps({"pytest_exit": 0}), encoding="utf-8")
    (work / "plan.json").write_text(
        json.dumps({"processes": [{"id": pid} for pid in PIDS]}), encoding="utf-8"
    )
    (work / "judgeable.json").write_text(json.dumps(PIDS), encoding="utf-8")
    (work / "blocked.json").write_text("{}", encoding="utf-8")
    return work


# --- PR1-2: requesting a retry is not an attempt -----------------------------


def test_first_timeout_keeps_attempt_marker_unstamped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="scr-a", issue_number=812), wall_path)
    work = _minimal_work(tmp_path)

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    assert rc == 0
    gate = json.loads(wall_path.read_text(encoding="utf-8"))["replan_gate"]
    assert gate["should_revalidate"] is True
    assert not gate.get("revalidate_run_started")


def test_second_timeout_after_run_started_is_human_stop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The revalidate job stamps revalidate_run_started when it actually
    starts; a draft_timeout on top of that marker is the terminal second
    failure (fail-closed)."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    wall = init_wall(run_id="scr-b", issue_number=812)
    wall["replan_gate"] = {
        "schema_version": "replan-gate.v1",
        "should_replan": False,
        "should_revalidate": True,
        "revalidate_run_started": True,
    }
    save_wall(wall, wall_path)
    work = _minimal_work(tmp_path)

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_error"] == "draft_timeout"
    assert merged.get("human_stop") is True
    assert merged["replan_gate"]["should_revalidate"] is False


# --- PR1-3: whole-chain consistency (real adopt -> gate -> derive) -----------


def test_whole_chain_first_timeout_then_started_retry_then_human_stop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Drive the real adopt() -> compute_replan_gate() -> derive() sequence on
    the wall each step actually produces. First timeout: no human_stop on the
    wall derive() saves (the retry is pending). After the revalidate job
    starts (marker stamped) and the retry dies the same way: human_stop."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="scr-chain", issue_number=812), wall_path)
    work = _minimal_work(tmp_path)

    # validate job: session killed at the wall, nothing on disk
    adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    wall = json.loads(wall_path.read_text(encoding="utf-8"))
    assert wall["replan_gate"]["should_revalidate"] is True
    assert not wall["replan_gate"].get("revalidate_run_started")
    gate_wall = compute(wall, round_num=1)
    merged, conclusion = derive(gate_wall, round_num=1)
    assert conclusion == "failure"
    assert merged.get("human_stop") is not True
    validate_with_jsonschema(merged)

    # the revalidate job starts: stamp the marker exactly like the workflow
    # guard, then the retry session dies at the wall again
    wall = merged
    wall["replan_gate"]["revalidate_run_started"] = True
    save_wall(wall, wall_path)
    adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    wall2 = json.loads(wall_path.read_text(encoding="utf-8"))
    assert wall2.get("human_stop") is True
    assert wall2["replan_gate"]["should_revalidate"] is False
    gate2 = compute(wall2, round_num=1)
    merged2, conclusion2 = derive(gate2, round_num=1)
    assert conclusion2 == "failure"
    assert merged2.get("human_stop") is True
    validate_with_jsonschema(merged2)


def test_gate_mirrors_run_started_marker():
    """The gate slice carries the attempt marker under its one truth name so
    the workflow guard and the wall stay one truth."""
    wall = init_wall(run_id="scr-gate", issue_number=1)
    wall["replan_gate"] = {
        "schema_version": "replan-gate.v1",
        "should_replan": False,
        "should_revalidate": True,
        "revalidate_run_started": True,
    }
    gate = compute(wall, round_num=1)["replan_gate"]
    assert gate["revalidate_run_started"] is True


# --- PR1-4: needs-reference lint ---------------------------------------------

NEEDS_LINT = ROOT / "scripts" / "team" / "lint_workflow_needs.py"

DECLARED_WF = """\
jobs:
  first:
    runs-on: ubuntu-latest
    outputs:
      flag: ${{ steps.s.outputs.flag }}
    steps:
      - id: s
        run: echo flag=true >> "$GITHUB_OUTPUT"
  second:
    needs: first
    if: ${{ needs.first.outputs.flag == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo hi
"""


def _run_needs_lint(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(NEEDS_LINT), "--workflow", str(path)],
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_needs_lint_accepts_declared_workflow(tmp_path: Path):
    wf = tmp_path / "wf.yml"
    wf.write_text(DECLARED_WF, encoding="utf-8")
    r = _run_needs_lint(wf)
    assert r.returncode == 0, r.stdout + r.stderr


def test_needs_lint_rejects_undeclared_output(tmp_path: Path):
    wf = tmp_path / "wf.yml"
    wf.write_text(
        DECLARED_WF.replace(
            "needs.first.outputs.flag", "needs.first.outputs.absent_flag"
        ),
        encoding="utf-8",
    )
    r = _run_needs_lint(wf)
    assert r.returncode == 1
    assert "absent_flag" in (r.stdout + r.stderr)


def test_needs_lint_rejects_undeclared_needs_ref(tmp_path: Path):
    wf = tmp_path / "wf.yml"
    wf.write_text(
        DECLARED_WF.replace(
            "  second:\n    needs: first\n    if: ${{ needs.first.outputs.flag == 'true' }}",
            "  second:\n    needs: first\n    if: ${{ needs.unknown.outputs.flag == 'true' }}",
        ),
        encoding="utf-8",
    )
    r = _run_needs_lint(wf)
    assert r.returncode == 1
    assert "unknown" in (r.stdout + r.stderr)


def test_repo_workflow_passes_needs_lint():
    """The shipped workflow must have no undeclared needs output / needs
    reference (PR1-0 / PR1-4: undeclared references are fail-dead wiring)."""
    r = subprocess.run(
        [sys.executable, str(NEEDS_LINT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 0, r.stdout + r.stderr
