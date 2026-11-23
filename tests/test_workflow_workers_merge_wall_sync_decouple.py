"""N-1/N-2: worker merge re-run must not block chain wall_sync in the same bash run block."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from lint_workflow_wall_exits import (  # noqa: E402
    derive_chain_sync_not_same_step,
    job_spans,
    step_chunks,
)

WORKFLOW = ROOT / ".github/workflows/team.yml"


def _job_text(name: str) -> str:
    text = WORKFLOW.read_text(encoding="utf-8")
    spans = job_spans(text)
    start, end = spans[name]
    return text[start:end]


@pytest.mark.parametrize(
    "job, sync_step_name",
    [
        ("workers-wall-merge", "Sync worker chain seat from wall (W-11 / N-1)"),
        ("workers2-wall-merge", "Sync worker2 chain seat from wall (W-11 / N-2)"),
    ],
)
def test_workers_wall_merge_step_order(job: str, sync_step_name: str):
    """Acceptance: prepare → re-merge → sync are separate steps with sync under always()."""
    job_text = _job_text(job)
    chunks = step_chunks(job_text)
    step_names = [re.search(r"name:\s*(.+)", c).group(1).strip() for c in chunks if re.search(r"name:\s*(.+)", c)]
    assert any("Prepare foreman-run" in n for n in step_names)
    assert any("Re-merge" in n and "deltas" in n for n in step_names)
    assert any(sync_step_name in n for n in step_names)
    idx_sync = next(i for i, n in enumerate(step_names) if sync_step_name in n)
    idx_remerge = next(i for i, n in enumerate(step_names) if "Re-merge" in n)
    assert idx_remerge < idx_sync
    sync_chunk = chunks[idx_sync]
    assert "wall_sync_job.py" in sync_chunk
    assert "merge_worker_deltas.py" not in sync_chunk
    assert "if: always()" in sync_chunk


def test_lint_rejects_merge_redo_and_worker_sync_same_step():
    combined = """
      - name: Record worker job exit on ForemanRun wall
        run: |
          PYTHONPATH=scripts/team python3 scripts/team/merge_worker_deltas.py --wall foreman-run.json
          PYTHONPATH=scripts/team python3 scripts/team/wall_sync_job.py --job worker
"""
    errs = derive_chain_sync_not_same_step(combined)
    assert any("merge re-run and wall_sync" in e for e in errs)


def test_lint_green_on_team_yml():
    lint = ROOT / "scripts" / "team" / "lint_workflow_wall_exits.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout
