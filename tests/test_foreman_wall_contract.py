"""Contract tests for ForemanRun wall (v2.7 machine gates)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from foreman_run_lib import (  # noqa: E402
    init_wall,
    merge_worker_slice,
    prep_should_run,
    save_wall,
    validate_schema,
    validate_with_jsonschema,
)
from compute_replan_gate import compute as compute_replan  # noqa: E402
from compute_validate_conclusion import derive as derive_validate  # noqa: E402
from merge_worker_deltas import apply_deltas  # noqa: E402


def test_env_hard_fail_forbids_ok_true():
    wall = init_wall(run_id="1", issue_number=9)
    wall["env"]["hard_fail_count"] = 1
    wall["env"]["ok"] = True
    errs = validate_schema(wall)
    assert any("hard_fail_count" in e for e in errs)


def test_forbidden_replan_string_lint():
    lint = ROOT / "scripts" / "team" / "lint_workflow_foreman.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout


def test_gh_project_parse_lint_in_contract_gate():
    lint = ROOT / "scripts" / "team" / "lint_gh_project_parse.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout


def test_workflow_budget_lint_in_contract_gate():
    lint = ROOT / "scripts" / "team" / "lint_workflow_budgets.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout


def test_half_artifact_not_complete():
    wall = init_wall(run_id="99", issue_number=1)
    key = "team-verdict-issue-1-run-99"
    wall["artifacts"][key]["complete"] = False
    wall["artifacts"][key]["missing"] = ["verdict.json"]
    assert not wall["artifacts"][key]["complete"]


def test_replan_reads_wall_not_validate_success():
    wall = init_wall(run_id="2", issue_number=3)
    wall["validation"] = {
        "schema_version": "validation-slice.v1",
        "adoption_status": "ok",
        "overall": "fail",
        "failed_process_ids": ["p1"],
        "unattributed_failure": False,
    }
    wall["artifacts"]["team-verdict-issue-3-run-2"]["complete"] = True
    wall["chain"]["validate"] = {
        "result": "success",
        "started": True,
        "produced_required_artifact": True,
        "downstream_blocker": None,
        "chain_facts": {"summary_code": "ok", "detail": "", "forbidden_phrases": []},
    }
    gated = compute_replan(wall)
    assert gated["replan_gate"]["should_replan"] is True


def test_worker_failed_prep_started_forbids_phrase(tmp_path: Path):
    from assemble_chain_facts import build_facts, pick_fallback_reason  # noqa: E402

    wall = init_wall(run_id="3", issue_number=1)
    wall = merge_worker_slice(wall, "p1", "failure")
    wall["chain"]["prep"]["produced_required_artifact"] = True
    wall["chain"]["prep"]["result"] = "success"
    wall = build_facts(wall, {"worker": "failure", "prep": "success"})
    reason = pick_fallback_reason(wall)
    assert "备料未启动" not in reason


def test_adoption_failed_sets_human_stop(tmp_path: Path):
    wall = init_wall(run_id="4", issue_number=1)
    wall["validation"] = {"adoption_status": "failed", "adoption_error": "missing_draft"}
    merged, conclusion = derive_validate(wall)
    assert merged.get("human_stop") is True
    assert conclusion == "failure"


def test_schema_file_validates_minimal_wall():
    wall = init_wall(run_id="5", issue_number=7)
    errs = validate_with_jsonschema(wall)
    assert not errs, errs


def test_prep_gate_completed_pids():
    wall = init_wall(run_id="6", issue_number=1)
    wall = merge_worker_slice(wall, "a", "cancelled")
    assert prep_should_run(wall) is False
    wall = merge_worker_slice(wall, "b", "success")
    assert prep_should_run(wall) is True


def test_assert_artifact_complete_script(tmp_path: Path):
    wall = init_wall(run_id="7", issue_number=1)
    path = tmp_path / "foreman-run.json"
    save_wall(wall, path)
    script = ROOT / "scripts" / "team" / "assert_artifact_complete.py"
    r = subprocess.run(
        [sys.executable, str(script), "--wall", str(path), "--name", "team-verdict-issue-1-run-7"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1


def test_merge_worker_deltas_union():
    wall = init_wall(run_id="8", issue_number=1)
    wall = apply_deltas(
        wall,
        [
            {"pid": "a", "result": "success"},
            {"pid": "b", "result": "failure"},
            {"pid": "c", "result": "cancelled", "cancel_reason": "job_wall_25m"},
        ],
    )
    w = wall["workers"]
    assert sorted(w["completed_pids"]) == ["a", "b"]
    assert w["cancelled_pids"] == ["c"]
    assert w["any_failed"]
    assert w["any_cancelled"]


def test_validate2_artifact_key_present():
    wall = init_wall(run_id="9", issue_number=2)
    assert "team-verdict2-issue-2-run-9" in wall["artifacts"]


def test_pick_verdict_incomplete_wall_fail_closed(tmp_path: Path):
    from pick_verdict_from_wall import pick  # noqa: E402

    wall = init_wall(run_id="10", issue_number=4)
    key = "team-verdict-issue-4-run-10"
    wall["artifacts"][key]["complete"] = False
    wall["artifacts"][key]["missing"] = ["verdict.json"]
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    dl = tmp_path / "dl"
    dl.mkdir()
    with pytest.raises(SystemExit, match="fail-closed"):
        pick(wall_path, dl, issue_number=4, run_id="10")


def test_pick_verdict_rejects_needs_chain_results(tmp_path: Path):
    from pick_verdict_from_wall import pick  # noqa: E402

    wall = init_wall(run_id="10b", issue_number=4)
    key = "team-verdict-issue-4-run-10b"
    wall["artifacts"][key]["complete"] = True
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    dl = tmp_path / "dl"
    dl.mkdir()
    with pytest.raises(SystemExit, match="chain_results forbidden"):
        pick(
            wall_path,
            dl,
            issue_number=4,
            run_id="10b",
            chain_results={"worker": "success"},
        )


def test_pick_verdict_prefers_wall_over_empty_dl(tmp_path: Path):
    from pick_verdict_from_wall import pick  # noqa: E402

    wall = init_wall(run_id="11", issue_number=5)
    key = "team-verdict-issue-5-run-11"
    wall["artifacts"][key]["complete"] = True
    wall["validation"] = {
        "schema_version": "validation-slice.v1",
        "overall": "fail",
        "adoption_status": "ok",
        "round": 1,
    }
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    dl = tmp_path / "dl"
    dl.mkdir()
    verdict, _candidate, picked, source = pick(
        wall_path, dl, issue_number=5, run_id="11", chain_results={}
    )
    assert picked == 1
    assert source == "wall+artifact"
    assert verdict["overall"] == "fail"


def test_validate_foreman_mode_require_prod(tmp_path: Path):
    script = ROOT / "scripts" / "team" / "validate_foreman_mode.py"
    plan = tmp_path / "plan.json"
    plan.write_text(
        json.dumps({"foreman_mode": "test", "processes": [{"id": "a"}, {"id": "b"}]}),
        encoding="utf-8",
    )
    r = subprocess.run(
        [sys.executable, str(script), "--plan", str(plan), "--mode", "test"],
        capture_output=True,
        text=True,
        env={**dict(os.environ), "FOREMAN_REQUIRE_PROD": "1"},
    )
    assert r.returncode == 1, r.stderr + r.stdout


def test_post_comment_hard_patches_wall(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from post_comment_hard import patch_wall_comment  # noqa: E402

    wall = init_wall(run_id="12", issue_number=3)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    patch_wall_comment(str(wall_path), "plan_dispatch", posted=True)
    patched = json.loads(wall_path.read_text(encoding="utf-8"))
    assert patched["closeout"]["comments"]["plan_dispatch"]["posted"] is True


def test_post_comment_hard_hard_required_fails_on_gh_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Locked issue / missing token surfaces as gh failure → exit 1 when --hard-required (B4)."""
    import post_comment_hard  # noqa: E402

    body = tmp_path / "body.md"
    body.write_text("ping", encoding="utf-8")

    def fake_run(cmd, **kwargs):
        assert cmd[0] == "gh"
        return subprocess.CompletedProcess(cmd, 1, "", "GraphQL: Resource not accessible")

    monkeypatch.setattr(post_comment_hard.subprocess, "run", fake_run)
    monkeypatch.setattr(
        sys,
        "argv",
        ["post_comment_hard", "--issue", "1", "--body-file", str(body), "--hard-required"],
    )
    assert post_comment_hard.main() == 1


def test_workflow_post_comment_hard_steps_set_gh_token():
    lint = ROOT / "scripts" / "team" / "lint_workflow_foreman.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout
    assert "post_comment_hard step missing GH_TOKEN" not in (r.stderr + r.stdout)


def test_workflow_wall_exit_lint_in_contract_gate():
    lint = ROOT / "scripts" / "team" / "lint_workflow_wall_exits.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout