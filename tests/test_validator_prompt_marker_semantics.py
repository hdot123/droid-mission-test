"""NC-R2-1 (M3 scrutiny round-2): the validator prompt must judge
checks-failed.marker by CONTENT — the same rule its machine consumers
(marker_verdict.py, wired into the salvage guard and the adopt gate) already
apply. The prompt is the last existence-key consumer of the marker.

Two wording defects against the content semantics:
- the evidence listing said the marker is "present only when the worker's own
  checks failed" — false since v2.6.3: the verify step also writes it when
  every check exited 0 and the problems are only missing evidence files,
  which is exactly the machine-salvaged-pack shape;
- the HARD RULE mandated a fail verdict on the marker's EXISTENCE — an
  obedient validator would then fail a green-by-content salvaged pack,
  leaving the death chain alive at the validator's seat.

The fix aligns the prompt with the machine rule (I-3 precedent: expose the
machine consumers' existing content judgement, no new policy). These tests
pin the new content wording, the zero-residue removal of the presence-key
wording (template source AND rendered product), a byte-freeze of every
untouched clause, and a render-level agreement check: the salvaged r58 pack
ships with a green-by-content marker while the prompt the validator
receives no longer mandates fail on it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PY = ROOT / "scripts" / "team" / "validator_prompt_template.py"
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from marker_verdict import marker_verdict_red  # noqa: E402
from validator_prompt_template import build_validator_prompt  # noqa: E402

PID = "hslconv"


@pytest.fixture(scope="module")
def r1() -> str:
    return build_validator_prompt([PID], round_num=1)


@pytest.fixture(scope="module")
def r2() -> str:
    return build_validator_prompt([PID], round_num=2)


def _hard_rule(prompt: str) -> str:
    lines = [ln for ln in prompt.splitlines() if ln.lstrip().startswith("- HARD RULE")]
    assert len(lines) == 1, f"expected exactly one HARD RULE line, got {len(lines)}"
    return lines[0]


# --- (a) the evidence listing states the true write condition ----------------


def test_listing_states_true_marker_write_condition(r1, r2):
    """The listing drops the false "present only when checks failed" claim and
    states the v2.6.3 fact: the marker is also written on green checks with
    missing-file problems."""
    for prompt in (r1, r2):
        assert "checks-failed.marker (written whenever" in prompt
        assert "the problems are only missing evidence files" in prompt


# --- (b) the HARD RULE judges marker content ---------------------------------


def test_hard_rule_fail_triggers_are_content_facts(r1, r2):
    """MUST-fail is keyed on the machine rule's red facts: a non-zero exit in
    checks-exit.json, a non-zero "check exit" line in the marker, a
    malformed-status problem, or any other unrecognized problem."""
    for prompt in (r1, r2):
        line = _hard_rule(prompt)
        assert 'has a non-zero "exit"' in line
        assert 'a "check exit" line with a non-zero code' in line
        assert 'a "problem: status file is not valid JSON" line' in line
        assert 'any problem line other than a "problem: missing expected file:" entry' in line
        assert "marker content that cannot be parsed into these shapes counts red too" in line
        assert 'you MUST judge that process "fail"' in line


def test_hard_rule_missing_file_only_marker_is_not_a_fail(r1, r2):
    """The benign branch, stated in the rule itself: a missing-file-only
    marker must not fail the process by itself; judge the rest of the pack
    with checks-exit.json as the authority."""
    for prompt in (r1, r2):
        line = _hard_rule(prompt)
        assert "missing-expected-file entries is NOT red by itself" in line
        assert "machine-salvaged pack" in line
        assert "checks-exit.json as the authoritative check record" in line


# --- zero residue of the old existence-key wording ---------------------------


def test_old_presence_wording_zero_residue_in_render(r1, r2):
    for prompt in (r1, r2):
        assert "present only when" not in prompt
        assert "marker exists" not in prompt
        assert 'or packs/<id>/checks-failed.marker exists' not in prompt


def test_old_presence_wording_zero_residue_in_template_source():
    text = TEMPLATE_PY.read_text(encoding="utf-8")
    assert "present only when" not in text
    assert "marker exists" not in text


# --- untouched clauses byte-frozen -------------------------------------------

UNCHANGED_CLAUSES = [
    # session discipline + recorder + conflict/fallback/final machinery
    "SESSION DISCIPLINE (mandatory, do first): work through the processes one at a time — read one piece of evidence, IMMEDIATELY persist that one conclusion by running the verdict-recorder tool, then move on to the next piece:",
    'The same persistence discipline applies to out-of-card conflicts: the moment you find one, record it in the same call by appending --conflict "<process-id>|<what conflicts, both values/sections named>|<where it is flagged, file with a short quote>" (repeat the flag for each extra conflict). A conflict recorded only in your reasoning is lost when the session is killed.',
    "FALLBACK: if you have already formed conclusions for several processes, record them all in the same turn right away — late is better than never. The recorder file survives a session timeout; conclusions that live only in your reasoning are lost when the session is killed.",
    "FINISHING: when your last process is recorded, run the recorder once more with --final (same --process/--verdict/--reason as that last conclusion). --final seals the partial file as your deliverable: a sealed partial that covers every process listed above is adopted as the verdict even if the session dies before the final files below are written. If the session is killed after your last process is recorded but the partial was never sealed with --final, it is treated as incomplete work and the round is re-validated.",
    # two-file contract
    'The top-level "conflicts" array is required in verdict-droid.json: write an empty array when no judged process flagged an out-of-card conflict.',
    "It must contain exactly one verdict for each judged process listed above, no more, no fewer.",
    # rules other than the HARD RULE, verbatim
    "- Pass a process only when its card, handoff, status, diff, and check outputs line up.",
    '- If a process\'s status.json or handoff.md explicitly flags a conflict outside its card or inside the work order itself (for example a body-vs-acceptance mismatch) and neither the card nor the plan addresses it, you MUST record it in the top-level "conflicts" array — do not bury it in a reason and do not silently pass over it. Recording a conflict does not by itself change that process\'s verdict: judge the card as written; the conflict is escalated for a human to see, and a verdict carrying any escalated conflict is treated as fail by the machine gates.',
    "- NOT conflicts: the team/handoffs/* and team/status/* files are protocol artifacts the pipeline itself maintains (they are whitelisted for the workers); their presence or absence is never an out-of-card conflict. A count difference between any pre-merge report and check-summary.json is bookkeeping, not a conflict — check-summary.json is the single authoritative count.",
    "- Authoritative counts: check-summary.json (per-card passed/skipped and merged totals) is the ONLY authoritative test-count source. Do not recount from worker status files and do not treat a mismatch as evidence of tampering.",
    "- Judge only from the evidence in this directory. Do not modify any evidence file.",
    # HARD RULE fragments that must not drift
    'HARD RULE — a red mandated check is never a pass: if any entry in packs/<id>/checks-exit.json has a non-zero "exit"',
    'you MUST judge that process "fail"',
    "Alignment proves the evidence is honest, not that the work passed",
    "In the reason, cite the failed check command(s) and exit code(s) from checks-exit.json.",
    "One exception: exit 127 recorded because pytest was unavailable does not count under this rule (that is an environment failure, judged via the pack/manifest evidence).",
]


@pytest.mark.parametrize("round_num", [1, 2])
def test_untouched_clauses_byte_identical(round_num):
    """Every clause outside the two marker wordings stays verbatim: the
    conflict declaration, the team-file whitelist, --final, --conflict, the
    authoritative-counts rule and the exit-127 exception."""
    prompt = build_validator_prompt([PID], round_num=round_num)
    for clause in UNCHANGED_CLAUSES:
        assert clause in prompt, f"clause drifted in round {round_num}: {clause[:60]}..."


def test_prompt_vocabulary_matches_marker_verdict_module():
    """No-drift seam: the prompt's rule names exactly the line shapes the
    shared module parses and classifies, and the module reads the benign
    shape green."""
    green_body = (
        f"process: {PID}\n"
        "check exit 0: python3 -m pytest tests/ -q\n"
        "problem: missing expected file: team/status/hslconv.json\n"
    )
    assert marker_verdict_red(green_body) is False
    prompt = build_validator_prompt([PID], round_num=1)
    line = _hard_rule(prompt)
    for shape in ("check exit", "status file is not valid JSON", "missing expected file"):
        assert shape in line, f"prompt rule lost the module's vocabulary: {shape}"


# --- adopt-side / docs residue (NC-R2-3 sync) --------------------------------


def test_readme_s2_gate_description_matches_content_semantics():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "存在即 fail" not in readme, "README still describes the adopt gate as presence-based"
    assert "按内容判定为红" in readme


# --- render level: the salvaged r58 shape, prompt vs machine gate ------------


def test_salvaged_pack_shape_prompt_and_machine_gate_agree(tmp_path):
    """VAL-CROSS-001 final ring, made executable: the salvaged pack reaches
    the validator WITH a green-by-content marker (the exact bytes the real
    verify step writes on the r58 shape), and the prompt the validator
    renders no longer mandates a fail verdict on that marker."""
    e2e = pytest.importorskip("tests.test_r58d_e2e_replay")
    ws = e2e.stage_evidence(tmp_path / "salv", e2e.FIXTURE)
    pack = ws / "evidence" / "packs" / e2e.PID
    marker = (
        f"process: {e2e.PID}\n"
        "check exit 0: python3 -m pytest tests/test_hslconv.py -q\n"
        "check exit 0: python3 -m pytest tests/ -q\n"
        f"problem: missing expected file: team/handoffs/{e2e.PID}.md\n"
        f"problem: missing expected file: team/status/{e2e.PID}.json\n"
    )
    (pack / "checks-failed.marker").write_text(marker, encoding="utf-8")
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["packs"][e2e.PID]["checks_failed_marker"] = True
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    wall = e2e.wall_with(
        [json.loads((e2e.FIXTURE / "worker-delta-wall-killed.json").read_text(encoding="utf-8"))]
    )
    reports = e2e.run_salvage(ws, wall)
    entry = next(r for r in reports if r["pid"] == e2e.PID)
    assert entry["salvaged"] is True, entry["reasons"]

    # machine face: this exact marker content reads green
    assert marker_verdict_red(marker) is False
    # LLM face: the prompt no longer instructs fail-on-presence for it
    prompt = build_validator_prompt([e2e.PID], round_num=1)
    assert "marker exists" not in prompt
    assert "present only when" not in prompt
    assert "missing-expected-file entries is NOT red by itself" in prompt
