"""Scrutiny round-1 prework pins for the V-3 gate (PR1-8 / PR1-9 / PR1-10 /
PR2-6), all about the single-source validator prompt and the revalidate sha
wiring. V-3 runs a real droid session against this exact prompt, so the
rendered bytes and the documented flags must be pinned, not assumed.

PR1-8: every inline render site in team.yml imports the template module the
same way (REPO_ROOT path insertion) — a divergent GITHUB_WORKSPACE-only import
drifts between render sites, and byte-drift is exactly the L-4 shape this
template was extracted to kill. M2-2: the import root must be an *exported*
REPO_ROOT — bash never passes a plain shell assignment to a `python3 -` child,
so an un-exported render site KeyErrors on CI while the suite (whose render
tests inject the variable themselves) stays green;
tests/test_render_step_execution.py executes the real step shell to catch it.

PR1-9: the workflow-embeds-template tests execute the workflow's own render
output (not a re-render through the module), so dropping the render call or
changing the stamp in team.yml turns them red.

PR1-10: the four manifest sha gates in the two revalidate jobs (header check
against EXPECTED_MANIFEST_SHA plus the per-file integrity walk) are pinned per
site — deleting any comparison leaves the suite red, fail-closed stays fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"

sys.path.insert(0, str(ROOT / "scripts" / "team"))

from validator_prompt_template import (  # noqa: E402
    build_validator_prompt,
    render_validator_prompt,
)

RENDER_SITES = [
    # (job key, step name, round) — the four inline template steps in team.yml
    ("validate", "Validator judges evidence packs only\n", 1),
    ("revalidate", "Validator judges evidence packs only (revalidate)\n", 1),
    ("validate2", "Validator judges evidence packs only (round 2)\n", 2),
    ("revalidate2", "Validator judges evidence packs only (revalidate round 2)\n", 2),
]

SHA_GATES = [
    # (job key, verifier print fragment, env pin the job's env block must carry)
    ("revalidate", "verified against prep output", "needs.prep.outputs.manifest_sha256"),
    (
        "revalidate2",
        "verified against prep2 output",
        "needs.prep2.outputs.manifest_sha256",
    ),
]


@pytest.fixture(scope="module")
def yml() -> str:
    return TEAM_YML.read_text(encoding="utf-8")


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


# --- PR1-8: render sites import the module through REPO_ROOT ----------------


@pytest.mark.parametrize("job_key,step_name,round_num", RENDER_SITES)
def test_render_site_imports_template_via_repo_root(yml, job_key, step_name, round_num):
    """Every render site resolves the template module through REPO_ROOT so the
    rendered prompt is byte-identical across all four jobs (L-4 drift shape)."""
    step = _step_text(_job_text(yml, job_key), step_name)
    assert "from validator_prompt_template import" in step, (
        f"{job_key}/{step_name.strip()}: must render from the single-source template"
    )
    assert f"round_num={round_num}" in step, (
        f"{job_key}: round stamp must stay parametric (round_num={round_num})"
    )
    # REPO_ROOT must reach the python child's environment: a plain shell
    # assignment is invisible to `python3 - <<'PY'` children (bash exports
    # nothing to a child without `export`), so the render KeyErrors on CI —
    # the exact runner-unset drift shape this pin exists to prevent.
    assert "export REPO_ROOT=" in step, (
        f"{job_key}/{step_name.strip()}: REPO_ROOT must be exported before the "
        "template import resolves through it"
    )
    assert 'os.environ["REPO_ROOT"]' in step, (
        f"{job_key}/{step_name.strip()}: template import must go through REPO_ROOT"
    )
    assert 'os.environ["GITHUB_WORKSPACE"]' not in step, (
        f"{job_key}/{step_name.strip()}: GITHUB_WORKSPACE-only import drifts and "
        "KeyErrors when unset (revalidate2 renderer shape)"
    )


def test_render_alias_matches_canonical_builder():
    """render_validator_prompt stays a byte-identical alias of the canonical
    builder (the workflow imports build_validator_prompt; both spellings must
    render the same bytes)."""
    assert render_validator_prompt(["p1"], round_num=1) == build_validator_prompt(
        ["p1"], round_num=1
    )
    assert render_validator_prompt(["p1"], round_num=2) == build_validator_prompt(
        ["p1"], round_num=2
    )


def test_all_four_render_sites_present_and_parametric(yml):
    """The two-round, two-job matrix is complete: no fifth render site, no
    missing site, each carrying its own round stamp."""
    stamps = re.findall(r"build_validator_prompt\(judgeable, round_num=(\d)\)", yml)
    assert sorted(stamps) == ["1", "1", "2", "2"]


# --- PR1-10: revalidate sha gates pinned per site ---------------------------


@pytest.mark.parametrize("job_key,verified_frag,env_pin", SHA_GATES)
def test_revalidate_sha_gate_steps_are_pinned(yml, job_key, verified_frag, env_pin):
    """Both sha gates in each revalidate job stay in place: the header check
    (refusing to judge on mismatch) and the per-file integrity walk, plus the
    env pin that carries prep's sha into the job."""
    job = _job_text(yml, job_key)
    assert f"EXPECTED_MANIFEST_SHA: ${{{{ {env_pin} }}}}" in job, (
        f"{job_key}: env must pin {env_pin}"
    )
    gate = re.search(
        r"- name: Extract evidence and keep verdict inputs.*?(?=\n      - name:)",
        job,
        re.DOTALL,
    )
    assert gate, f"{job_key}: extract step missing"
    text = gate.group(0)
    assert 'expected_sha = os.environ.get("EXPECTED_MANIFEST_SHA", "")' in text
    assert (
        'if not expected_sha or actual_sha != expected_sha:' in text
    ), f"{job_key}: header sha gate deleted (fail-closed hole)"
    assert "refusing to judge" in text, f"{job_key}: refusal branch deleted"
    assert verified_frag in text, (
        f"{job_key}: site-specific sha-verified print missing (the pin this "
        "test exists to enforce — PR1-10)"
    )
    # the per-file integrity walk (every file in the manifest must match on disk)
    assert 'for path, digest in manifest["sha256"].items():' in text
    assert 'bad.append(path)' in text
    assert 'print("evidence integrity check failed:", bad)' in text
    assert "sys.exit(1)" in text


