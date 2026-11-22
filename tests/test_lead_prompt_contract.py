"""Lead prompt contract: segments are the only hand-written source.

Locks the M1 assembly refactor into pytest: no instruction may ask the lead
to write team-plan.json, the id derivation rule must be present and correct
for the round-51 module pool, and every revise/overwrite/placeholder mention
must stay consistent with the never-overwrite segment protocol.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"

SEGMENT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
WRITE_PLAN_PHRASES = (
    "write the full team-plan.json",
    "Create team-plan.json",
    "write team-plan.json",
    "final team-plan.json write",
    "into team-plan.json",
)


def _team_yml() -> str:
    return TEAM_YML.read_text(encoding="utf-8")


def _lead_prompt() -> str:
    yml = _team_yml()
    start = yml.index('prompt = f"""') + len('prompt = f"""')
    end = yml.index('"""', start)
    return yml[start:end]


def _pos(needle: str) -> int:
    yml = _team_yml()
    return yml.index(needle)


def test_prompt_never_asks_lead_to_write_team_plan():
    prompt = _lead_prompt()
    hits = [phrase for phrase in WRITE_PLAN_PHRASES if phrase in prompt]
    assert not hits, f"lead prompt still instructs writing team-plan.json: {hits}"
    assert "never create, edit, or write it" in prompt
    assert "assembled by the system" in prompt


def test_prompt_still_requires_segments():
    prompt = _lead_prompt()
    assert "team/lead-plan-segments/00-header.json" in prompt
    assert "team/lead-plan-segments/process-<id>.json" in prompt
    assert "never overwrite an existing segment file" in prompt


def test_prompt_id_derivation_rule_matches_pool():
    prompt = _lead_prompt()
    assert "^[a-z0-9][a-z0-9-]*$" in prompt
    assert "lower-case" in prompt and "underscores into hyphens" in prompt
    pool = [
        "chaocipher",
        "centroid",
        "base62",
        "dijkstra",
        "nthprime",
        "windscale",
        "bell",
        "tapcode",
        "decimaltime",
        "numwords",
        "code39",
        "solids",
    ]
    for name in pool:
        assert SEGMENT_ID_RE.fullmatch(name), f"pool module name {name} violates the id rule"


def test_prompt_mutable_mentions_are_consistent():
    """revise/overwrite may only appear in the never-overwrite direction;
    placeholder must be gone with the old write-later-then-revise flow."""
    prompt = _lead_prompt()
    assert "placeholder" not in prompt.lower()
    for line in prompt.splitlines():
        for word in ("revise", "overwrite", "update"):
            for _ in re.finditer(word, line, flags=re.IGNORECASE):
                context = line.strip().lower()
                assert (
                    "never overwrite" in context or "never update" in context
                ), f"inconsistent {word!r} mention: {line.strip()!r}"


def test_prompt_has_no_tool_budget_for_plan_write():
    """The old 'at most 8 tool calls before the final plan write' budget is gone."""
    assert "Be efficient: at most" not in _lead_prompt()


def test_workflow_stitch_step_ordered_before_validate():
    yml = _team_yml()
    stitch = yml.index("Stitch segments into team-plan.json (single source)")
    validate = yml.index("- name: Validate plan, file [计划] issue and sub-issues")
    assert stitch < validate
    stitch_step = yml[stitch:validate]
    assert "lead_plan_segments.py stitch" in stitch_step
    gate_step = yml[validate : yml.index("- name: Post plan dispatch comment")]
    assert "lead_plan_segments.py assert-ready" in gate_step


def test_workflow_team_plan_reads_come_after_stitch():
    """Static compatibility: every lead-job read of team-plan.json textually
    follows the stitch step (later steps or downstream jobs download it)."""
    yml = _team_yml()
    stitch = yml.index("Stitch segments into team-plan.json (single source)")
    for m in re.finditer(r'json\.load\(open\("team-plan\.json"\)\)', yml):
        assert m.start() > stitch, "team-plan.json read located before the stitch step"
