"""Execution-level pins for the validator prompt render steps (M2-2).

String pins (tests/test_v3_prework_pins.py) assert what the step text says;
they cannot say what the step does. Scrutiny m2 round 1 (M2-1) found all four
render steps dead on CI: REPO_ROOT is assigned without `export`, the inline
python child reads os.environ["REPO_ROOT"], bash never passes a non-exported
variable to a child, so the step exits 1 with KeyError before
validator-prompt.txt is written — while the full suite stayed green, because
the tests that do execute the render heredoc inject REPO_ROOT themselves.

These tests execute the step's real `run:` text under the runner's shell form
(bash --noprofile --norc -eo pipefail -c) with only the variables a GitHub
runner supplies: GITHUB_WORKSPACE set, REPO_ROOT absent. The script is cut
before the live droid session launches and the byte identity of the rendered
prompt is asserted against the template module.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"

sys.path.insert(0, str(ROOT / "scripts" / "team"))

from validator_prompt_template import build_validator_prompt  # noqa: E402

RENDER_SITES = [
    # (job key, step name, round)
    ("validate", "Validator judges evidence packs only\n", 1),
    ("revalidate", "Validator judges evidence packs only (revalidate)\n", 1),
    ("validate2", "Validator judges evidence packs only (round 2)\n", 2),
    ("revalidate2", "Validator judges evidence packs only (revalidate round 2)\n", 2),
]

JUDGEABLE = ["proc-a", "proc-b", "proc-c"]


def _job_text(yml: str, job_key: str) -> str:
    m = re.search(rf"^  {job_key}:\n", yml, re.MULTILINE)
    assert m, f"job {job_key} missing"
    next_m = re.search(r"^  [a-z0-9-]+:\n", yml[m.end() :], re.MULTILINE)
    end = m.end() + next_m.start() if next_m else len(yml)
    return yml[m.start() : end]


def _step_text(job_text: str, step_name: str) -> str:
    start = job_text.index(f"- name: {step_name}")
    chunk_end = job_text.index("\n      - name:", start)
    return job_text[start:chunk_end]


def _run_text(step_chunk: str) -> str:
    """Extract and dedent the step's `run: |` block scalar."""
    m = re.search(r"^        run: \|\n((?:          .*\n?|\n)*)", step_chunk, re.MULTILINE)
    assert m, "run: | block missing"
    block = m.group(1)
    return "\n".join(ln[10:] if ln.startswith(" " * 10) else ln for ln in block.splitlines())


@pytest.mark.parametrize("job_key,step_name,round_num", RENDER_SITES)
def test_render_step_executes_under_runner_shell(job_key, step_name, round_num):
    """The step's real shell, run with runner-only variables, renders a prompt
    byte-identical to build_validator_prompt — session never launched.

    The script is truncated at the live droid session call (run_droid_session.py);
    everything before it must succeed on its own: the render heredoc, the wall
    copy and the budget heredoc. Removing the `export` from the REPO_ROOT
    assignment turns this test red (KeyError: 'REPO_ROOT', exit 1)."""
    yml = TEAM_YML.read_text(encoding="utf-8")
    step = _step_text(_job_text(yml, job_key), step_name)
    run = _run_text(step)
    assert "run_droid_session.py" in run, f"{job_key}: guard lost, truncation unsafe"

    cut = run.index("FOREMAN_RUN_PATCH=1")
    script = run[:cut] + "\nexit 0\n"

    work = Path(tempfile.mkdtemp(prefix=f"render-{job_key}-"))
    try:
        # the step runs with working-directory: work; ../wall-in/foreman-run.json
        # must exist one level above it or the wall copy fails for the wrong reason
        (work / "work").mkdir()
        (work / "wall-in").mkdir()
        (work / "work" / "judgeable.json").write_text(json.dumps(JUDGEABLE))
        wall = json.loads(
            (ROOT / "tests" / "fixtures" / "foreman_wall_r53c" / "foreman-run.json").read_text(
                encoding="utf-8"
            )
        )
        (work / "wall-in" / "foreman-run.json").write_text(json.dumps(wall))
        (work / "gh-env.txt").write_text("")
        (work / "gh-output.txt").write_text("")

        env = {k: v for k, v in os.environ.items() if k in ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR")}
        env["GITHUB_WORKSPACE"] = str(ROOT)  # a real runner variable
        env["GITHUB_ENV"] = str(work / "gh-env.txt")
        env["GITHUB_OUTPUT"] = str(work / "gh-output.txt")
        # REPO_ROOT is deliberately absent: it is the variable under test.
        # A runner also carries CI=true; keep it so step logic stays honest.
        env["CI"] = "true"

        proc = subprocess.run(
            ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", script],
            cwd=str(work / "work"),
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert proc.returncode == 0, (
            f"{job_key}: step shell exited {proc.returncode} before the session "
            f"launch\nstderr:\n{proc.stderr[-2000:]}"
        )
        prompt = (work / "work" / "validator-prompt.txt").read_bytes()
        assert prompt == build_validator_prompt(JUDGEABLE, round_num=round_num).encode(), (
            f"{job_key}: rendered prompt drifted from the template module"
        )
    finally:
        shutil.rmtree(work, ignore_errors=True)
