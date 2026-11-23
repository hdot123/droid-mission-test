"""52A-type counterexample: escalated conflicts must gate the verdict.

Round 52 A (run 45078438609) death shape: the validator escalated a real
work-order contradiction (chaocipher body-vs-acceptance vector mismatch) into
verdict.json's top-level conflicts array — yet overall stayed a bare,
unannotated "pass". Nothing downstream could distinguish a clean pass from a
pass-with-escalated-contradiction, so the conflict triggered no action.

These tests pin the fix at the single authoritative verdict computation
(scripts/team/adopt_verdict.py): a non-empty conflicts array forces a
"conflicts_escalated" annotation on the verdict — it must never emit a bare
pass again.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from adopt_verdict import adopt  # noqa: E402
from compute_replan_gate import compute  # noqa: E402
from compute_validate_conclusion import derive  # noqa: E402
from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402

_FIXTURES = ROOT / "tests" / "fixtures" / "validator-r52a"
# Real 52A conflicts[0] (run 45078438609), copied verbatim — see provenance.txt.
CHAOCIPHER_CONFLICT = json.loads(
    (_FIXTURES / "conflict-chaocipher.json").read_text(encoding="utf-8")
)


@pytest.fixture()
def r52a_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """A clean round-1 run: all processes pass, merged suite green, one escalated conflict."""
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "work"
    work.mkdir()
    manifest = {"pytest_exit": 0, "iteration": 1}
    plan = {"processes": [{"id": "base62"}, {"id": "centroid"}, {"id": "chaocipher"}]}
    judgeable = ["base62", "centroid", "chaocipher"]
    draft = {
        "processes": [
            {"id": pid, "verdict": "pass", "reason": "five artifacts line up"}
            for pid in judgeable
        ],
        "conflicts": [CHAOCIPHER_CONFLICT],
    }
    (work / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    (work / "judgeable.json").write_text(json.dumps(judgeable), encoding="utf-8")
    (work / "blocked.json").write_text("{}", encoding="utf-8")
    (work / "pytest-output.txt").write_text("199 passed, 1 skipped\n", encoding="utf-8")
    (work / "verdict-droid.json").write_text(json.dumps(draft), encoding="utf-8")
    (work / "verdict-droid.md").write_text("# report\n", encoding="utf-8")
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="r52a", issue_number=761), wall_path)
    return wall_path, work


def test_52a_replay_conflicts_do_not_yield_bare_pass(r52a_env):
    """The exact 52A shape: verdicts all pass, pytest 0, conflicts[0] escalated.

    The verdict must NOT be a bare pass: the escalated work-order contradiction
    demotes overall to fail (matching the repo's existing unattributed-failure
    precedent, where 'all pass but something is wrong' fails the verdict so the
    replan gate can act). A conflicting order is never a silent green."""
    wall_path, work = r52a_env
    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    assert rc == 0
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert verdict["overall"] == "fail"
    assert verdict["conflicts"] == [
        {
            "process": CHAOCIPHER_CONFLICT["process"],
            "summary": CHAOCIPHER_CONFLICT["summary"],
            "evidence": CHAOCIPHER_CONFLICT["evidence"],
        }
    ]
    assert verdict["conflicts_escalated"] is True
    assert verdict["unattributed_failure"] is False
    assert [p["verdict"] for p in verdict["processes"]] == ["pass", "pass", "pass"]
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["conflicts_escalated"] is True


def test_conflicts_annotation_propagates_to_gates(r52a_env):
    """The demotion must be actionable downstream: replan gate reopens the
    order and the validate job conclusion is failure — an escalated
    work-order contradiction is never a silent green."""
    wall_path, work = r52a_env
    adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["conflicts_escalated"] is True
    assert merged["validation"]["overall"] == "fail"

    gate = compute(merged)["replan_gate"]
    assert gate["should_replan"] is True
    assert gate["reasons"] == ["conflicts_escalated"]

    _, conclusion = derive(merged)
    assert conclusion == "failure"
    validate_with_jsonschema(gate)


def test_clean_pass_has_no_conflicts_annotation(r52a_env):
    """No conflicts → no annotation: a clean pass is still a clean pass."""
    wall_path, work = r52a_env
    draft = json.loads((work / "verdict-droid.json").read_text(encoding="utf-8"))
    draft["conflicts"] = []
    (work / "verdict-droid.json").write_text(json.dumps(draft), encoding="utf-8")
    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    assert rc == 0
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert verdict["overall"] == "pass"
    assert verdict["conflicts_escalated"] is False
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    gate = compute(merged)["replan_gate"]
    assert gate["should_replan"] is False


def test_failing_verdict_with_conflicts_stays_fail(r52a_env):
    """Conflicts annotation must not soften a real failure into a pass."""
    wall_path, work = r52a_env
    draft = json.loads((work / "verdict-droid.json").read_text(encoding="utf-8"))
    draft["processes"][1]["verdict"] = "fail"
    draft["processes"][1]["reason"] = "checks-output shows red mandated check"
    (work / "verdict-droid.json").write_text(json.dumps(draft), encoding="utf-8")
    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    assert rc == 0
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert verdict["overall"] == "fail"
    assert verdict["conflicts_escalated"] is True
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    gate = compute(merged)["replan_gate"]
    assert gate["should_replan"] is True


def test_round2_conflicts_also_gate(r52a_env):
    """Round 2 verdicts follow the same rule (the 52A fix covers both rounds)."""
    wall_path, work = r52a_env
    rc = adopt(
        work,
        wall_path,
        droid_exit=0,
        merge_step_ran=True,
        round_num=2,
        round1_verdict=None,
    )
    assert rc == 0
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert verdict["overall"] == "fail"
    assert verdict["conflicts_escalated"] is True


def test_board_status_maps_conflicted_verdict_to_blocked(r52a_env):
    """52A downstream lock: the board write maps a conflicts-demoted verdict
    (overall=fail) to 阻塞 — a contradictory order never lands as 已验收.
    The round-52 A run wrote 已验收 with an escalated chaocipher contradiction;
    under the fix its verdict is fail, so the board must follow."""
    import project_state_write  # noqa: E402

    wall_path, work = r52a_env
    adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert verdict["overall"] == "fail"
    assert verdict["conflicts_escalated"] is True
    assert project_state_write.STATUS_BY_OVERALL["fail"] == "阻塞"


def test_replan_coverage_includes_conflicted_processes():
    """The replan claim-check must require a decision for every conflicted
    process (deterministically, from the verdict's conflicts array) — not
    only the failed ones. A conflicts-only round (failed=∅, one escalated
    conflict) otherwise dead-ends: the prompt says "revise the conflicted
    card" while the coverage check demands changes cover failed=∅ exactly."""
    team_yml = (ROOT / ".github" / "workflows" / "team.yml").read_text(encoding="utf-8")
    # The coverage merge must exist and run on the verdict's conflicts array.
    assert "conflicted = {c.get(\"process\") for c in conflicts" in team_yml
    assert "required |= conflicted" in team_yml
    # The prompt's coverage rule must name conflicted processes, so the
    # instruction and the checker agree (no prompt/checker contradiction).
    assert "conflicted = named in the verdict's conflicts array" in team_yml
    # The foreman decision line must cover revise AND redispatch for conflicts.
    assert "or redispatch with a retry_note stating the card stands as" in team_yml
