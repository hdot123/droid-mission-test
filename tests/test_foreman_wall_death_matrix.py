"""Batch-2 death matrix: every chain seat records failure/timeout on the unified wall."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

import wall_sync_job  # noqa: E402
from assemble_chain_facts import sync_assemble_exit  # noqa: E402
from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402

DEATH_MATRIX = (
    ("lead", "failure"),
    ("lead", "cancelled"),
    ("worker", "failure"),
    ("worker", "cancelled"),
    ("worker", "skipped"),
    ("prep", "failure"),
    ("validate", "failure"),
    ("replan", "cancelled"),
    ("worker2", "cancelled"),
    ("prep2", "failure"),
    ("assemble", "failure"),
)


@pytest.mark.parametrize("job,result", DEATH_MATRIX)
def test_chain_seat_records_non_success_exit(tmp_path: Path, job: str, result: str):
    wall = init_wall(run_id="dm", issue_number=48)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    if job == "assemble":
        merged = sync_assemble_exit(wall, job_result=result, produced_required_artifact=False)
        save_wall(merged, wall_path)
    else:
        old_argv = sys.argv
        sys.argv = [
            "wall_sync_job",
            "--wall",
            str(wall_path),
            "--job",
            job,
            "--result",
            result,
            "--produced",
            "false",
        ]
        try:
            assert wall_sync_job.main() == 0
        finally:
            sys.argv = old_argv
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    node = synced["chain"][job]
    assert node["result"] == result, node
    if result == "skipped":
        assert node["started"] is False
        assert node["chain_facts"]["summary_code"] == "not_started"
    else:
        assert node["started"] is True
        assert node["chain_facts"]["summary_code"] in ("failed", "cancelled")
    schema_errs = validate_with_jsonschema(synced)
    assert not schema_errs, schema_errs


def test_w9_lead_session_death_wall_not_left_at_init_snapshot(tmp_path: Path):
    """W-9: lead failure must land on wall even without team-plan.json (no success-only skip)."""
    wall = init_wall(run_id="48a", issue_number=900)
    assert wall["chain"]["lead"]["result"] == "unknown"
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    old_argv = sys.argv
    sys.argv = [
        "wall_sync_job",
        "--wall",
        str(wall_path),
        "--job",
        "lead",
        "--result",
        "failure",
        "--produced",
        "false",
    ]
    try:
        assert wall_sync_job.main() == 0
    finally:
        sys.argv = old_argv
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    assert synced["chain"]["lead"]["result"] == "failure"
    assert synced["chain"]["lead"]["produced_required_artifact"] is False
    assert synced["chain"]["lead"]["chain_facts"]["summary_code"] == "failed"
    assert synced["chain"]["lead"]["result"] != "unknown"


def test_assemble_exit_does_not_backfill_unknown_seats(tmp_path: Path):
    wall = init_wall(run_id="dm2", issue_number=1)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    merged = sync_assemble_exit(wall, job_result="success", produced_required_artifact=True)
    save_wall(merged, wall_path)
    data = json.loads(wall_path.read_text(encoding="utf-8"))
    assert data["chain"]["assemble"]["result"] == "success"
    assert data["chain"]["worker"]["result"] == "unknown"
    assert data["chain"]["prep"]["result"] == "unknown"


def test_workflow_wall_exit_lint_green():
    lint = ROOT / "scripts" / "team" / "lint_workflow_wall_exits.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout
