"""Regression tests for ForemanRun wall failure paths (live round 47 / W-1–W-4)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from foreman_run_lib import (  # noqa: E402
    chain_summary_code_for_result,
    init_wall,
    parse_project_item_list,
    save_wall,
    validate_with_jsonschema,
)
import project_state_write  # noqa: E402
import wall_sync_job  # noqa: E402
import write_worker_delta  # noqa: E402


def test_w1_parse_project_item_list_dict_items():
    payload = {"items": [{"id": "PVTI_1", "content": {"number": 630}}], "totalCount": 1}
    items = parse_project_item_list(payload)
    assert len(items) == 1
    assert items[0]["content"]["number"] == 630


def test_w1_parse_project_item_list_not_empty_for_gh_json_shape():
    """Operator-precedence bug made dict payloads always yield []."""
    raw = json.dumps({"items": [{"id": "x", "content": {"number": 1}}]})
    data = json.loads(raw)
    assert parse_project_item_list(data) != []


def test_w1_find_item_reads_items_from_dict():
    calls = {"n": 0}

    def fake_gh(args, token):
        calls["n"] += 1
        if calls["n"] == 1:
            body = json.dumps({"items": [{"id": "ITEM1", "content": {"number": 633}}]})
            return subprocess.CompletedProcess(args, 0, body, "")
        body = json.dumps({"id": "PVT_proj"})
        return subprocess.CompletedProcess(args, 0, body, "")

    with patch.object(project_state_write, "_gh", fake_gh):
        item_id, project_id = project_state_write.find_item_and_project(
            "hdot123", 33, 633, "token"
        )
    assert item_id == "ITEM1"
    assert project_id == "PVT_proj"


def test_w2_board_write_fail_omits_null_enum(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    wall = init_wall(run_id="47a", issue_number=630)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)

    def boom(*_a, **_k):
        raise RuntimeError("issue #630 not linked to project #33")

    monkeypatch.setenv("PROJECTS_STATE_PAT", "fake-pat")
    monkeypatch.setenv("GITHUB_REPOSITORY", "hdot123/droid-mission-test")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "project_state_write",
            "--wall",
            str(wall_path),
            "--overall",
            "fail",
            "--issue",
            "630",
        ],
    )
    with patch.object(project_state_write, "find_item_and_project", boom):
        rc = project_state_write.main()
    assert rc == 1
    patched = json.loads(wall_path.read_text(encoding="utf-8"))
    closeout = patched["closeout"]
    assert closeout["project_state_written"] is False
    assert closeout.get("run_must_fail") is True
    assert "project_state_enum" not in closeout
    assert not validate_with_jsonschema(patched), validate_with_jsonschema(patched)


def test_w3_wall_sync_maps_failure_to_summary_failed(tmp_path: Path):
    wall = init_wall(run_id="47b", issue_number=631)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(wall, wall_path)
    monkeypatch_argv = [
        "wall_sync_job",
        "--wall",
        str(wall_path),
        "--job",
        "worker",
        "--result",
        "failure",
        "--produced",
        "false",
    ]
    old_argv = sys.argv
    sys.argv = monkeypatch_argv
    try:
        assert wall_sync_job.main() == 0
    finally:
        sys.argv = old_argv
    synced = json.loads(wall_path.read_text(encoding="utf-8"))
    node = synced["chain"]["worker"]
    assert node["result"] == "failure"
    assert node["chain_facts"]["summary_code"] == "failed"
    assert chain_summary_code_for_result("failure") == "failed"
    assert not validate_with_jsonschema(synced), validate_with_jsonschema(synced)


def test_w4_worker_delta_respects_job_status_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("JOB_STATUS", "failure")
    out = tmp_path / "worker-delta.json"
    monkeypatch.setattr(
        sys,
        "argv",
        ["write_worker_delta", "--pid", "hashtable", "--result", "success", "--out", str(out)],
    )
    assert write_worker_delta.main() == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["result"] == "failure"


def test_w4_worker_delta_timeout_style_failure_without_marker(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Matrix leaf defaults RESULT=success; JOB_STATUS=failure must flip delta (round 47-B)."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("JOB_STATUS", "failure")
    out = tmp_path / "delta.json"
    env = {**os.environ, "JOB_STATUS": "failure"}
    r = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "team" / "write_worker_delta.py"),
            "--pid",
            "p0",
            "--result",
            "success",
            "--out",
            str(out),
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert json.loads(out.read_text())["result"] == "failure"