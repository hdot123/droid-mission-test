"""VAL-M3-003/004 replay: round-52 wall ledgers must tell the stitch truth.

Fixtures provenance (read-only sources, copied verbatim):
- tests/fixtures/lead_plan_segments/r52{A,B,C,D}/ — real round-52 lead streams
  (runs 45078438609 / 45078468896 / 45078521269 / 45078564505), extracted with
  tests/fixtures/extract_lead_segments.py (same tool that built the r51 set).
- tests/fixtures/foreman_wall_r52/foreman-run-C.json — the final foreman-run
  wall of run 45078521269 exactly as uploaded by the live round-52 C order,
  carrying the two ledger defects under test: an empty plan slice (the
  stitch log said shape=complete while chain.lead's detail recorded
  lead_plan_output_shape=unknown) and a stale replan_gate.should_replan=true
  left over from round 1 after round 2 absorbed the loop.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

import compute_replan_gate  # noqa: E402
from compute_replan_gate import compute  # noqa: E402
from foreman_run_lib import deep_merge, init_wall, save_wall  # noqa: E402
from lead_plan_segments import (  # noqa: E402
    cmd_stitch,
    scan_segments,
    stitch_plan_file,
)

FIXTURES = ROOT / "tests" / "fixtures" / "lead_plan_segments"
WALL_FIXTURE = ROOT / "tests" / "fixtures" / "foreman_wall_r52" / "foreman-run-C.json"
R52_ORDERS = ("r52A", "r52B", "r52C", "r52D")


def _prepare_workdir(tag: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    work = tmp_path / tag
    shutil.copytree(FIXTURES / tag / "team", work / "team")
    wall = init_wall(run_id=tag, issue_number=52)
    wall_path = work / "foreman-run.json"
    save_wall(wall, wall_path)
    monkeypatch.chdir(work)
    monkeypatch.setattr("lead_plan_segments.SEGMENTS_DIR", work / "team" / "lead-plan-segments")
    monkeypatch.setattr("lead_plan_segments.PLAN_PATH", work / "team-plan.json")
    return wall_path


@pytest.mark.parametrize("tag", R52_ORDERS)
def test_r52_stitch_writes_matching_wall_slice(tmp_path, monkeypatch, tag):
    """The stitch step records the plan slice it just proved in the log.

    Round 52 ran stitch with shape=complete in the job log, yet every wall
    ended with no plan slice, so the lead close-out detail read
    lead_plan_output_shape=unknown. The stitch step is the truth side: it
    must patch the wall with the same scan the log line prints.
    """
    wall_path = _prepare_workdir(tag, tmp_path, monkeypatch)
    scan = scan_segments()
    assert scan.errors == ()
    assert scan.shape == "complete"

    assert cmd_stitch(wall_path) == 0

    wall = json.loads(wall_path.read_text(encoding="utf-8"))
    plan_slice = wall.get("plan") or {}
    assert plan_slice.get("output_shape") == "complete", plan_slice
    assert plan_slice.get("schema_version") == "lead-plan-slice.v1"
    assert plan_slice.get("segment_files") == sorted(scan.segment_files)
    assert plan_slice.get("process_segment_count") == len(scan.processes)
    assert plan_slice.get("has_header_segment") is True
    assert plan_slice.get("segment_errors") == []
    outcome = ((wall.get("budgets") or {}).get("session_outcome") or {})
    assert outcome.get("plan_output_shape") == "complete"


def test_r52_stitch_cli_writes_wall(tmp_path, monkeypatch):
    """CLI parity: `lead_plan_segments stitch --wall <wall>` patches the wall."""
    wall_path = _prepare_workdir("r52C", tmp_path, monkeypatch)
    argv = ["lead_plan_segments", "stitch", "--wall", str(wall_path)]
    monkeypatch.setattr(sys, "argv", argv)
    import lead_plan_segments as lps

    assert lps.main() == 0
    wall = json.loads(wall_path.read_text(encoding="utf-8"))
    assert (wall.get("plan") or {}).get("output_shape") == "complete"


def test_lead_closeout_detail_no_longer_reads_unknown(tmp_path, monkeypatch):
    """The detail expression's source field exists after the stitch step.

    This pins the contract team.yml's lead close-out step relies on: the
    wall's plan.output_shape is populated by the time wall_sync_job records
    the lead seat, so the recorded detail can never be 'unknown' again.
    """
    wall_path = _prepare_workdir("r52A", tmp_path, monkeypatch)
    assert cmd_stitch(wall_path) == 0
    wall = json.loads(wall_path.read_text(encoding="utf-8"))
    shape = (wall.get("plan") or {}).get("output_shape", "unknown")
    assert shape != "unknown"
    detail = f"lead_plan_output_shape={shape}"
    assert detail == "lead_plan_output_shape=complete"


def test_c_wall_final_gate_overrides_stale_true():
    """VAL-M3-004: the round-2 rerun overwrites the stale round-1 gate.

    The live C wall (fixture copied verbatim) still carries
    should_replan=true from round 1 after round 2 passed cleanly. The
    terminal gate recomputation must clear it from that same wall.
    """
    wall = json.loads(WALL_FIXTURE.read_text(encoding="utf-8"))
    assert wall["replan_gate"]["should_replan"] is True, "fixture must carry the live defect"
    # The wall's validation slice is already round 2's (adoption ok, overall
    # pass) — the gate simply predates that update and was never recomputed.
    assert (wall.get("validation") or {}).get("round") == 2
    assert (wall.get("validation") or {}).get("overall") == "pass"

    gate = compute_replan_gate.compute(wall, round_num=2)["replan_gate"]
    assert gate["should_replan"] is False
    assert gate["round"] == 2
    assert gate["reasons"] == []


def test_round1_gate_shape_unchanged_and_lint_clean():
    """Single-round behavior is untouched."""
    assert compute_replan_gate._TERMINAL_ROUND == 2
    wall = init_wall(run_id="r1", issue_number=1)
    wall = deep_merge(
        wall,
        {
            "validation": {
                "adoption_status": "ok",
                "overall": "fail",
                "failed_process_ids": ["dijkstra"],
                "unattributed_failure": False,
            },
            "artifacts": {"team-verdict-issue-1-run-r1": {"complete": True}},
            "chain": {"validate": {"result": "success"}},
        },
    )
    gate = compute(wall)["replan_gate"]
    assert gate["should_replan"] is True
    assert gate["reasons"] == ["overall_not_pass"]
    assert "round" not in gate


def test_terminal_gate_requires_final_verdict_present():
    """Fail-closed: validate2 killed before adoption never clears the gate.

    A wall whose validation slice is still round 1 (adopt2 never ran) must
    raise on a terminal-round recomputation instead of silently re-writing
    the gate from stale inputs. When the round-2 slice exists, the verdict
    artifact gate alone keeps should_replan honest (no raise needed).
    """
    wall = json.loads(WALL_FIXTURE.read_text(encoding="utf-8"))
    # Round-2 slice present but its verdict artifact missing: the
    # verdict-complete input gates should_replan to False.
    missing = json.loads(WALL_FIXTURE.read_text(encoding="utf-8"))
    del missing["artifacts"]["team-verdict2-issue-763-run-45078521269"]
    gate = compute_replan_gate.compute(missing, round_num=2)["replan_gate"]
    assert gate["should_replan"] is False

    # adopt2 never wrote the round-2 slice: refuse to recompute.
    stale_input = json.loads(WALL_FIXTURE.read_text(encoding="utf-8"))
    stale_input["validation"] = {
        "schema_version": "validation-slice.v1",
        "round": 1,
        "adoption_status": "ok",
        "overall": "fail",
        "failed_process_ids": ["tapcode"],
        "unattributed_failure": False,
        "pytest_exit": 1,
    }
    with pytest.raises(compute_replan_gate.StaleGateError):
        compute_replan_gate.compute(stale_input, round_num=2)
