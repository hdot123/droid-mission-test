"""Batch-3: 480+120 validator budget in wall config and workflow lint."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from budget_resolve import (  # noqa: E402
    adopt_reserve_sec,
    assert_validator_job_budget,
    droid_wall_sec,
    validator_session_budget,
)
from foreman_run_lib import init_wall, save_wall  # noqa: E402
from lead_plan_checkpoint import recover  # noqa: E402


def test_init_wall_validator_480_plus_120():
    wall = init_wall(run_id="b3", issue_number=1)
    droid, adopt = validator_session_budget(wall)
    assert droid == 480
    assert adopt == 120
    assert droid + adopt == 600


def test_validator_job_wall_covers_droid_plus_adopt():
    wall = init_wall(run_id="b3b", issue_number=2)
    assert not assert_validator_job_budget(wall, job_timeout_min=15)


def test_droid_wall_reads_wall_not_literal_600():
    wall = init_wall(run_id="b3c", issue_number=3)
    assert droid_wall_sec(wall, "validator") == 480
    assert adopt_reserve_sec(wall, "validator") == 120
    wall["budgets"]["roles"]["validator"]["droid_wall_sec"] = 90
    assert droid_wall_sec(wall, "validator") == 90


def test_run_droid_session_requires_foreman_run_patch(tmp_path: Path, monkeypatch):
    import run_droid_session  # noqa: E402

    wall = init_wall(run_id="b3d", issue_number=4)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    prompt = tmp_path / "p.txt"
    prompt.write_text("hi", encoding="utf-8")
    monkeypatch.delenv("FOREMAN_RUN_PATCH", raising=False)
    code = run_droid_session.run_session(
        wall_path=wall_path,
        role="validator",
        prompt_file=prompt,
        stream_out=tmp_path / "s.jsonl",
        exit_out=tmp_path / "exit.txt",
        wall_override_sec=None,
        enable_heartbeat=False,
    )
    assert code == 2


def test_lead_checkpoint_promote(tmp_path: Path, monkeypatch):
    stream = tmp_path / "lead-stream.jsonl"
    plan = {
        "summary": "s",
        "processes": [{"id": "a", "title": "t", "scope": "s", "files": ["f.py"], "task": "t", "checks": ["true"]}],
    }
    stream.write_text(json.dumps({"content": json.dumps(plan)}) + "\n", encoding="utf-8")
    ckpt = tmp_path / "team"
    ckpt.mkdir()
    monkeypatch.chdir(tmp_path)
    assert recover(stream_path=stream, promote=True) == 0
    assert (tmp_path / "team-plan.json").is_file()
    assert (tmp_path / "team/lead-plan-checkpoint.json").is_file()


def test_lint_workflow_budgets_green():
    lint = ROOT / "scripts" / "team" / "lint_workflow_budgets.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout