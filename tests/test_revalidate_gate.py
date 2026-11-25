"""I-5 revalidate chain (round54-root-cure PR-1): a wall-killed validator no
longer terminates the whole order at the first draft_timeout.

Round-54 A/C death shape: the validator session hit the wall with NO draft and
NO salvage on disk; adopt_verdict recorded adoption_error=draft_timeout and
hard-patched human_stop=true — the order died with zero automatic recovery even
though the evidence pack was intact and a validator-only re-run (same
EXPECTED_MANIFEST_SHA, same pack) is a pure retry of one session.

The fix: adopt_verdict writes replan_gate.should_revalidate=true on the
draft_timeout/no-draft path (no human_stop, no closeout), and the gate gains a
should_revalidate field consumed by the revalidate job in team.yml. Fail-closed
stays intact: revalidate re-runs ONLY the validator, at most once (the job's
guard stamps revalidate_run_started when the session actually starts); a second
failure re-terminates with human_stop.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from adopt_verdict import adopt  # noqa: E402
from compute_replan_gate import compute  # noqa: E402
from compute_validate_conclusion import derive  # noqa: E402
from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402

PIDS = ["dijkstra", "nthprime", "windscale"]


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


# --- 54A/C replay: exit 124, no draft, no partial --------------------------


def test_draft_timeout_no_artifacts_writes_should_revalidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The exact 54A/C shape: exit 124, nothing on disk. The wall must carry
    replan_gate.should_revalidate=true instead of human_stop=true."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="r54a", issue_number=812), wall_path)
    work = _minimal_work(tmp_path)

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_error"] == "draft_timeout"
    assert merged.get("human_stop") is not True
    assert "closeout" not in merged
    gate = merged["replan_gate"]
    assert gate["should_revalidate"] is True
    assert gate["should_replan"] is False
    validate_with_jsonschema(merged)


@pytest.mark.parametrize("round_num", [1, 2])
def test_draft_timeout_revalidate_flag_on_both_rounds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, round_num: int
):
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id=f"r54r{round_num}", issue_number=812), wall_path)
    work = _minimal_work(tmp_path)

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=round_num)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["replan_gate"]["should_revalidate"] is True
    assert merged.get("human_stop") is not True


def test_draft_timeout_with_salvage_still_revalidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Partial salvage (< full coverage) is the same revalidate shape: the
    recovered conclusions survive on the verdict, but the round still asks for
    a validator-only re-run."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="r54s", issue_number=812), wall_path)
    work = _minimal_work(tmp_path)
    partial = {
        "salvage_schema_version": "validator-partial.v1",
        "round": 1,
        "analyzed_count": 1,
        "processes": [{"id": PIDS[0], "verdict": "pass", "reason": "aligned"}],
        "conflicts": [],
    }
    (work / "verdict-partial.json").write_text(json.dumps(partial), encoding="utf-8")

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_error"] == "draft_timeout"
    assert merged.get("human_stop") is not True
    assert merged["replan_gate"]["should_revalidate"] is True
    validate_with_jsonschema(merged)


# --- fail-closed: the second timeout still terminates ----------------------


def test_revalidate_already_used_second_failure_human_stop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """At most one revalidate: when the wall shows the revalidate already ran
    (attempt marker stamped by the revalidate job's guard), a second
    draft_timeout re-terminates fail-closed with human_stop."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    wall = init_wall(run_id="r54b2", issue_number=812)
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
    assert merged["closeout"]["run_must_fail"] is True
    validate_with_jsonschema(merged)


def test_revalidate_not_duplicated_after_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """A clean adoption clears the revalidate request: the gate must not keep
    should_revalidate=true after a successful adopt (the retry already
    happened; its verdict is the outcome)."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    wall = init_wall(run_id="r54ok", issue_number=812)
    wall["replan_gate"] = {
        "schema_version": "replan-gate.v1",
        "should_replan": False,
        "should_revalidate": True,
        "revalidate_run_started": True,
    }
    save_wall(wall, wall_path)
    work = _minimal_work(tmp_path)
    draft = {
        "processes": [
            {"id": pid, "verdict": "pass", "reason": "five artifacts line up"} for pid in PIDS
        ],
        "conflicts": [],
    }
    (work / "verdict-droid.json").write_text(json.dumps(draft), encoding="utf-8")
    (work / "verdict-droid.md").write_text("# report\n", encoding="utf-8")
    (work / "pytest-output.txt").write_text("190 passed in 3s\n", encoding="utf-8")

    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True, round_num=1)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "ok"
    gate = merged["replan_gate"]
    assert gate["should_revalidate"] is False
    assert gate["should_replan"] is False
    validate_with_jsonschema(merged)


# --- non-timeout failures stay terminal ------------------------------------


@pytest.mark.parametrize("adoption_error", ["missing_draft", "merge_skipped"])
def test_other_errors_still_human_stop(tmp_path, monkeypatch, adoption_error):
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id=f"r54x-{adoption_error}", issue_number=812), wall_path)
    work = _minimal_work(tmp_path)
    if adoption_error == "merge_skipped":
        rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=False, round_num=1)
    else:
        # judgeable non-empty + no draft + exit 0 lands missing_draft
        rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True, round_num=1)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_error"] == adoption_error
    assert merged.get("human_stop") is True


# --- gate field contract ---------------------------------------------------


def test_gate_compute_defaults_should_revalidate_false():
    """The gate slice always carries should_revalidate (schema/contract field),
    defaulting to false so a clean wall stays clean."""
    wall = init_wall(run_id="gdefault", issue_number=1)
    gate = compute(wall)["replan_gate"]
    assert gate["should_revalidate"] is False


def test_gate_should_revalidate_reached_terminal_round_overwrites(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Terminal recomputation (--round 2) keeps the current should_revalidate
    semantics: a round-2 revalidate request survives the recompute instead of
    being dropped by the terminal-overwrite path."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    wall = init_wall(run_id="gterm", issue_number=1)
    wall["validation"] = {
        "schema_version": "validation-slice.v1",
        "round": 2,
        "adoption_status": "failed",
        "adoption_error": "draft_timeout",
        "overall": "fail",
    }
    wall["replan_gate"] = {
        "schema_version": "replan-gate.v1",
        "should_replan": False,
        "should_revalidate": True,
        "revalidate_run_started": True,
    }
    wall["artifacts"]["team-verdict2-issue-1-run-gterm"] = {
        "complete": False,
        "missing": ["verdict.json"],
    }
    wall["chain"]["validate2"] = {**wall["chain"]["validate2"], "result": "failure"}
    save_wall(wall, wall_path)
    merged = compute(wall, round_num=2)
    gate = merged["replan_gate"]
    assert gate["should_revalidate"] is True
    assert gate["round"] == 2
    validate_with_jsonschema(merged)


# --- conclusion derivation: revalidate stays red but not terminal ----------


def test_draft_timeout_derive_failure_without_human_stop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """derive() keeps the validate job red on a draft_timeout (fail-closed) but
    must not hard-patch human_stop while the one revalidate retry is still
    available (the revalidate job has not stamped its start marker)."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    wall = init_wall(run_id="gderive", issue_number=1)
    wall["validation"] = {
        "adoption_status": "failed",
        "adoption_error": "draft_timeout",
    }
    wall["replan_gate"] = {
        "schema_version": "replan-gate.v1",
        "should_replan": False,
        "should_revalidate": True,
        "revalidate_run_started": False,
    }
    save_wall(wall, wall_path)
    merged, conclusion = derive(wall)
    assert conclusion == "failure"
    assert merged.get("human_stop") is not True
    validate_with_jsonschema(merged)


def test_draft_timeout_terminal_derive_sets_human_stop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Same derive() after the one revalidate was used and failed: terminal,
    human_stop patched as before."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="gderive2", issue_number=1), wall_path)
    work = _minimal_work(tmp_path)
    adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    wall = json.loads(wall_path.read_text(encoding="utf-8"))
    assert wall["replan_gate"]["should_revalidate"] is True
    # the revalidate ran and its adopt died the same way
    wall["replan_gate"]["revalidate_run_started"] = True
    save_wall(wall, wall_path)
    merged, conclusion = derive(wall, round_num=1)
    assert conclusion == "failure"
    assert merged.get("human_stop") is True
    validate_with_jsonschema(merged)
