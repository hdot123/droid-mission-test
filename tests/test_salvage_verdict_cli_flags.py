"""VAL-P2-001: recorder CLI grows --conflict (repeatable) and --final (the
D-2 seal), and main() passes conflicts through to record_verdict.

D-2 (user ruling): an assemblable partial must carry an explicit final seal
so a machine can tell "the validator finished judging and this partial is the
deliverable" apart from "the session died mid-analysis". The seal only makes
sense together with full coverage, which the adopt side checks.
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from salvage_verdict import PARTIAL_NAME, read_salvage  # noqa: E402


def _run(work: Path, argv: list[str]) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONPATH": str(ROOT / "scripts" / "team")}
    return subprocess.run(
        argv, cwd=work, env=env, capture_output=True, text=True, timeout=30
    )


def _argv(work: Path, extra: str) -> list[str]:
    base = (
        f"python3 -m salvage_verdict --work-dir {shlex.quote(str(work))} "
        f"--process dijkstra --verdict pass --reason aligned"
    )
    return shlex.split(base + " " + extra)


def test_cli_accepts_repeatable_conflict_flags(tmp_path: Path):
    proc = _run(
        tmp_path,
        _argv(
            tmp_path,
            "--conflict dijkstra|card-vs-acceptance|handoff.md --conflict windscale|body-vs-checks|status.json",
        ),
    )
    assert proc.returncode == 0, proc.stderr
    doc = json.loads((tmp_path / PARTIAL_NAME).read_text(encoding="utf-8"))
    assert doc["conflicts"] == [
        {"process": "dijkstra", "summary": "card-vs-acceptance", "evidence": "handoff.md"},
        {"process": "windscale", "summary": "body-vs-checks", "evidence": "status.json"},
    ]
    salvaged = read_salvage(tmp_path)
    assert salvaged is not None and len(salvaged["conflicts"]) == 2


def test_cli_final_seal_lands_in_partial_file(tmp_path: Path):
    proc = _run(tmp_path, _argv(tmp_path, "--final"))
    assert proc.returncode == 0, proc.stderr
    doc = json.loads((tmp_path / PARTIAL_NAME).read_text(encoding="utf-8"))
    assert doc["final"] is True
    assert read_salvage(tmp_path)["final"] is True


def test_cli_without_final_has_no_seal_key(tmp_path: Path):
    proc = _run(tmp_path, _argv(tmp_path, ""))
    assert proc.returncode == 0, proc.stderr
    doc = json.loads((tmp_path / PARTIAL_NAME).read_text(encoding="utf-8"))
    assert not doc.get("final")


def test_record_verdict_seal_survives_second_write(tmp_path: Path):
    """The seal is not lost when the validator records one more process after
    sealing (late recorder calls must keep the partial adoptable)."""
    from salvage_verdict import record_verdict

    record_verdict(tmp_path, pid="dijkstra", verdict="pass", reason="ok", final=True)
    record_verdict(tmp_path, pid="nthprime", verdict="fail", reason="red check")
    doc = read_salvage(tmp_path)
    assert doc["final"] is True
    assert [p["id"] for p in doc["processes"]] == ["dijkstra", "nthprime"]


def test_re_record_process_without_seal_keeps_existing_seal(tmp_path: Path):
    from salvage_verdict import record_verdict

    record_verdict(tmp_path, pid="dijkstra", verdict="pass", reason="ok", final=True)
    record_verdict(tmp_path, pid="dijkstra", verdict="fail", reason="found red")
    doc = read_salvage(tmp_path)
    assert doc["final"] is True
    assert doc["processes"][0]["verdict"] == "fail"


def test_conflicts_merge_across_writes(tmp_path: Path):
    from salvage_verdict import record_verdict

    record_verdict(
        tmp_path,
        pid="dijkstra",
        verdict="pass",
        reason="ok",
        conflicts=[{"process": "dijkstra", "summary": "s1", "evidence": "e1"}],
    )
    record_verdict(
        tmp_path,
        pid="nthprime",
        verdict="pass",
        reason="ok",
        conflicts=[{"process": "nthprime", "summary": "s2", "evidence": "e2"}],
    )
    doc = read_salvage(tmp_path)
    assert {c["process"] for c in doc["conflicts"]} == {"dijkstra", "nthprime"}
