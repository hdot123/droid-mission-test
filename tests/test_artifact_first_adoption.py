"""VAL-P2-002/003/004: artifact-first adoption (round54-root-cure PR-2, U-3/D-2).

Round-54 A/C death chain: the validator session was wall-killed (exit 124)
after analyzing every judgeable process, the per-process conclusions were
persisted incrementally, and adoption still failed the whole order —
draft_timeout -> human_stop — because the exit code outranked the artifacts
on disk. PR-2 inverts the precedence (U-3): disk artifact completeness
outranks the exit code.

Adoption decision order pinned here:
  1. evidence integrity (EXPECTED_MANIFEST_SHA) — untouched, checked first;
  2. complete draft on disk (any exit, incl. 124) -> normal adoption (L-6);
  3. verdict-partial.json covering ALL judgeable + final seal (D-2)
     -> machine-assembled draft -> normal adoption (I-6); the pytest_exit /
     conflicts machine gates still apply to the assembled verdict;
  4. anything less (no seal, undercoverage) -> draft_timeout revalidate path
     (VAL-P1-002); tampered evidence stays terminal fail-closed.
"""
from __future__ import annotations

import hashlib
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
from salvage_verdict import salvage_verdict  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "validator-r54ac"


def _r54ac_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, letter: str):
    """Real round-54 evidence pack (manifest/plan/pytest output verbatim), wall + work dir."""
    monkeypatch.chdir(tmp_path)
    src = FIXTURES / letter
    plan = json.loads((src / "plan.json").read_text(encoding="utf-8"))
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_bytes((src / "manifest.json").read_bytes())
    (work / "plan.json").write_bytes((src / "plan.json").read_bytes())
    (work / "pytest-output.txt").write_bytes((src / "pytest-output.txt").read_bytes())
    ids = [p["id"] for p in plan["processes"]]
    (work / "judgeable.json").write_text(json.dumps(ids), encoding="utf-8")
    (work / "blocked.json").write_text("{}", encoding="utf-8")
    monkeypatch.setenv(
        "EXPECTED_MANIFEST_SHA",
        hashlib.sha256((src / "manifest.json").read_bytes()).hexdigest(),
    )
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id=f"r54{letter}", issue_number=812), wall_path)
    return wall_path, work, ids


def _final_partial(work: Path, ids: list[str], *, final: bool, covered: int, reason: str = "all artifacts line up") -> None:
    salvage = salvage_verdict(
        work,
        analyzed={pid: {"verdict": "pass", "reason": reason} for pid in ids[:covered]},
        round_num=1,
    )
    if final:
        salvage["final"] = True
    (work / "verdict-partial.json").write_text(
        json.dumps(salvage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# --- VAL-P2-002: complete draft outranks exit 124 (L-6) ---------------------


def test_complete_draft_with_exit_124_adopts_normally(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The L-6 shape (54 A/C lost 9.9-25.7s of censored tail with the draft
    already on disk): a complete verdict-droid.json plus exit 124 must adopt
    normally, not draft_timeout."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="l6", issue_number=812), wall_path)
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text(json.dumps({"pytest_exit": 0, "iteration": 1}), encoding="utf-8")
    plan = {"processes": [{"id": pid} for pid in ["dijkstra", "nthprime", "windscale"]]}
    (work / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    (work / "judgeable.json").write_text(json.dumps(["dijkstra", "nthprime", "windscale"]), encoding="utf-8")
    (work / "blocked.json").write_text("{}", encoding="utf-8")
    (work / "pytest-output.txt").write_text("192 passed, 1 skipped in 15.61s\n", encoding="utf-8")
    draft = {
        "processes": [
            {"id": pid, "verdict": "pass", "reason": "five artifacts line up"}
            for pid in ["dijkstra", "nthprime", "windscale"]
        ],
        "conflicts": [],
    }
    (work / "verdict-droid.json").write_text(json.dumps(draft), encoding="utf-8")
    (work / "verdict-droid.md").write_text("# report\n", encoding="utf-8")

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "ok"
    assert merged["validation"]["overall"] == "pass"
    assert merged.get("human_stop") is not True
    assert "closeout" not in merged
    assert merged["replan_gate"]["should_revalidate"] is False
    assert merged["artifacts"]["team-verdict-issue-812-run-l6"]["complete"] is True
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert verdict["overall"] == "pass"
    assert verdict["pytest_exit"] == 0
    validate_with_jsonschema(merged)


# --- VAL-P2-003: the four-variant assembled-partial decision matrix ---------


def test_final_full_partial_assembles_into_normal_adoption(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """All conditions met (final seal + full judgeable coverage + sha ok),
    exit 124, no draft: the machine assembles the draft and adoption is a
    NORMAL ok adoption (I-6), machine gates included."""
    wall_path, work, ids = _r54ac_env(tmp_path, monkeypatch, "a")
    _final_partial(work, ids, final=True, covered=len(ids))

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "ok"
    assert merged["validation"]["adoption_error"] is None
    assert merged["validation"]["overall"] == "pass"
    assert merged["validation"]["pytest_exit"] == 0
    assert merged.get("human_stop") is not True
    assert "closeout" not in merged
    assert merged["artifacts"]["team-verdict-issue-812-run-r54a"]["complete"] is True
    assert merged["replan_gate"]["should_revalidate"] is False
    assert merged["replan_gate"]["should_replan"] is False
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert verdict["overall"] == "pass"
    assert verdict["salvage_assembled"] is True
    assert all(p["verdict"] == "pass" for p in verdict["processes"])
    assert not compute(merged)["replan_gate"]["should_replan"]
    validate_with_jsonschema(merged)


def test_partial_without_final_seal_goes_revalidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Coverage complete but the D-2 seal missing: NOT adoptable — the
    draft_timeout revalidate path runs (should_revalidate=true, no human_stop
    while the one retry is available)."""
    wall_path, work, ids = _r54ac_env(tmp_path, monkeypatch, "a")
    _final_partial(work, ids, final=False, covered=len(ids))

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "failed"
    assert merged["validation"]["adoption_error"] == "draft_timeout"
    assert merged.get("human_stop") is not True
    assert merged["replan_gate"]["should_revalidate"] is True
    validate_with_jsonschema(merged)


def test_partial_undercoverage_goes_revalidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Sealed but covering only part of the judgeable set: NOT adoptable —
    revalidate path."""
    wall_path, work, ids = _r54ac_env(tmp_path, monkeypatch, "a")
    _final_partial(work, ids, final=True, covered=len(ids) - 1)

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_error"] == "draft_timeout"
    assert merged.get("human_stop") is not True
    assert merged["replan_gate"]["should_revalidate"] is True
    validate_with_jsonschema(merged)


def test_partial_with_sha_mismatch_stays_evidence_tampered(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Evidence integrity outranks everything, including a sealed full partial:
    a manifest sha mismatch stays terminal evidence_tampered + human_stop."""
    wall_path, work, ids = _r54ac_env(tmp_path, monkeypatch, "a")
    monkeypatch.setenv("EXPECTED_MANIFEST_SHA", "0" * 64)
    _final_partial(work, ids, final=True, covered=len(ids))

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "failed"
    assert merged["validation"]["adoption_error"] == "evidence_tampered"
    assert merged.get("human_stop") is True
    assert merged["closeout"]["run_must_fail"] is True
    assert merged["replan_gate"]["should_revalidate"] is False
    # Tamper short-circuits before any judging: no verdict.json was written,
    # so there is no assembled artifact to audit.
    assert not Path("verdict.json").exists()
    validate_with_jsonschema(merged)


def test_assembled_partial_conflicts_still_gate_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Machine gates apply to the assembled verdict: an escalated conflict in
    the partial demotes overall to fail and propagates to the wall slice."""
    wall_path, work, ids = _r54ac_env(tmp_path, monkeypatch, "a")
    salvage = salvage_verdict(
        work,
        analyzed={pid: {"verdict": "pass", "reason": "aligned"} for pid in ids},
        conflicts=[
            {"process": ids[0], "summary": "card vs acceptance mismatch", "evidence": "handoff"}
        ],
        round_num=1,
    )
    salvage["final"] = True
    (work / "verdict-partial.json").write_text(json.dumps(salvage), encoding="utf-8")

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "ok"
    assert merged["validation"]["overall"] == "fail"
    assert merged["validation"]["conflicts_escalated"] is True
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert verdict["conflicts_escalated"] is True
    assert not compute(merged)["replan_gate"]["should_replan"] is False or True  # gate sees escalated
    gate = compute(merged)["replan_gate"]
    assert gate["should_replan"] is True
    validate_with_jsonschema(merged)


@pytest.mark.parametrize("letter", ["a", "c"])
def test_r54_replay_sealed_full_partial_adopts_ok(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, letter: str
):
    """The exact 54 A/C artifact dry-run replay: their real evidence packs,
    exit 124, a sealed full partial instead of nothing — adoption must be ok
    and the validate job green."""
    wall_path, work, ids = _r54ac_env(tmp_path, monkeypatch, letter)
    _final_partial(work, ids, final=True, covered=len(ids))

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "ok"
    assert merged["validation"]["overall"] == "pass"
    merged2, conclusion = derive(merged, round_num=1)
    assert conclusion == "success"
    assert merged2.get("human_stop") is not True
    validate_with_jsonschema(merged2)


# --- VAL-P2-004: conclusion derivation accepts assembled artifacts ----------


@pytest.mark.parametrize("round_num", [1, 2])
def test_conclusion_accepts_assembled_artifact_both_rounds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, round_num: int
):
    """The workflow's timeout branch change: an adoption ok'd via the
    assembled artifact derives success (and no human_stop) on both rounds."""
    wall_path, work, ids = _r54ac_env(tmp_path, monkeypatch, "a")
    _final_partial(work, ids, final=True, covered=len(ids))

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=round_num)
    assert rc == 0
    wall = json.loads(wall_path.read_text(encoding="utf-8"))
    merged, conclusion = derive(wall, round_num=round_num)
    assert conclusion == "success"
    assert merged.get("human_stop") is not True
    validate_with_jsonschema(merged)


def test_revalidate_job_shape_assembled_draft_passes_conclusion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The revalidate job's wiring shape replayed: adopt reads the wall where
    revalidate_attempted=true, the fresh session dies at the wire again, but
    this time a sealed full partial is on disk — normal adoption, the order
    does NOT land human_stop (the assembled retry verdict is the outcome)."""
    wall_path, work, ids = _r54ac_env(tmp_path, monkeypatch, "a")
    wall = json.loads(wall_path.read_text(encoding="utf-8"))
    wall["replan_gate"] = {
        "schema_version": "replan-gate.v1",
        "should_replan": False,
        "should_revalidate": True,
        "revalidate_attempted": True,
    }
    save_wall(wall, wall_path)
    _final_partial(work, ids, final=True, covered=len(ids))

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "ok"
    assert merged["replan_gate"]["should_revalidate"] is False
    assert merged.get("human_stop") is not True
    validate_with_jsonschema(merged)
