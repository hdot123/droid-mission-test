"""Round-2 salvage recovery: the validator2 prompt and the adopt2 reader must
agree on rounds.

Scrutiny round-1 blocking finding (m3-round53-prep): the validator2 prompt
discipline line invoked the recorder without --round (the CLI stamps round 1),
while the adopt2 recovery reads with --round 2; read_salvage returns None on
the mismatch, so a validate2 wall-kill recovered zero conclusions — the 52B
loss shape reproduced on the round-2 path. These tests drive the recovery with
the exact command the round-2 prompt tells the validator to run, so the
prompt-to-adopter wiring cannot drift again.

Fixtures are the real round-52 B artifacts (same provenance as
test_validator_partial_verdict_r52b.py).
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from adopt_verdict import adopt  # noqa: E402
from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402
from validator_prompt_template import build_validator_prompt  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "validator-r52b"
PIDS = ["dijkstra", "nthprime", "windscale"]


def _validator_prompt(round_num: int) -> str:
    # Single-source template (VAL-P1-001): the same module the workflow's
    # droid_validate steps render; no more string-slicing team.yml.
    return build_validator_prompt(PIDS, round_num=round_num)


def _recorder_line(prompt: str) -> str:
    hits = [
        ln.strip()
        for ln in prompt.splitlines()
        if ln.strip().startswith("python3 -m salvage_verdict")
    ]
    assert len(hits) == 1, f"expected exactly one recorder discipline line, got {hits}"
    return hits[0]


def _prompted_command(prompt: str, pid: str) -> list[str]:
    """Turn the prompt's discipline line into the concrete argv a validator runs."""
    line = _recorder_line(prompt)
    line = (
        line.replace("<process-id>", pid)
        .replace("pass|fail", "pass")
        .replace(
            "<one line evidence-based reason>",
            "card, handoff, status, diff and checks line up",
        )
    )
    return shlex.split(line)


@pytest.fixture()
def r52b_round2_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Wall + work dir matching the 52B evidence pack; adopt2 reads --round 2."""
    monkeypatch.chdir(tmp_path)
    plan = json.loads((FIXTURES / "plan.json").read_text(encoding="utf-8"))
    manifest = json.loads((FIXTURES / "manifest.json").read_text(encoding="utf-8"))
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    (work / "judgeable.json").write_text(json.dumps(PIDS), encoding="utf-8")
    (work / "blocked.json").write_text("{}", encoding="utf-8")
    (work / "pytest-output.txt").write_text(
        "192 passed, 1 skipped in 15.61s\n", encoding="utf-8"
    )
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="r52b", issue_number=762), wall_path)
    return wall_path, work


def _run_recorder(work: Path, argv: list[str]) -> None:
    env = {**os.environ, "PYTHONPATH": str(ROOT / "scripts" / "team")}
    proc = subprocess.run(
        argv, cwd=work, env=env, capture_output=True, text=True, timeout=30
    )
    assert proc.returncode == 0, f"recorder failed: {proc.stderr}"


def test_prompted_round2_records_survive_validate2_kill(r52b_round2_env):
    """The validate2 wall-kill recovery: record one conclusion using the exact
    command the round-2 prompt mandates, then adopt2 (--round 2) must recover
    it instead of silently returning zero conclusions."""
    wall_path, work = r52b_round2_env
    prompt = _validator_prompt(round_num=2)
    _run_recorder(work, _prompted_command(prompt, PIDS[0]))
    assert (work / "verdict-partial.json").exists()

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=2)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["round2"]["validation"]["adoption_error"] == "draft_timeout"
    assert merged["artifacts"]["team-verdict2-issue-762-run-r52b"]["complete"] is False
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    recovered = {p["id"]: p["verdict"] for p in verdict["processes"]}
    assert recovered[PIDS[0]] == "pass"
    for pid in PIDS[1:]:
        assert recovered[pid] == "blocked"
    assert verdict["salvaged_from"] == "verdict-partial.json"
    assert verdict["salvaged_count"] == 1
    # Fail-closed accounting is intact: the kill still fails the round.
    assert verdict["overall"] == "fail"
    assert verdict["pytest_exit"] is None
    validate_with_jsonschema(merged)


def test_prompted_round2_full_kill_recovers_all_conclusions(r52b_round2_env):
    """52B loss shape on the round-2 path: every process analyzed and recorded
    via the prompted command, killed before the draft — adopt2 recovers all of
    them, never zero. U-3 (PR-2): the unsealed shape routes to the revalidate
    chain instead of terminating (the round-2 revalidate job re-runs the
    validator); the sealed variant adopts normally (see
    test_artifact_first_adoption.py)."""
    wall_path, work = r52b_round2_env
    prompt = _validator_prompt(round_num=2)
    for pid in PIDS:
        _run_recorder(work, _prompted_command(prompt, pid))

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=2)
    assert rc == 0
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    recovered = {p["id"]: p["verdict"] for p in verdict["processes"]}
    assert recovered == {pid: "pass" for pid in PIDS}
    assert verdict["salvaged_count"] == 3
    assert verdict["overall"] == "fail"
    assert verdict["pytest_exit"] is None
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["round2"]["validation"]["adoption_error"] == "draft_timeout"
    assert merged.get("human_stop") is not True
    assert merged["replan_gate"]["should_revalidate"] is True
    validate_with_jsonschema(merged)


def test_recorder_round_flags_pair_with_adopt_flags():
    """Each validator prompt's discipline line must stamp the round its adopt
    step reads back: round 1 relies on the CLI default (adopt1 reads round 1),
    the round-2 prompt must pass --round 2 explicitly (adopt2 reads round 2)."""
    r1_line = _recorder_line(_validator_prompt(round_num=1))
    r2_line = _recorder_line(_validator_prompt(round_num=2))
    assert "--round" not in r1_line
    assert "--round 2" in r2_line
