"""VAL-P1-001: the two validator prompts must come from ONE template file.

L-4 (round-54 adversarial finding): the round-1 and round-2 validator prompts
in team.yml were byte-identical except the functional `--round 2` stamp and the
"final validation round after a replan" sentence; both were inlined as separate
f-strings and tests sliced them back out with string indices. This file pins
the single-source contract: both rounds build their prompt from
scripts/team/validator_prompt_template.py, the differences stay parametric,
and the workflow embeds the template (the workflow is the deploy surface).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"
TEMPLATE_PY = ROOT / "scripts" / "team" / "validator_prompt_template.py"
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from validator_prompt_template import (  # noqa: E402
    ROUND1_INTRO,
    ROUND2_INTRO,
    build_validator_prompt,
    render_validator_prompt,
)

R1_STEP = "- name: Validator judges evidence packs only\n"
R2_STEP = "- name: Validator judges evidence packs only (round 2)\n"


def _embedded_prompt(step_name: str) -> str:
    """Extract the prompt the workflow's inline template step renders for a
    mock judgeable list — the same code path CI executes."""
    yml = TEAM_YML.read_text(encoding="utf-8")
    step = yml.index(step_name)
    chunk_end = yml.index("\n      - name:", step)
    chunk = yml[step:chunk_end]
    assert "validator_prompt_template" in chunk, (
        f"step must build its prompt from the single-source template module: {step_name}"
    )
    marker = str(ROOT / "REVAL_TEST_JSON")
    round_num = 1 if step_name == R1_STEP else 2
    shim = (
        f"\nopen('{marker}', 'w').write(build_validator_prompt(['proc-a', 'proc-b'], round_num={round_num}))\n"
    )
    body = chunk[chunk.index("python3 - <<'PY'") : chunk.index("\n          PY\n")]
    body = body[body.index("\n") + 1 :]
    # the heredoc body is indented 10 spaces inside the workflow yaml
    dedented = "\n".join(
        ln[10:] if ln.startswith(" " * 10) else ln for ln in body.splitlines()
    )
    script = dedented + shim
    import os as _os
    import tempfile

    # the workflow step runs with working-directory: work
    with tempfile.TemporaryDirectory() as work_dir:
        (Path(work_dir) / "judgeable.json").write_text('["proc-a", "proc-b"]')
        r = subprocess.run(
            [sys.executable, "-"],
            input=script,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=work_dir,
            env={**_os.environ, "REPO_ROOT": str(ROOT)},
        )
    assert r.returncode == 0, r.stderr
    return (ROOT / marker).read_text(encoding="utf-8")


def test_template_module_exists():
    assert TEMPLATE_PY.is_file(), "scripts/team/validator_prompt_template.py missing"


def test_two_rounds_share_one_template():
    """The prompts differ ONLY in the parametric points: intro sentence, the
    --round stamp, and the two round-2 evidence-wording variants (effective
    plan / final merged candidate). Everything else is single-source text."""
    r1 = build_validator_prompt(["p1"], round_num=1)
    r2 = build_validator_prompt(["p1"], round_num=2)
    assert ROUND1_INTRO in r1
    assert ROUND2_INTRO in r2
    assert ROUND1_INTRO != ROUND2_INTRO
    # identical after removing the parametric points
    r1_norm = r1.replace(ROUND1_INTRO, "@INTRO@")
    r2_norm = (
        r2.replace(ROUND2_INTRO, "@INTRO@")
        .replace(" --round 2", "")
        .replace(
            "- plan.json (the effective plan: revised cards for re-dispatched processes, original cards otherwise)",
            "- plan.json (the plan and process cards)",
        )
        .replace(
            "pytest-output.txt and pytest-exit.txt (full test evidence for the final merged candidate)",
            "pytest-output.txt and pytest-exit.txt (full test evidence for the merged candidate)",
        )
    )
    assert r1_norm == r2_norm


def test_round1_line_has_no_round_stamp_and_round2_has_it():
    r1 = build_validator_prompt(["p1"], round_num=1)
    r2 = build_validator_prompt(["p1"], round_num=2)
    r1_line = [ln for ln in r1.splitlines() if ln.strip().startswith("python3 -m salvage_verdict")]
    r2_line = [ln for ln in r2.splitlines() if ln.strip().startswith("python3 -m salvage_verdict")]
    assert len(r1_line) == 1 and len(r2_line) == 1
    assert "--round" not in r1_line[0]
    assert "--round 2" in r2_line[0]


def test_render_substitutes_judgeable_list():
    prompt = render_validator_prompt(["alpha", "beta"], round_num=1)
    assert "Judge ONLY these processes: alpha, beta" in prompt
    packs_block = [ln for ln in prompt.splitlines() if "- packs/alpha/" in ln]
    assert len(packs_block) == 1
    prompt2 = render_validator_prompt(["alpha", "beta"], round_num=2)
    assert "Judge ONLY these processes: alpha, beta" in prompt2


def test_template_carries_the_fixed_discipline_sections():
    """The single source keeps every mandatory section (the recorder discipline,
    two-file contract, HARD RULE, evidence-only rule)."""
    prompt = build_validator_prompt(["p1"], round_num=1)
    assert "SESSION DISCIPLINE (mandatory, do first)" in prompt
    assert "verdict-droid.json" in prompt and "verdict-droid.md" in prompt
    assert "HARD RULE — a red mandated check is never a pass" in prompt
    assert "Judge only from the evidence in this directory" in prompt


@pytest.mark.parametrize("step_name,round_num", [(R1_STEP, 1), (R2_STEP, 2)])
def test_workflow_embeds_template_and_matches_module(step_name, round_num):
    """The workflow's inline template step executes the template module: its
    output for a mock judgeable set is byte-identical to the module output."""
    embedded = _embedded_prompt(step_name)
    module = build_validator_prompt(["proc-a", "proc-b"], round_num=round_num)
    assert embedded == module


def test_salvage_test_file_reads_prompt_from_template():
    """The round-2 salvage tests must build their prompt from the template
    module instead of slicing team.yml by string index."""
    text = (ROOT / "tests" / "test_salvage_round2_recovery.py").read_text(encoding="utf-8")
    assert "validator_prompt_template" in text
    assert 'prompt = f"""' not in text
