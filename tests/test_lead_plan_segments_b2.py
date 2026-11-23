"""B2: lead plan segmented persistence — tri-state stitch, no stream salvage."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

import lead_plan_segments as lps  # noqa: E402
from foreman_run_lib import init_wall, save_wall  # noqa: E402
from lead_plan_segments import (  # noqa: E402
    SEGMENT_ID_RE,
    cmd_assert_ready,
    cmd_sync_wall,
    scan_segments,
    stitch_plan_file,
)


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


def test_assert_ready_header_only_records_wall_and_fails(tmp_path: Path, monkeypatch):
    seg = tmp_path / "team/lead-plan-segments"
    _write_header(seg)
    wall = init_wall(run_id="b2p", issue_number=1)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    monkeypatch.setattr(lps, "PLAN_PATH", tmp_path / "team-plan.json")

    assert cmd_assert_ready(wall_path) == 1
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    assert synced["plan"]["output_shape"] == "partial"
    assert synced["plan"]["process_segment_count"] == 0
    assert synced["plan"]["has_header_segment"] is True
    assert synced["chain"]["lead"]["result"] == "unknown"
    assert not (tmp_path / "team-plan.json").exists()


def test_assert_ready_none_fails(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cmd_assert_ready(None) == 1


def test_assert_ready_stitches_plan_from_segments(tmp_path: Path, monkeypatch):
    """Header + cards only: the machine writes team-plan.json and the gate passes."""
    seg = tmp_path / "team/lead-plan-segments"
    _write_header(seg, "ship it")
    _write_process(seg, "alpha")
    _write_process(seg, "beta")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    plan_path = tmp_path / "team-plan.json"
    monkeypatch.setattr(lps, "PLAN_PATH", plan_path)
    assert not plan_path.exists()

    assert cmd_assert_ready(None) == 0
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    assert plan["summary"] == "ship it"
    assert [p["id"] for p in plan["processes"]] == ["alpha", "beta"]
    scan = scan_segments(segments_dir=seg)
    assert scan.shape == "complete"


def test_stitch_tri_state_none_partial_complete(tmp_path: Path, monkeypatch):
    """none (nothing stitchable), partial (unclean scan: a card fails its gate),
    complete (header + every card on disk scans clean)."""
    seg = tmp_path / "team/lead-plan-segments"
    plan_path = tmp_path / "team-plan.json"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    monkeypatch.setattr(lps, "PLAN_PATH", plan_path)

    # none
    assert stitch_plan_file(plan_path) is None
    assert not plan_path.exists()

    # header + at least one card: a stitchable plan exists
    _write_header(seg, "first card survived the timeout")
    _write_process(seg, "only-one")
    assert scan_segments(segments_dir=seg).shape == "complete"
    assert stitch_plan_file(plan_path) == "complete"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    assert plan["summary"] == "first card survived the timeout"
    assert [p["id"] for p in plan["processes"]] == ["only-one"]

    # partial: one clean card + one residue card whose id no longer matches
    # its filename — the clean card stitches, the residue never enters.
    _write_process(seg, "second-one")
    proc = json.loads((seg / "process-second-one.json").read_text(encoding="utf-8"))
    proc["process"]["id"] = "renamed-id"
    (seg / "process-second-one.json").write_text(
        json.dumps(proc, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    assert scan_segments(segments_dir=seg).shape == "partial"
    assert stitch_plan_file(plan_path) == "partial"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    assert [p["id"] for p in plan["processes"]] == ["only-one"]

    # header alone stitches nothing; with both cards clean it is complete.
    (seg / "process-second-one.json").unlink()
    _write_process(seg, "second-one")
    assert scan_segments(segments_dir=seg).shape == "complete"
    assert stitch_plan_file(plan_path) == "complete"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    assert [p["id"] for p in plan["processes"]] == ["only-one", "second-one"]


def test_stitch_overwrites_whole_file_never_merges(tmp_path: Path, monkeypatch):
    seg = tmp_path / "team/lead-plan-segments"
    _write_header(seg, "fresh summary")
    _write_process(seg, "alpha")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    plan_path = tmp_path / "team-plan.json"
    monkeypatch.setattr(lps, "PLAN_PATH", plan_path)
    plan_path.write_text(
        json.dumps(
            {"summary": "stale", "processes": [{"id": "ghost"}], "plan_version": 1},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    assert stitch_plan_file(plan_path) == "complete"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    assert plan["summary"] == "fresh summary"
    assert [p["id"] for p in plan["processes"]] == ["alpha"]


def test_segment_id_derivation_rule_round51_pool():
    """Every round-51 pool module name yields an id satisfying the filename rule."""
    pool = [
        "chaocipher",
        "centroid",
        "base62",
        "dijkstra",
        "nthprime",
        "windscale",
        "bell",
        "tapcode",
        "decimaltime",
        "numwords",
        "code39",
        "solids",
    ]
    for name in pool:
        assert SEGMENT_ID_RE.fullmatch(name), f"pool name {name} violates the id rule"
        assert f"process-{name}.json" == f"process-{name}.json"


@pytest.mark.parametrize("upper,underscored,expected", [
    ("Chaocipher", "chao_cipher", "chaocipher"),
])
def test_segment_id_normalization_documented(upper: str, underscored: str, expected: str):
    """The prompt's normalization rule (lower-case, hyphens) is the scan rule."""
    for name in (upper, underscored):
        assert SEGMENT_ID_RE.fullmatch(name) is None
    assert SEGMENT_ID_RE.fullmatch(expected) is not None


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
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    monkeypatch.setattr(lps, "PLAN_PATH", tmp_path / "team-plan.json")
    monkeypatch.chdir(tmp_path)
    run_droid_session._patch_session_outcome(wall_path, role="lead", exit_code=124)
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    assert synced["budgets"]["session_outcome"]["completion_status"] == "timeout"
    assert synced["budgets"]["session_outcome"]["plan_output_shape"] == "partial"


