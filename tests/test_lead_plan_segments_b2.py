"""B2: lead plan segmented persistence — partial vs none, equivalence, no stream salvage."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from foreman_run_lib import init_wall, save_wall  # noqa: E402
from lead_plan_segments import (  # noqa: E402
    assemble_plan_dict,
    cmd_assert_ready,
    cmd_sync_wall,
    plans_core_equivalent,
    scan_segments,
)
import lead_plan_segments as lps  # noqa: E402


def _write_header(seg_dir: Path, summary: str = "summary") -> None:
    seg_dir.mkdir(parents=True, exist_ok=True)
    (seg_dir / "00-header.json").write_text(
        json.dumps(
            {"schema_version": "lead-plan-segment.v1", "kind": "header", "summary": summary},
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def _write_process(seg_dir: Path, pid: str) -> None:
    seg_dir.mkdir(parents=True, exist_ok=True)
    proc = {
        "id": pid,
        "title": "t",
        "scope": "s",
        "files": ["a.py"],
        "task": "do",
        "checks": ["true"],
    }
    (seg_dir / f"process-{pid}.json").write_text(
        json.dumps(
            {"schema_version": "lead-plan-segment.v1", "kind": "process", "process": proc},
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def test_scan_none_when_empty(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    scan = scan_segments(segments_dir=tmp_path / "team/lead-plan-segments")
    assert scan.shape == "none"
    assert scan.segment_files == ()


def test_scan_partial_with_header_only(tmp_path: Path, monkeypatch):
    seg = tmp_path / "team/lead-plan-segments"
    _write_header(seg)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    scan = scan_segments(segments_dir=seg)
    assert scan.shape == "partial"
    assert scan.header is not None
    assert scan.processes == ()


def test_assert_ready_partial_records_wall_and_fails(tmp_path: Path, monkeypatch):
    seg = tmp_path / "team/lead-plan-segments"
    _write_header(seg)
    _write_process(seg, "alpha")
    wall = init_wall(run_id="b2p", issue_number=1)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    monkeypatch.setattr(lps, "PLAN_PATH", tmp_path / "team-plan.json")

    assert cmd_assert_ready(wall_path) == 1
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    assert synced["plan"]["output_shape"] == "partial"
    assert synced["plan"]["process_segment_count"] == 1
    assert synced["chain"]["lead"]["result"] == "unknown"


def test_assert_ready_none_fails(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cmd_assert_ready(None) == 1


def test_normal_path_equivalent_to_segments(tmp_path: Path, monkeypatch):
    seg = tmp_path / "team/lead-plan-segments"
    _write_header(seg, "ship it")
    _write_process(seg, "alpha")
    _write_process(seg, "beta")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    plan_path = tmp_path / "team-plan.json"
    monkeypatch.setattr(lps, "PLAN_PATH", plan_path)
    assembled = assemble_plan_dict(scan_segments(segments_dir=seg))
    assert assembled is not None
    plan = dict(assembled)
    plan["plan_version"] = 1
    plan["iteration"] = 1
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    scan = scan_segments(segments_dir=seg)
    assert scan.shape == "complete"
    assert plans_core_equivalent(json.loads(plan_path.read_text()), assembled)
    assert cmd_assert_ready(None) == 0


def test_sync_wall_session_outcome_shape(tmp_path: Path, monkeypatch):
    seg = tmp_path / "team/lead-plan-segments"
    _write_header(seg)
    wall = init_wall(run_id="b2s", issue_number=2)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    assert cmd_sync_wall(wall_path, "lead") == 0
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    assert synced["budgets"]["session_outcome"]["plan_output_shape"] == "partial"


def test_stream_salvage_module_removed():
    salvage_path = ROOT / "scripts" / "team" / "lead_plan_checkpoint.py"
    assert not salvage_path.is_file(), "lead_plan_checkpoint.py stream salvage must be deleted"


def test_lead_session_timeout_partial_shape_on_wall(tmp_path: Path, monkeypatch):
    import run_droid_session  # noqa: E402

    seg = tmp_path / "team/lead-plan-segments"
    _write_header(seg, "partial run")
    _write_process(seg, "only-one")
    wall = init_wall(run_id="b2kill", issue_number=99)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    monkeypatch.setattr(lps, "PLAN_PATH", tmp_path / "team-plan.json")
    run_droid_session._patch_session_outcome(wall_path, role="lead", exit_code=124)
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    assert synced["budgets"]["session_outcome"]["completion_status"] == "timeout"
    assert synced["budgets"]["session_outcome"]["plan_output_shape"] == "partial"