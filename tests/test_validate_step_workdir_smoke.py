"""W-10: validate/validate2 steps use working-directory: work — PYTHONPATH must be absolute.

Parse `.github/workflows/team.yml` validator droid steps directly (batch B) so step text
drift breaks tests without updating a parallel replica in workflow_paths.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEAM_YML = ROOT / ".github/workflows/team.yml"
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from workflow_paths import repo_root, team_pythonpath_env, team_scripts_dir  # noqa: E402

YML_PYTHONPATH_EXPORT = 'export PYTHONPATH="${REPO_ROOT}/scripts/team"'
YML_TEAM_PY = 'TEAM_PY="${REPO_ROOT}/scripts/team"'
YML_REPO_ROOT = 'export REPO_ROOT="${GITHUB_WORKSPACE}"'

_BUDGET_HEREDOC_RE = re.compile(
    r"python3 -\s+<<'PY'\s+>>\s*\"\$GITHUB_ENV\"\s*\n([\s\S]*?)\n\s*PY",
)


def _step_chunk_by_id(text: str, step_id: str) -> str:
    needle = f"id: {step_id}"
    idx = text.find(needle)
    assert idx >= 0, f"step id {step_id} missing from team.yml"
    next_step = text.find("\n      - name:", idx + len(needle))
    return text[idx : next_step if next_step > 0 else len(text)]


def _step_working_directory(step_chunk: str) -> str | None:
    m = re.search(r"working-directory:\s*(\S+)", step_chunk)
    return m.group(1) if m else None


def _step_run_body(step_chunk: str) -> str:
    m = re.search(r"run: \|\n", step_chunk)
    assert m, "run: | block missing on validator droid step"
    lines: list[str] = []
    for line in step_chunk[m.end() :].splitlines():
        if line.startswith("      - "):
            break
        if line.strip() == "":
            lines.append("")
            continue
        if not line.startswith("          "):
            break
        lines.append(line[10:])
    return "\n".join(lines) + "\n"


def _budget_resolve_heredoc(run_body: str) -> str:
    m = _BUDGET_HEREDOC_RE.search(run_body)
    assert m, "budget_resolve GITHUB_ENV heredoc missing from team.yml step"
    return m.group(1).strip() + "\n"


def _run_budget_heredoc_in_work(
    heredoc: str,
    workspace_root: Path,
    work_dir: Path,
    wall_path: Path,
) -> subprocess.CompletedProcess[str]:
    (work_dir / "foreman-run.json").write_bytes(wall_path.read_bytes())
    env = {
        **os.environ,
        "GITHUB_WORKSPACE": str(workspace_root),
        "PYTHONPATH": str(workspace_root / "scripts" / "team"),
    }
    return subprocess.run(
        [sys.executable, "-"],
        input=heredoc,
        cwd=work_dir,
        env=env,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize("step_id", ["droid_validate", "droid_validate2"])
def test_team_yml_validator_step_pythonpath_lines_match_workflow_paths(step_id: str):
    text = TEAM_YML.read_text(encoding="utf-8")
    chunk = _step_chunk_by_id(text, step_id)
    run = _step_run_body(chunk)
    assert _step_working_directory(chunk) == "work"
    assert YML_REPO_ROOT in run
    assert YML_PYTHONPATH_EXPORT in run
    assert YML_TEAM_PY in run

    os.environ["GITHUB_WORKSPACE"] = str(ROOT)
    resolved = team_pythonpath_env()["PYTHONPATH"]
    assert resolved == str((ROOT / "scripts" / "team").resolve())
    assert resolved == str(team_scripts_dir())
    assert repo_root() == ROOT.resolve()
    # Step text must stay on the absolute REPO_ROOT/scripts/team contract (not relative PYTHONPATH).
    assert "PYTHONPATH=scripts/team" not in run.replace("${REPO_ROOT}/scripts/team", "")


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


@pytest.mark.parametrize("step_id", ["droid_validate", "droid_validate2"])
def test_work_subdir_team_yml_budget_heredoc_imports_budget_resolve(
    step_id: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """Execute budget_resolve heredoc extracted from team.yml validate / validate2 steps."""
    monkeypatch.setenv("GITHUB_WORKSPACE", str(ROOT))
    text = TEAM_YML.read_text(encoding="utf-8")
    heredoc = _budget_resolve_heredoc(_step_run_body(_step_chunk_by_id(text, step_id)))

    from foreman_run_lib import init_wall, save_wall

    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="w10", issue_number=1), wall_path)
    work = tmp_path / "work"
    work.mkdir()

    proc = _run_budget_heredoc_in_work(heredoc, ROOT, work, wall_path)
    assert proc.returncode == 0, proc.stderr
    assert "VALIDATOR_DROID_WALL_SEC=" in proc.stdout
    assert "ADOPT_RESERVE_SEC=" in proc.stdout