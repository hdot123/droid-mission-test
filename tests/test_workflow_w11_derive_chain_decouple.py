"""W-11: derive must not block chain wall_sync in the same bash run block."""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from compute_validate_conclusion import derive  # noqa: E402
from foreman_run_lib import deep_merge, init_wall, save_wall  # noqa: E402
import wall_sync_job  # noqa: E402


def _verdict_key(wall: dict) -> str:
    return next(k for k in wall["artifacts"] if k.startswith("team-verdict"))


def _sync_validate_chain(wall_path: Path, *, job: str, art_suffix: str) -> None:
    wall = json.loads(wall_path.read_text(encoding="utf-8"))
    art_key = art_suffix if art_suffix in wall.get("artifacts", {}) else _verdict_key(wall)
    complete = bool(wall.get("artifacts", {}).get(art_key, {}).get("complete"))
    result = (wall.get("validation") or {}).get("job_conclusion_derived", "failure")
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
        "true" if complete else "false",
    ]
    try:
        assert wall_sync_job.main() == 0
    finally:
        sys.argv = old_argv


def _jsonschema_available() -> bool:
    # Mirrors foreman_run_lib.validate_with_jsonschema's ImportError guard so the
    # skip matches exactly the condition that flips the wall validator to the
    # stricter fallback (true absence or a None-blocked sys.modules entry).
    try:
        importlib.import_module("jsonschema")
    except ImportError:
        return False
    return True


@pytest.mark.skipif(
    not _jsonschema_available(),
    reason="these walls rely on the jsonschema validator: the fallback validator's W6 rule "
    "is stricter than the schema and rejects adoption_status=failed without run_must_fail "
    "(round-53 lucas bare-venv finding, verify-targeted §5)",
)
@pytest.mark.parametrize(
    "scenario,extra",
    [
        (
            "pre_session_death",
            {
                "budgets": {
                    "session_outcome": {
                        "completion_status": "missing_output",
                        "exit_code": -1,
                    }
                },
                "validation": {"adoption_status": "failed", "adoption_error": "no_session"},
            },
        ),
        (
            "session_timeout",
            {
                "budgets": {
                    "session_outcome": {
                        "completion_status": "timeout",
                        "exit_code": 124,
                    }
                },
                "validation": {"adoption_status": "failed", "adoption_error": "draft_timeout"},
            },
        ),
    ],
)
def test_validate_derive_nonzero_exit_then_chain_sync(tmp_path: Path, scenario: str, extra: dict):
    """Acceptance: validator death before/ during session still lands chain.validate."""
    wall = init_wall(run_id=f"w11-{scenario}", issue_number=49)
    art_key = _verdict_key(wall)
    wall = deep_merge(
        wall,
        {
            **extra,
            "artifacts": {
                art_key: {"complete": False, "uploaded": False},
            },
        },
    )
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)

    old_argv = sys.argv
    sys.argv = [
        "compute_validate_conclusion",
        "--wall",
        str(wall_path),
    ]
    try:
        rc = __import__("compute_validate_conclusion").main()
    finally:
        sys.argv = old_argv
    assert rc == 1, scenario

    _sync_validate_chain(wall_path, job="validate", art_suffix=art_key)
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    node = synced["chain"]["validate"]
    assert node["result"] == "failure", synced
    assert node["started"] is True
    assert node["chain_facts"]["summary_code"] == "failed"
    assert synced["validation"]["job_conclusion_derived"] == "failure"
    assert node["result"] != "unknown"


def test_workflow_w11_lint_rejects_same_step_derive_and_sync():
    from lint_workflow_wall_exits import derive_chain_sync_not_same_step

    combined = """
      - name: Derive validate job conclusion (W4)
        run: |
          PYTHONPATH=scripts/team python3 scripts/team/compute_validate_conclusion.py
          PYTHONPATH=scripts/team python3 scripts/team/wall_sync_job.py --job validate
"""
    errs = derive_chain_sync_not_same_step(combined)
    assert any("W-11" in e for e in errs)


def test_workflow_w11_lint_green_on_team_yml():
    lint = ROOT / "scripts" / "team" / "lint_workflow_wall_exits.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout