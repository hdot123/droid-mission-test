"""VAL-P2-005 / VAL-P2-006: the validator prompt's new per-artifact discipline.

I-1: the "at most 12 tool calls" arithmetic and the "never batch" phrasing
created the decision paralysis that killed round-54 A/C (27 tool calls, zero
recorder invocations). The prompt now carries a per-artifact main rule (read
one -> record it -> next) plus a fallback (several conclusions already formed?
record them all in the same turn — late is better than never).

I-3: team/handoffs and team/status are protocol artifacts, not out-of-bounds
writes and not conflicts; count differences between pre-merge reports and the
merged suite are not conflicts either (check-summary.json is the authority).

I-4: check-summary.json (produced by prep) is the only authoritative count.
"""
from __future__ import annotations

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
)

R1_STEP = "- name: Validator judges evidence packs only\n"
R2_STEP = "- name: Validator judges evidence packs only (round 2)\n"


def _embedded_prompt(step_name: str) -> str:
    """Same extraction as test_prompt_template: execute the workflow's inline
    template step for a mock judgeable list."""
    yml = TEAM_YML.read_text(encoding="utf-8")
    step = yml.index(step_name)
    chunk_end = yml.index("\n      - name:", step)
    chunk = yml[step:chunk_end]
    marker = str(ROOT / "REVAL_TEST_JSON")
    round_num = 1 if step_name == R1_STEP else 2
    shim = (
        f"\nopen('{marker}', 'w').write(build_validator_prompt(['proc-a', 'proc-b'], round_num={round_num}))\n"
    )
    body = chunk[chunk.index("python3 - <<'PY'") : chunk.index("\n          PY\n")]
    body = body[body.index("\n") + 1 :]
    dedented = "\n".join(
        ln[10:] if ln.startswith(" " * 10) else ln for ln in body.splitlines()
    )
    script = dedented + shim
    import os as _os
    import tempfile

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


# --- I-1: old wording zero residue, main rule + fallback in place -----------


@pytest.mark.parametrize("round_num", [1, 2])
def test_prompt_has_no_tool_budget_arithmetic(round_num: int):
    prompt = build_validator_prompt(["p1"], round_num=round_num)
    assert "at most 12 tool calls" not in prompt
    assert "12 tool calls" not in prompt


@pytest.mark.parametrize("round_num", [1, 2])
def test_prompt_has_no_never_batch(round_num: int):
    prompt = build_validator_prompt(["p1"], round_num=round_num)
    assert "never batch" not in prompt


@pytest.mark.parametrize("round_num", [1, 2])
def test_prompt_carries_per_artifact_main_rule(round_num: int):
    prompt = build_validator_prompt(["p1"], round_num=round_num)
    low = prompt.lower()
    assert "read one piece of evidence" in low
    assert "record" in low
    assert "next" in low


@pytest.mark.parametrize("round_num", [1, 2])
def test_prompt_carries_batch_fallback(round_num: int):
    prompt = build_validator_prompt(["p1"], round_num=round_num)
    low = prompt.lower()
    assert "same turn" in low
    assert ("late is better than never" in low) or ("later is better than never" in low)


# --- I-3: protocol artifacts are not conflicts ------------------------------


@pytest.mark.parametrize("round_num", [1, 2])
def test_prompt_declares_protocol_artifacts_non_conflict(round_num: int):
    prompt = build_validator_prompt(["p1"], round_num=round_num)
    assert "team/handoffs" in prompt
    assert "team/status" in prompt
    assert "not a conflict" in prompt.lower()


@pytest.mark.parametrize("round_num", [1, 2])
def test_prompt_declares_count_difference_non_conflict(round_num: int):
    prompt = build_validator_prompt(["p1"], round_num=round_num)
    low = prompt.lower()
    assert "count" in low
    assert "not a conflict" in low


# --- I-4: check-summary.json is the only authoritative count ----------------


@pytest.mark.parametrize("round_num", [1, 2])
def test_prompt_names_check_summary_authority(round_num: int):
    prompt = build_validator_prompt(["p1"], round_num=round_num)
    assert "check-summary.json" in prompt
    assert "authoritative" in prompt.lower()


# --- workflow contract: both rounds' embedded prompts match the module ------


@pytest.mark.parametrize("step_name,round_num", [(R1_STEP, 1), (R2_STEP, 2)])
def test_workflow_embeds_template_and_matches_module(step_name, round_num):
    embedded = _embedded_prompt(step_name)
    module = build_validator_prompt(["proc-a", "proc-b"], round_num=round_num)
    assert embedded == module


def test_rounds_still_differ_only_parametrically():
    """The parametric points from PR-1 survive the rewrite: intro sentence,
    the --round 2 stamp, and the two round-2 evidence-wording variants."""
    r1 = build_validator_prompt(["p1"], round_num=1)
    r2 = build_validator_prompt(["p1"], round_num=2)
    assert ROUND1_INTRO in r1 and ROUND2_INTRO in r2
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
