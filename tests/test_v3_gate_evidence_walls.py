"""M2-4: the committed V-3 gate wall accounts must be what the real adopt
chain produces from the gate's own session outputs.

Scrutiny m2 round 1 found docs/evidence/v3-gate-rerun/{a,c}/foreman-run.json
carrying human_stop=true and closeout.run_must_fail=true beside adoption
adoption_status=ok — flags stamped by an earlier mis-shaped replay that a
successful adopt never cleared (adopt_verdict sets them only on adoption
failure and never resets them). The artefact cited as proof the gate passed
showed a human-stopped run. These tests replay the real chain
(adopt -> compute_replan_gate -> compute_validate_conclusion, the same three
CLIs the workflow runs) from a FRESH wall against the gate's verbatim work
dirs (tests/fixtures/v3-gate-rerun/) and pin the committed file to the result.
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
from foreman_run_lib import (  # noqa: E402
    init_wall,
    load_wall,
    save_wall,
    validate_with_jsonschema,
)

EVIDENCE = ROOT / "docs" / "evidence" / "v3-gate-rerun"
GATE_WORK = ROOT / "tests" / "fixtures" / "v3-gate-rerun"
RUN_ID = "45195635939"  # the real gate run (see session-meta.json / PROVENANCE)
ISSUE = 812


def _replay_fresh_wall(work: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    """Run the workflow's adopt chain on a fresh wall for the given work dir."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id=RUN_ID, issue_number=ISSUE, foreman_mode="test"), wall_path)
    droid_exit = int((work / "droid-exit.txt").read_text(encoding="utf-8").strip())

    rc = adopt(
        work, wall_path, droid_exit=droid_exit, merge_step_ran=True, round_num=1
    )
    assert rc == 0, "adopt failed on the gate's own outputs"
    wall = load_wall(wall_path)
    wall = compute(wall, round_num=1)
    wall, conclusion = derive(wall, round_num=1)
    save_wall(wall, wall_path)
    return {"wall": load_wall(wall_path), "conclusion": conclusion}


@pytest.mark.parametrize("side", ["a", "c"])
def test_gate_wall_regenerates_green_from_fresh_replay(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, side: str
):
    """A fresh-wall replay of the gate session gives a green run: no
    human_stop, no closeout, adoption ok, conclusion success. The committed
    wall account must equal it — replaying from a wall an earlier failed
    adopt stamped would show human_stop=true beside a green adoption (the
    M2-4 stale-flag shape)."""
    fresh = _replay_fresh_wall(GATE_WORK / f"{side}-work", tmp_path, monkeypatch)
    wall = fresh["wall"]
    validate_with_jsonschema(wall)
    assert wall.get("human_stop") is False, (
        f"{side}: fresh-wall replay must not stamp human_stop (a successful "
        "adopt never clears the flag, so the replay wall must start clean)"
    )
    assert "closeout" not in wall
    val = wall["validation"]
    assert val["adoption_status"] == "ok"
    assert val["overall"] == "pass"
    assert val["pytest_exit"] == 0
    assert val["job_conclusion_derived"] == "success"
    assert fresh["conclusion"] == "success"
    gate = wall["replan_gate"]
    assert gate["should_replan"] is False
    assert gate["should_revalidate"] is False

    committed = json.loads((EVIDENCE / side / "foreman-run.json").read_text(encoding="utf-8"))
    for section in ("human_stop", "closeout", "validation", "replan_gate"):
        assert committed.get(section) == wall.get(section), (
            f"{side}: committed {section} drifted from the fresh-wall replay"
        )


@pytest.mark.parametrize("side", ["a", "c"])
def test_committed_gate_verdict_matches_fresh_adopt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, side: str
):
    """The committed verdict.json is exactly what adopting the gate session's
    outputs produces — the evidence pair stays internally consistent."""
    fresh = _replay_fresh_wall(GATE_WORK / f"{side}-work", tmp_path, monkeypatch)
    committed = json.loads((EVIDENCE / side / "verdict.json").read_text(encoding="utf-8"))
    adopted = json.loads(
        (tmp_path / "verdict.json").read_text(encoding="utf-8")
    )
    assert adopted == committed, f"{side}: committed verdict.json is not the adopt output"