def test_lead_segment_gate_unit_hard_fail():
    """Hard gate thread trips when threshold elapsed and disk has zero segment files."""
    import time

    import run_droid_session  # noqa: E402
    from lead_plan_segments import SegmentScan  # noqa: E402

    events: list[str] = []
    terminated: list[int] = []

    class _FakeProc:
        returncode: int | None = None

        def poll(self):
            return None

        def terminate(self):
            terminated.append(1)

    proc = _FakeProc()
    gate = run_droid_session._LeadSegmentGate(
        gate_sec=1,
        scan=lambda: SegmentScan("none", (), None, (), ()),
        proc_getter=lambda: proc,
        on_trip=lambda: events.append("trip"),
    )
    gate.start()
    time.sleep(6.5)
    gate.stop()
    assert events == ["trip"]
    assert terminated == [1]
    assert gate.tripped


def test_lead_segment_gate_session_records_none_on_wall(tmp_path: Path, monkeypatch):
    """Lead session with heartbeat: gate trip writes session_outcome none before exit."""
    import run_droid_session  # noqa: E402
    from lead_plan_segments import SegmentScan  # noqa: E402

    wall = init_wall(run_id="b2gate", issue_number=100)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    prompt = tmp_path / "lead-prompt.txt"
    prompt.write_text("plan", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("FOREMAN_RUN_PATCH", "1")
    monkeypatch.setattr(run_droid_session, "_lead_segment_gate_sec", lambda: 1)
    monkeypatch.setattr(
        lps,
        "scan_segments",
        lambda **_: SegmentScan("none", (), None, (), ()),
    )

    class _FakePopen:
        returncode: int | None = None

        def __init__(self, cmd, **kwargs):
            self._alive = True

        def poll(self):
            return None if self._alive else -15

        def terminate(self):
            self._alive = False
            self.returncode = -15

        def communicate(self):
            import time

            while self._alive:
                time.sleep(0.05)
            if self.returncode is None:
                self.returncode = -15
            return ("", "")

    monkeypatch.setattr(
        run_droid_session,
        "build_droid_timeout_cmd",
        lambda **_: (["sleep", "3600"], 3600),
    )
    monkeypatch.setattr(run_droid_session.subprocess, "Popen", _FakePopen)

    code = run_droid_session.run_session(
        wall_path=wall_path,
        role="lead",
        prompt_file=prompt,
        stream_out=tmp_path / "lead-stream.jsonl",
        exit_out=tmp_path / "lead-exit.txt",
        wall_override_sec=600,
        enable_heartbeat=True,
    )
    assert code == run_droid_session.LEAD_SEGMENT_GATE_EXIT
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    assert synced["budgets"]["session_outcome"]["plan_output_shape"] == "none"
    assert synced["budgets"]["session_outcome"]["exit_code"] == run_droid_session.LEAD_SEGMENT_GATE_EXIT


def test_lead_strong_kill_header_on_disk_partial_wall(tmp_path: Path, monkeypatch):
    """Strong-kill drill: SIGKILL-style exit with 00-header already on disk records partial on wall."""
    import run_droid_session  # noqa: E402

    seg = tmp_path / "team/lead-plan-segments"
    _write_header(seg, "killed mid-session")
    wall = init_wall(run_id="b2sigkill", issue_number=101)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(lps, "SEGMENTS_DIR", seg)
    monkeypatch.setattr(lps, "PLAN_PATH", tmp_path / "team-plan.json")
    assert (seg / "00-header.json").is_file()

    # 137 = 128 + SIGKILL (timeout --signal=KILL or external kill).
    run_droid_session._patch_session_outcome(wall_path, role="lead", exit_code=137)
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    assert synced["budgets"]["session_outcome"]["completion_status"] == "droid_failed"
    assert synced["budgets"]["session_outcome"]["plan_output_shape"] == "partial"
    header = json.loads((seg / "00-header.json").read_text(encoding="utf-8"))
    assert header["kind"] == "header"
    assert header["summary"] == "killed mid-session"
