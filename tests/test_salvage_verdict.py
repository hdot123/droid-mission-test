"""salvage_verdict: the incremental per-process verdict writer (52B fix side).

Locks the write discipline the validator prompt mandates: one process, one
write, immediately after its analysis finishes; the file survives and stays
readable no matter when the session dies.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from salvage_verdict import PARTIAL_NAME, read_salvage, record_verdict  # noqa: E402
from salvage_verdict import salvage_verdict  # noqa: E402


def test_record_then_read_roundtrip(tmp_path: Path):
    out = record_verdict(
        tmp_path, pid="dijkstra", verdict="pass", reason="spec and tests line up"
    )
    assert out["analyzed_count"] == 1
    doc = read_salvage(tmp_path)
    assert doc is not None
    assert doc["processes"] == [
        {"id": "dijkstra", "verdict": "pass", "reason": "spec and tests line up"}
    ]


def test_one_write_per_process_appends_sorted(tmp_path: Path):
    record_verdict(tmp_path, pid="windscale", verdict="fail", reason="red check")
    record_verdict(tmp_path, pid="bell", verdict="pass", reason="clean")
    record_verdict(tmp_path, pid="tapcode", verdict="pass", reason="clean")
    doc = read_salvage(tmp_path)
    assert [p["id"] for p in doc["processes"]] == ["bell", "tapcode", "windscale"]
    assert doc["analyzed_count"] == 3


def test_re_record_same_process_overwrites_verdict(tmp_path: Path):
    record_verdict(tmp_path, pid="bell", verdict="pass", reason="first look")
    record_verdict(tmp_path, pid="bell", verdict="fail", reason="red check found later")
    doc = read_salvage(tmp_path)
    assert doc["processes"] == [
        {"id": "bell", "verdict": "fail", "reason": "red check found later"}
    ]
    assert doc["analyzed_count"] == 1


def test_round_mismatch_is_not_recovered(tmp_path: Path):
    record_verdict(tmp_path, pid="bell", verdict="pass", reason="r1", round_num=1)
    assert read_salvage(tmp_path, round_num=1) is not None
    assert read_salvage(tmp_path, round_num=2) is None


def test_invalid_verdict_value_rejected(tmp_path: Path):
    with pytest.raises(ValueError):
        salvage_verdict(tmp_path, analyzed={"bell": {"verdict": "maybe", "reason": ""}})
    with pytest.raises(ValueError):
        salvage_verdict(tmp_path, analyzed={"": {"verdict": "pass", "reason": ""}})
    assert not (tmp_path / PARTIAL_NAME).exists()


def test_torn_file_is_ignored_not_fatal(tmp_path: Path):
    (tmp_path / PARTIAL_NAME).write_text("{not json", encoding="utf-8")
    record_verdict(tmp_path, pid="bell", verdict="pass", reason="clean")
    doc = read_salvage(tmp_path)
    assert [p["id"] for p in doc["processes"]] == ["bell"]


def test_schema_error_shape_round_trips(tmp_path: Path):
    record_verdict(tmp_path, pid="bell", verdict="pass", reason="clean")
    doc = json.loads((tmp_path / PARTIAL_NAME).read_text(encoding="utf-8"))
    assert doc["salvage_schema_version"] == "validator-partial.v1"
    assert set(doc) == {
        "salvage_schema_version",
        "round",
        "analyzed_count",
        "processes",
        "conflicts",
    }
