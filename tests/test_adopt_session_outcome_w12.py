"""W-12: adopt step must not record session_outcome ok when validator droid never started."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from adopt_verdict import adopt  # noqa: E402
from budget_resolve import adopt_session_completion_status  # noqa: E402
from compute_validate_conclusion import derive  # noqa: E402
from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402


def _minimal_work(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text("{}", encoding="utf-8")
    (work / "plan.json").write_text('{"processes": []}', encoding="utf-8")
    (work / "judgeable.json").write_text("[]", encoding="utf-8")
    return work


def test_adopt_session_not_started_records_missing_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # adopt() writes verdict.json/verdict.md to CWD (bare relative paths);
    # without chdir the suite pollutes the repo root (round-53 F-1 killer).
    monkeypatch.chdir(tmp_path)
    wall = init_wall(run_id="w12a", issue_number=701)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    work = _minimal_work(tmp_path)
    adopt(work, wall_path, droid_exit=None, merge_step_ran=False)
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    outcome = merged["budgets"]["session_outcome"]
    assert outcome["completion_status"] == "missing_output"
    assert outcome["exit_code"] == -1
    validate_with_jsonschema(merged)
    _, conclusion = derive(merged)
    assert conclusion == "failure"


def test_adopt_session_timeout_regression(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    wall = init_wall(run_id="w12b", issue_number=702)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    work = _minimal_work(tmp_path)
    adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["budgets"]["session_outcome"]["completion_status"] == "timeout"
    assert merged["validation"]["adoption_status"] == "failed"
    assert merged["validation"]["adoption_error"] == "draft_timeout"


def test_adopt_session_ok_when_droid_exit_zero_and_no_judgeable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    assert adopt_session_completion_status(0) == "ok"
    wall = init_wall(run_id="w12c", issue_number=703)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    work = _minimal_work(tmp_path)
    adopt(work, wall_path, droid_exit=0, merge_step_ran=False)
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["budgets"]["session_outcome"]["completion_status"] == "ok"