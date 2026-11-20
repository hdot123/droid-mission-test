"""Absolute paths for team workflow steps (W-10: working-directory safe)."""
from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    env = os.environ.get("GITHUB_WORKSPACE") or os.environ.get("REPO_ROOT")
    if env:
        return Path(env).resolve()
    return Path.cwd().resolve()


def team_scripts_dir() -> Path:
    return repo_root() / "scripts" / "team"


def team_pythonpath_env() -> dict[str, str]:
    return {"PYTHONPATH": str(team_scripts_dir())}


def team_script(name: str) -> Path:
    return team_scripts_dir() / name