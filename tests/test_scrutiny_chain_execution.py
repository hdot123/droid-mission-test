"""Whole-chain execution check (scrutiny suggestedGuidanceUpdates): the real
CLI entry points, driven on the output each step actually produces, for the
exact m1-scrutiny-fixes faces:

  chain A — first timeout: adopt(124) -> compute_replan_gate ->
            compute_validate_conclusion (CLI) must leave human_stop OFF and
            the revalidate request ON through every step;
  chain B — torn draft + sealed partial: same CLI chain must adopt ok and
            derive success;
  chain C — after the revalidate job stamps its start marker and the retry
            dies again: every step must terminate human_stop (fail-closed).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402
from salvage_verdict import salvage_verdict  # noqa: E402

PIDS = ["damm", "easterorthodox", "graph"]
ENV = {**__import__("os").environ, "PYTHONPATH": str(ROOT / "scripts" / "team"),
       "FOREMAN_RUN_PATCH": "1"}


def _work(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text(json.dumps({"pytest_exit": 0}), encoding="utf-8")
    (work / "plan.json").write_text(
        json.dumps({"processes": [{"id": pid} for pid in PIDS]}), encoding="utf-8"
    )
    (work / "judgeable.json").write_text(json.dumps(PIDS), encoding="utf-8")
    (work / "blocked.json").write_text("{}", encoding="utf-8")
    return work


def _cli(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args], capture_output=True, text=True, timeout=60, env=ENV,
        cwd=str(cwd),
    )


def _wall(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_chain(tmp_path: Path, run_id: str, *, stamp_started: bool, torn: bool):
    """Drive adopt -> gate -> derive through the real CLI main() entry points."""
    monkey = pytest.MonkeyPatch()
    monkey.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id=run_id, issue_number=812), wall_path)
    work = _work(tmp_path)
    if torn:
        salvage = salvage_verdict(
            work,
            analyzed={pid: {"verdict": "pass", "reason": "aligned"} for pid in PIDS},
            round_num=1,
        )
        salvage["final"] = True
        (work / "verdict-partial.json").write_text(json.dumps(salvage), encoding="utf-8")
        (work / "verdict-droid.json").write_bytes(b"not json at all")
    if stamp_started:
        wall = _wall(wall_path)
        wall.setdefault("replan_gate", {})["revalidate_run_started"] = True
        save_wall(wall, wall_path)

    r1 = _cli(
        str(ROOT / "scripts/team/adopt_verdict.py"), "--wall", str(wall_path),
        "--work-dir", str(work), "--droid-exit", "124", cwd=tmp_path,
    )
    assert r1.returncode == 0, r1.stderr
    r2 = _cli(str(ROOT / "scripts/team/compute_replan_gate.py"), "--wall", str(wall_path), cwd=tmp_path)
    assert r2.returncode == 0, r2.stderr
    r3 = _cli(
        str(ROOT / "scripts/team/compute_validate_conclusion.py"), "--wall", str(wall_path),
        cwd=tmp_path,
    )
    return _wall(wall_path), r3


def test_cli_chain_first_timeout_keeps_revalidate_pending(tmp_path: Path):
    wall, _ = _run_chain(tmp_path / "a" if False else tmp_path, "cli-a", stamp_started=False, torn=False)
    gate = wall["replan_gate"]
    assert gate["should_revalidate"] is True
    assert not gate.get("revalidate_run_started")
    assert wall.get("human_stop") is not True
    assert "closeout" not in wall
    validate_with_jsonschema(wall)


def test_cli_chain_torn_draft_adopts_ok(tmp_path: Path):
    wall, r3 = _run_chain(tmp_path, "cli-b", stamp_started=False, torn=True)
    assert wall["validation"]["adoption_status"] == "ok"
    assert wall["validation"]["overall"] == "pass"
    assert wall["validation"]["job_conclusion_derived"] == "success"
    assert wall.get("human_stop") is not True
    assert r3.returncode == 0, r3.stdout + r3.stderr
    validate_with_jsonschema(wall)


def test_cli_chain_second_timeout_terminates_fail_closed(tmp_path: Path):
    wall, _ = _run_chain(tmp_path, "cli-c", stamp_started=True, torn=False)
    assert wall.get("human_stop") is True
    assert wall["closeout"]["run_must_fail"] is True
    assert wall["replan_gate"]["should_revalidate"] is False
    validate_with_jsonschema(wall)
