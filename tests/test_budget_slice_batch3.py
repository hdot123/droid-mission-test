"""Batch-3: 480+120 validator budget in wall config and workflow lint."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from budget_resolve import (  # noqa: E402
    adopt_reserve_sec,
    assert_validator_job_budget,
    droid_wall_sec,
    validator_session_budget,
)
from foreman_run_lib import init_wall, save_wall  # noqa: E402


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




def test_lint_workflow_budgets_green():
    lint = ROOT / "scripts" / "team" / "lint_workflow_budgets.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout


def test_validator_droid_wall_not_600_when_role_stripped():
    wall = init_wall(run_id="b3e", issue_number=5)
    del wall["budgets"]["roles"]["validator"]["droid_wall_sec"]
    assert droid_wall_sec(wall, "validator") == 480
    del wall["budgets"]["roles"]["validator"]
    assert droid_wall_sec(wall, "validator") == 480


def test_validator_droid_subprocess_uses_480s_timeout(tmp_path: Path, monkeypatch):
    import run_droid_session  # noqa: E402

    wall = init_wall(run_id="b3f", issue_number=6)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    prompt = tmp_path / "p.txt"
    prompt.write_text("prompt", encoding="utf-8")
    captured: list[list[str]] = []

    def fake_run(cmd, **kwargs):
        captured.append(list(cmd))
        from types import SimpleNamespace

        return SimpleNamespace(returncode=0, stderr="")

    monkeypatch.setenv("FOREMAN_RUN_PATCH", "1")
    monkeypatch.setattr(run_droid_session.subprocess, "run", fake_run)
    code = run_droid_session.run_session(
        wall_path=wall_path,
        role="validator",
        prompt_file=prompt,
        stream_out=tmp_path / "s.jsonl",
        exit_out=tmp_path / "exit.txt",
        wall_override_sec=None,
        enable_heartbeat=False,
    )
    assert code == 0
    assert captured, "subprocess.run was not called"
    assert "480s" in captured[0]
    assert "600s" not in captured[0]


def test_validator_override_replaces_480s_only_when_set(tmp_path: Path):
    import run_droid_session  # noqa: E402

    wall = init_wall(run_id="b3g", issue_number=7)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    cmd, sec = run_droid_session.build_droid_timeout_cmd(
        wall_path=wall_path,
        role="validator",
        prompt_text="x",
        wall_override_sec=15,
    )
    assert sec == 15
    assert "15s" in cmd
    assert "480s" not in cmd


def test_adopt_step_wraps_gnu_timeout_from_wall(tmp_path: Path, monkeypatch):
    import run_adopt_step  # noqa: E402

    wall = init_wall(run_id="b3h", issue_number=8)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text("{}", encoding="utf-8")
    captured: list[list[str]] = []

    def fake_run(cmd, env=None):
        captured.append(list(cmd))
        return subprocess.CompletedProcess(cmd, 1)

    monkeypatch.setenv("FOREMAN_RUN_PATCH", "1")
    monkeypatch.setattr(run_adopt_step.subprocess, "run", fake_run)
    run_adopt_step.run_adopt(
        wall_path=wall_path,
        work_dir=work,
        droid_exit=None,
        merge_step_ran=False,
        round_num=1,
        round1_verdict=None,
        github_output=None,
    )
    assert captured
    assert "120s" in captured[0]
    assert captured[0][0] == "timeout"
