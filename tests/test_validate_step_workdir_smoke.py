"""W-10: validate/validate2 steps use working-directory: work — PYTHONPATH must be absolute.

working-directory audit (repo-wide, 2026-11-20):
- `.github/workflows/team.yml` `working-directory: work` at validate droid step (round 1)
- `.github/workflows/team.yml` `working-directory: work` at validate2 droid step (round 2)
- No other `working-directory` entries under this repository.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from workflow_paths import repo_root, team_pythonpath_env, team_scripts_dir  # noqa: E402


def _heredoc_budget_resolve_snippet() -> str:
  return """import json
from budget_resolve import validator_session_budget
w = json.load(open("../foreman-run.json"))
droid, adopt = validator_session_budget(w)
print(droid, adopt)
"""


def test_work_subdir_relative_pythonpath_raises_module_not_found_for_budget_resolve(
    tmp_path: Path,
):
    """Anti-pattern (pre-W-10 workflow): relative PYTHONPATH=scripts/team from work/."""
    work = tmp_path / "work"
    work.mkdir()
    (tmp_path / "foreman-run.json").write_text("{}", encoding="utf-8")
    env = {**os.environ, "PYTHONPATH": "scripts/team"}
    proc = subprocess.run(
        [sys.executable, "-c", "from budget_resolve import validator_session_budget"],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
    assert "ModuleNotFoundError" in proc.stderr + proc.stdout
    assert "budget_resolve" in proc.stderr + proc.stdout


def test_work_subdir_absolute_pythonpath_imports_budget_resolve(tmp_path: Path, monkeypatch):
    """Fixed pattern: GITHUB_WORKSPACE-scoped PYTHONPATH (see team.yml validate step)."""
    monkeypatch.setenv("GITHUB_WORKSPACE", str(ROOT))
    work = tmp_path / "work"
    work.mkdir()
    wall_src = ROOT / "schemas" / "foreman-run.v1.schema.json"
    assert wall_src.is_file()
    import json
    from foreman_run_lib import init_wall, save_wall

    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="w10", issue_number=1), wall_path)
    (work / "foreman-run.json").write_bytes(wall_path.read_bytes())

    env = {**os.environ, **team_pythonpath_env()}
    proc = subprocess.run(
        [sys.executable, "-c", _heredoc_budget_resolve_snippet()],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert team_scripts_dir().is_dir()
    assert repo_root() == ROOT.resolve()