def test_revalidate_guard_stamps_run_started(yml):
    """The at-most-once guard keeps its refusal branch and its run-start stamp
    (PR1-2 semantics that the sha gates sit beside)."""
    for job_key in ("revalidate", "revalidate2"):
        job = _job_text(yml, job_key)
        guard = job.index("Refuse a second revalidate")
        block = job[guard : job.index("\n      - name: Download evidence", guard)]
        assert "revalidate_run_started" in block
        assert "refusing to run again" in block
        assert "revalidate_run_started" in block and "= True" in block


# --- PR2-6: the prompt documents the persistence-channel flags --------------


@pytest.mark.parametrize("round_num", [1, 2])
def test_prompt_documents_final_seal_flag(round_num: int):
    """The D-2 seal is the only way the I-6 artifact-first adoption fires; a
    prompt that never mentions --final keeps the headline path undiscoverable
    (scrutiny PR2-6)."""
    prompt = build_validator_prompt(["p1"], round_num=round_num)
    assert "--final" in prompt
    low = prompt.lower()
    assert "final" in low and "deliverable" in low
    assert "covers every process listed above" in low


@pytest.mark.parametrize("round_num", [1, 2])
def test_prompt_documents_conflict_flag(round_num: int):
    """Conflicts must be recordable the moment they are found (the same
    persist-immediately discipline as verdicts), not deferred to the final
    two-file write the session may not reach."""
    prompt = build_validator_prompt(["p1"], round_num=round_num)
    assert "--conflict" in prompt
    low = prompt.lower()
    assert "pipe" in low or "|" in prompt


@pytest.mark.parametrize("round_num", [1, 2])
def test_prompt_flags_match_recorded_cli_line(round_num: int):
    """The documented flags and the recorder discipline line stay consistent:
    the --final note must sit beside the per-artifact discipline and must not
    contradict the line's own stamping."""
    prompt = build_validator_prompt(["p1"], round_num=round_num)
    lines = prompt.splitlines()
    recorder_idx = [
        i for i, ln in enumerate(lines) if ln.strip().startswith("python3 -m salvage_verdict")
    ]
    assert len(recorder_idx) == 1
    after = "\n".join(lines[recorder_idx[0] : recorder_idx[0] + 6])
    assert "--final" in after, "--final documentation must sit beside the discipline line"
    if round_num == 2:
        assert "--round 2" in lines[recorder_idx[0]]
    else:
        assert "--round" not in lines[recorder_idx[0]]
    # M2-3: the re-validation price is scoped to the kill-with-unsealed-partial
    # case — the normal paths (a complete draft on disk, or no partial) adopt
    # without any revalidation, so the sentence must not promise a price the
    # adopt chain never charges.
    assert "killed after your last process is recorded" in prompt
    assert "the round is re-validated" in prompt
    assert "the whole round is re-validated" not in prompt
