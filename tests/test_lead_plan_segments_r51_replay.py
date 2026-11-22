"""Round-51 replay: segment-only lead output must reach the Validate read.

Fixtures under tests/fixtures/lead_plan_segments/r51{A,B,C,D} are the real
segment writes (header + one file per process card) extracted from the four
round-51 lead streams via extract_lead_segments.py. On the old double-write
path all four orders died at the assembly joint: A/C/D on the plan-vs-segments
equivalence gate, B additionally on id-vs-filename and card whitespace drift.
This file is the failing-first replay suite for the machine-assembly path:
team-plan.json is produced by stitching the segments alone, so the mines those
orders actually hit have no remaining trigger surface.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from foreman_run_lib import init_wall, save_wall  # noqa: E402
from lead_plan_segments import (  # noqa: E402
    cmd_assert_ready,
    scan_segments,
    stitch_plan_file,
)
import lead_plan_segments as lps  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "lead_plan_segments"
# Round-51 order B, exactly as produced live: process ids carry a -module
# suffix the filenames lack, and two cards' task text drifted in whitespace
# from the team-plan.json the lead also wrote. In segment-only mode the id is
# derived from the filename and the card body has a single source, so none of
# the three mines can fire; only the id gate can still speak, deterministically.
R51B_ID_MISMATCHES = ("dijkstra", "nthprime", "windscale")


def _fixture_dir(tag: str) -> Path:
    return FIXTURES / tag


def _unpack(tag: str, tmp_path: Path) -> Path:
    work = tmp_path / tag
    shutil.copytree(_fixture_dir(tag) / "team", work / "team")
    return work


def _prepare_workdir(work: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    wall = init_wall(run_id=work.name, issue_number=51)
    wall_path = work / "foreman-run.json"
    save_wall(wall, wall_path)
    monkeypatch.chdir(work)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", work / "team" / "lead-plan-segments")
    monkeypatch.setattr(lps, "PLAN_PATH", work / "team-plan.json")
    return wall_path


def _fixture_summary(tag: str) -> str:
    header = json.loads(
        (_fixture_dir(tag) / "team" / "lead-plan-segments" / "00-header.json").read_text(
            encoding="utf-8"
        )
    )
    return str(header["summary"])


@pytest.mark.parametrize("tag", ["r51A", "r51C", "r51D"])
def test_r51_acd_segment_only_replay(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, tag: str):
    """A/C/D real segments stitch to a valid plan; no gate-related death."""
    work = _unpack(tag, tmp_path)
    wall_path = _prepare_workdir(work, monkeypatch)

    scan = scan_segments(segments_dir=work / "team" / "lead-plan-segments")
    assert scan.errors == ()
    assert scan.shape == "complete"
    assert len(scan.processes) == 3

    assert stitch_plan_file(work / "team-plan.json") == "complete"
    plan = json.loads((work / "team-plan.json").read_text(encoding="utf-8"))
    assert plan["summary"] == _fixture_summary(tag)
    assert [p["id"] for p in plan["processes"]] == sorted(
        p["id"] for p in plan["processes"]
    )
    assert {p["id"] for p in plan["processes"]} == {
        name[len("process-") : -len(".json")]
        for name in scan.segment_files
        if name.startswith("process-")
    }
    for proc in plan["processes"]:
        for key in ("id", "title", "scope", "files", "task", "checks"):
            assert proc.get(key), f"{tag}: {proc.get('id')} missing {key}"
    # The stitched file carries no execution bookkeeping; Validate adds it.
    assert plan.get("plan_version") is None

    assert cmd_assert_ready(wall_path) == 0
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    assert synced["plan"]["output_shape"] == "complete"
    # The gate re-stitched from the same segments: content identical.
    on_disk = json.loads((work / "team-plan.json").read_text(encoding="utf-8"))
    assert on_disk["summary"] == plan["summary"]
    assert on_disk["processes"] == plan["processes"]


def test_r51b_triple_mine_segment_only_replay(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Order B's three mines: id mismatch, summary divergence, task drift.

    Only the id/filename gate survives by design; it fails deterministically
    naming the segment files to rename, never as a cross-artifact verdict.
    """
    work = _unpack("r51B", tmp_path)
    wall_path = _prepare_workdir(work, monkeypatch)
    seg_dir = work / "team" / "lead-plan-segments"

    scan = scan_segments(segments_dir=seg_dir)
    assert scan.errors, "id mismatch must still be reported"
    assert all("must match filename" in err for err in scan.errors)
    assert scan.processes == (), "mismatched cards must not enter the plan"

    # Deterministic report, not a gate verdict: each error names the file.
    reported = {err.split(":")[0] for err in scan.errors}
    assert reported == {f"process-{pid}.json" for pid in R51B_ID_MISMATCHES}

    assert cmd_assert_ready(wall_path) == 1
    assert not (work / "team-plan.json").exists(), "failed gate writes no plan"

    # Repair in the prescribed direction (rename to the derived id): the
    # card bodies are untouched — whitespace drift cannot matter because no
    # second artifact exists to compare against.
    for name in sorted(p.name for p in seg_dir.iterdir()):
        if not name.startswith("process-"):
            continue
        proc = json.loads((seg_dir / name).read_text(encoding="utf-8"))["process"]
        derived = name[len("process-") : -len(".json")]
        proc["id"] = derived
        (seg_dir / name).write_text(
            json.dumps(
                {"schema_version": "lead-plan-segment.v1", "kind": "process", "process": proc},
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
    assert stitch_plan_file(work / "team-plan.json") == "complete"
    plan = json.loads((work / "team-plan.json").read_text(encoding="utf-8"))
    assert plan["summary"] == _fixture_summary("r51B")
    assert [p["id"] for p in plan["processes"]] == sorted(R51B_ID_MISMATCHES)
    # Single source: the untouched card bodies keep their live byte lengths
    # (746/1483 on the cards vs 745/1480 in B's also-written team-plan.json).
    tasks = {p["id"]: p["task"] for p in plan["processes"]}
    assert len(tasks["nthprime"]) == 746
    assert len(tasks["windscale"]) == 1483
    assert cmd_assert_ready(wall_path) == 0


def test_r51_partial_shape_stitches_partial_plan(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Timeout mid-round: only part of the segments ever landed on disk.

    The landed segments are clean (disk scan complete) and still stitch into a
    schema-valid plan; the run-level wall shape degrades to partial on timeout.
    """
    import run_droid_session  # noqa: E402

    work = _unpack("r51A", tmp_path)
    wall_path = _prepare_workdir(work, monkeypatch)
    seg_dir = work / "team" / "lead-plan-segments"
    for name in sorted(p.name for p in seg_dir.iterdir()):
        if name.startswith("process-") and "base62" not in name:
            (seg_dir / name).unlink()

    scan = scan_segments(segments_dir=seg_dir)
    # Disk-truth scan: every segment on disk is clean, so the scan itself is
    # complete; the run-level shape degrades to partial on timeout only.
    assert scan.shape == "complete"
    assert [p["id"] for p in scan.processes] == ["base62"]

    assert stitch_plan_file(work / "team-plan.json") == "complete"
    plan = json.loads((work / "team-plan.json").read_text(encoding="utf-8"))
    assert [p["id"] for p in plan["processes"]] == ["base62"]

    assert cmd_assert_ready(wall_path) == 0
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    assert synced["plan"]["output_shape"] == "complete"

    run_droid_session._patch_session_outcome(wall_path, role="lead", exit_code=124)
    timed_out = json.loads(wall_path.read_text(encoding="utf-8"))
    assert timed_out["budgets"]["session_outcome"]["plan_output_shape"] == "partial"


def test_r51_none_shape_no_plan_no_death_note(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Zero segments: none, fail, and never write a placeholder plan."""
    work = _unpack("r51A", tmp_path)
    wall_path = _prepare_workdir(work, monkeypatch)
    shutil.rmtree(work / "team")

    assert stitch_plan_file(work / "team-plan.json") is None
    assert not (work / "team-plan.json").exists()
    assert cmd_assert_ready(wall_path) == 1


def test_r51_leading_preexisting_plan_not_merged(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """A pre-existing team-plan.json is overwritten from segments, never merged."""
    work = _unpack("r51C", tmp_path)
    wall_path = _prepare_workdir(work, monkeypatch)
    (work / "team-plan.json").write_text(
        json.dumps(
            {"summary": "stale hand-written plan", "processes": [], "plan_version": 1},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    assert stitch_plan_file(work / "team-plan.json") == "complete"
    plan = json.loads((work / "team-plan.json").read_text(encoding="utf-8"))
    assert plan["summary"] == _fixture_summary("r51C")
    assert len(plan["processes"]) == 3
    assert "plan_version" not in plan


def test_r51_written_plan_is_stitch_fresh(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Stitched plan is schema-complete fresh from segments and passes the gate."""
    work = _unpack("r51A", tmp_path)
    wall_path = _prepare_workdir(work, monkeypatch)

    assert stitch_plan_file(work / "team-plan.json") == "complete"
    plan = json.loads((work / "team-plan.json").read_text(encoding="utf-8"))
    assert plan["summary"] == _fixture_summary("r51A")
    assert "plan_version" not in plan  # bookkeeping belongs to the Validate step
    assert cmd_assert_ready(wall_path) == 0
