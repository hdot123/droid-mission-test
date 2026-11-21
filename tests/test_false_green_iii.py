"""III-1 / III-2a: fail-closed defaults and worker merge sync gating (red/green per site)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from assemble_chain_facts import build_facts  # noqa: E402
from foreman_run_lib import init_wall, patch_chain_job, save_wall  # noqa: E402
import wall_sync_job  # noqa: E402
import write_worker_delta  # noqa: E402
from lint_workflow_wall_exits import worker_merge_sync_gated  # noqa: E402


def test_iii_2a_worker_delta_unknown_without_job_status(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
  monkeypatch.chdir(tmp_path)
  out = tmp_path / "delta.json"
  monkeypatch.setattr(
      sys,
      "argv",
      ["write_worker_delta", "--pid", "p0", "--result", "unknown", "--out", str(out)],
  )
  assert write_worker_delta.main() == 0
  assert json.loads(out.read_text())["result"] == "unknown"


def test_iii_2a_worker_delta_success_only_with_job_status(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
  monkeypatch.chdir(tmp_path)
  out = tmp_path / "delta.json"
  monkeypatch.setenv("JOB_STATUS", "success")
  monkeypatch.setattr(
      sys,
      "argv",
      ["write_worker_delta", "--pid", "p0", "--result", "unknown", "--out", str(out)],
  )
  assert write_worker_delta.main() == 0
  assert json.loads(out.read_text())["result"] == "success"


def test_iii_2a_legacy_cli_success_without_status_becomes_unknown(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
  monkeypatch.chdir(tmp_path)
  out = tmp_path / "delta.json"
  monkeypatch.delenv("JOB_STATUS", raising=False)
  monkeypatch.setattr(
      sys,
      "argv",
      ["write_worker_delta", "--pid", "p0", "--result", "success", "--out", str(out)],
  )
  assert write_worker_delta.main() == 0
  assert json.loads(out.read_text())["result"] == "unknown"


def test_init_wall_env_ok_default_not_true():
  wall = init_wall(run_id="iii", issue_number=1)
  assert wall["env"]["ok"] is False


def test_env_check_wall_artifact_complete_follows_env_ok(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
  tsv = tmp_path / "env.tsv"
  tsv.write_text("FAIL\t板面配置\tmissing\n", encoding="utf-8")
  out = tmp_path / "foreman-run.json"
  monkeypatch.setenv("S_PROJECTS_STATE_PAT", "1")
  monkeypatch.setenv("S_FACTORY_API_KEY", "1")
  monkeypatch.setenv("S_WORKER_CI_KEY", "1")
  import env_check_wall  # noqa: E402

  monkeypatch.setattr(
      sys,
      "argv",
      [
          "env_check_wall",
          "--results-tsv",
          str(tsv),
          "--issue",
          "1",
          "--run-id",
          "iii",
          "--out",
          str(out),
      ],
  )
  assert env_check_wall.main() == 1
  data = json.loads(out.read_text(encoding="utf-8"))
  assert data["env"]["ok"] is False
  assert data["artifacts"]["foreman-run-iii"]["complete"] is False


def test_assemble_build_facts_unknown_not_ok():
  wall = init_wall(run_id="iii", issue_number=2)
  merged = build_facts(wall, {j: "skipped" for j in wall["chain"]})
  assert merged["chain"]["lead"]["chain_facts"]["summary_code"] == "not_started"
  assert merged["chain"]["lead"]["chain_facts"]["detail"].endswith("未启动")


def test_wall_sync_unknown_keeps_started_false(tmp_path: Path):
  wall = init_wall(run_id="iii", issue_number=3)
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
      "unknown",
      "--produced",
      "false",
  ]
  try:
    assert wall_sync_job.main() == 0
  finally:
    sys.argv = old_argv
  node = json.loads(wall_path.read_text())["chain"]["lead"]
  assert node["result"] == "unknown"
  assert node["started"] is False
  assert node["chain_facts"]["summary_code"] == "not_started"


def test_iii_1_lint_red_when_sync_not_gated():
  bad = """
  workers-wall-merge:
    steps:
      - name: Sync worker chain seat from wall (W-11 / N-1)
        if: always()
        run: |
          python3 wall_sync_job.py --job worker
"""
  errs = worker_merge_sync_gated(bad, {"workers-wall-merge": (0, len(bad))})
  assert any("III-1" in e for e in errs)


def test_prep_unknown_result_not_success_shape(tmp_path: Path):
  wall = init_wall(run_id="iii", issue_number=4)
  merged = patch_chain_job(wall, "prep", result="unknown", produced_required_artifact=False)
  assert merged["chain"]["prep"]["result"] == "unknown"
  assert merged["chain"]["prep"]["produced_required_artifact"] is False
  assert merged["chain"]["prep"]["started"] is False


def test_chain_sync_result_unknown_maps_not_started(tmp_path: Path):
  wall = init_wall(run_id="iii", issue_number=5)
  wall_path = tmp_path / "foreman-run.json"
  save_wall(wall, wall_path)
  old_argv = sys.argv
  sys.argv = [
      "wall_sync_job",
      "--wall",
      str(wall_path),
      "--job",
      "replan",
      "--result",
      "unknown",
      "--produced",
      "false",
  ]
  try:
    assert wall_sync_job.main() == 0
  finally:
    sys.argv = old_argv
  node = json.loads(wall_path.read_text())["chain"]["replan"]
  assert node["result"] == "unknown"
  assert node["chain_facts"]["summary_code"] != "ok"


def test_iii_1_workflow_green_on_team_yml():
  text = (ROOT / ".github/workflows/team.yml").read_text(encoding="utf-8")
  from lint_workflow_wall_exits import job_spans  # noqa: E402

  assert not worker_merge_sync_gated(text, job_spans(text))