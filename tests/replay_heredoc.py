"""Clean-subprocess replay of team.yml inline heredocs (CI import fidelity).

exec() inside a pytest process inherits the test module's sys.path, so a
workflow heredoc that forgets to put scripts/team on the import path stays
green in the suite and breaks only in CI (the r58 scrutiny round-1
blocking defect: ``from attribution_reason import ...`` at the replan step
raised ModuleNotFoundError under every post-F1 wall shape). CI runs each
heredoc as ``python3 - <<'PY'`` — a fresh interpreter whose sys.path starts
at '', with no PYTHONPATH set — inside the checked-out repository. These
helpers replay exactly that: the extracted heredoc body is piped to a clean
``python3 -`` subprocess whose environment has PYTHONPATH and
GITHUB_WORKSPACE stripped and whose cwd is a ``git archive HEAD`` copy of
the repo (the tracked tree only, scripts/team overlaid from the working
tree so the replay exercises the code as it will merge).

The real checkout is never mutated: replays run inside the disposable
archive copy.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"
REPLAN_STEP = "- name: Foreman classifies failures and writes plan v2\n"


def replan_heredoc_source() -> str:
    """The replan heredoc body, dedented to compilable Python."""
    yml = TEAM_YML.read_text(encoding="utf-8")
    step = yml.index(REPLAN_STEP)
    heredoc = yml.index("python3 - <<'PY'\n", step) + len("python3 - <<'PY'\n")
    end = yml.index("\n          PY\n", heredoc)
    return textwrap.dedent(yml[heredoc:end])


def _clean_env() -> dict[str, str]:
    """CI-shaped environment: PYTHONPATH and GITHUB_WORKSPACE dropped (a
    hostile-parent inherited value must not redirect the seeded import
    path), PATH kept so python3 and tar resolve."""
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("GITHUB_WORKSPACE", None)
    return env


def create_git_archive_copy(dest: Path) -> Path:
    """A checkout-shaped copy of the repo at dest: ``git archive HEAD``
    extracted, then the working tree's scripts/team overlaid (bytecode
    caches excluded) — the workflow sees exactly the import targets a
    checkout would give it, without the tests tree or untracked helpers."""
    dest.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(
        ["git", "archive", "HEAD"], cwd=str(ROOT), capture_output=True, check=True
    )
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive.stdout, check=True)
    shutil.copytree(
        ROOT / "scripts" / "team",
        dest / "scripts" / "team",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    return dest


def run_heredoc_in_clean_subprocess(
    source: str,
    *,
    cwd: Path,
) -> subprocess.CompletedProcess:
    """Replay one heredoc body the way CI runs it: a fresh interpreter with
    the body on stdin (``python3 - <<'PY'``), PYTHONPATH/GITHUB_WORKSPACE
    unset, cwd = the archive-copy workspace. Returns the CompletedProcess
    untouched — callers pin the exit code, the artifacts on disk, and
    stderr."""
    return subprocess.run(
        [sys.executable, "-"],
        input=source,
        cwd=str(cwd),
        env=_clean_env(),
        capture_output=True,
        text=True,
        timeout=60,
    )


def stage_replan_replay_dir(replay_dir: Path) -> None:
    """Create the empty replay workspace a replan heredoc run needs:
    stage/ (the step mkdirs it in CI, but the caller writes the input
    artifacts into it first) — wall-in/ is created by the caller."""
    (replay_dir / "stage").mkdir(parents=True, exist_ok=True)
