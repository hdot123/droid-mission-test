"""VAL-P3-001: the S-2 machine gates — checks-exit.json non-zero (exit 127
exception kept) and a red-by-content checks-failed.marker — live on the
adopt side, so a red mandated check can never ride a pass through adoption
even when the validator's verdict says pass (HARD RULE no longer rests on
model obedience).

The marker gate is judged by CONTENT (marker_verdict, M3 scrutiny round-1
BLK-1): the verify step records missing deliverables in the same marker as
red checks, and prep's checks-exit.json is the green authority — only a
genuinely red marker (non-zero check exit / malformed status / unparseable
bytes) fails the process; a missing-file-only marker with all-0 exits does
not (covered end to end in tests/test_salvage_marker_content.py).

Three-state pin per gate (red / green / 127 exception), plus the fail-closed
corner cases:
- red exit + pass verdict -> fail (machine override), reason names the gate;
- all exits zero + no marker -> pass untouched;
- exit 127 (pytest unavailable at prep) -> NOT red, verdict stands;
- unreadable/malformed checks-exit.json -> red (fail-closed);
- gates apply identically on the machine-assembled partial path (I-6).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from adopt_verdict import adopt, machine_gate_reds  # noqa: E402
from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402
from salvage_verdict import salvage_verdict  # noqa: E402

IDS = ["dijkstra", "nthprime", "windscale"]


def _env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, manifest: dict | None = None):
    """Minimal complete evidence environment (sha unpinned -> adoption passes
    integrity; pytest_exit 0 so only the pack gates can turn the round red)."""
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "work"
    work.mkdir()
    manifest = manifest or {"pytest_exit": 0, "iteration": 1}
    (work / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work / "plan.json").write_text(
        json.dumps({"processes": [{"id": pid} for pid in IDS]}), encoding="utf-8"
    )
    (work / "judgeable.json").write_text(json.dumps(IDS), encoding="utf-8")
    (work / "blocked.json").write_text("{}", encoding="utf-8")
    (work / "pytest-output.txt").write_text("192 passed in 15.61s\n", encoding="utf-8")
    draft = {
        "processes": [
            {"id": pid, "verdict": "pass", "reason": "five artifacts line up"}
            for pid in IDS
        ],
        "conflicts": [],
    }
    (work / "verdict-droid.json").write_text(json.dumps(draft), encoding="utf-8")
    (work / "verdict-droid.md").write_text("# report\n", encoding="utf-8")
    for pid in IDS:
        (work / "packs" / pid).mkdir(parents=True)
        (work / "packs" / pid / "checks-exit.json").write_text("[]", encoding="utf-8")
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="p3", issue_number=812), wall_path)
    return wall_path, work


# --- checks-exit.json gate: red / green / 127 exception ----------------------


def test_red_exit_overrides_pass_verdict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """A non-zero entry in checks-exit.json makes the process fail even when
    the validator judged pass — the model's word is no longer the gate."""
    wall_path, work = _env(tmp_path, monkeypatch)
    (work / "packs" / IDS[0] / "checks-exit.json").write_text(
        json.dumps([{"command": "pytest tests/test_x.py -q", "exit": 1}]),
        encoding="utf-8",
    )

    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    assert rc == 0
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in verdict["processes"]}
    assert by_id[IDS[0]]["verdict"] == "fail"
    assert "checks-exit.json" in by_id[IDS[0]]["reason"]
    assert by_id[IDS[1]]["verdict"] == "pass" and by_id[IDS[2]]["verdict"] == "pass"
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "ok"
    assert merged["validation"]["overall"] == "fail"
    assert merged["validation"]["failed_process_ids"] == [IDS[0]]
    assert not merged.get("human_stop")
    validate_with_jsonschema(merged)


def test_green_exits_and_no_marker_keep_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """All exits zero, no marker: the gates are silent and the verdict stands."""
    wall_path, work = _env(tmp_path, monkeypatch)
    (work / "packs" / IDS[0] / "checks-exit.json").write_text(
        json.dumps([{"command": "a", "exit": 0}, {"command": "b", "exit": 0}]),
        encoding="utf-8",
    )

    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    assert rc == 0
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert all(p["verdict"] == "pass" for p in verdict["processes"])
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["overall"] == "pass"
    validate_with_jsonschema(merged)


def test_exit_127_pytest_unavailable_is_not_red(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The kept exception: exit 127 recorded because pytest was unavailable at
    prep is an environment failure, not a red mandated check — the validator's
    pass stands (its verdict judges the pack via the manifest evidence)."""
    wall_path, work = _env(tmp_path, monkeypatch)
    (work / "packs" / IDS[0] / "checks-exit.json").write_text(
        json.dumps([{"command": "pytest -q", "exit": 127}]), encoding="utf-8"
    )

    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    assert rc == 0
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert all(p["verdict"] == "pass" for p in verdict["processes"])
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["overall"] == "pass"
    validate_with_jsonschema(merged)


def test_unreadable_checks_exit_is_red_fail_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """A checks-exit.json that cannot be parsed (truncated write, tamper) is
    treated as red — an unreadable gate must never read as green."""
    wall_path, work = _env(tmp_path, monkeypatch)
    (work / "packs" / IDS[1] / "checks-exit.json").write_text("{oops", encoding="utf-8")

    reds = machine_gate_reds(work, IDS)
    assert reds[IDS[1]] and "不可读" in reds[IDS[1]]

    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in verdict["processes"]}
    assert by_id[IDS[1]]["verdict"] == "fail"


def test_malformed_exit_entries_are_red_fail_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Entries without an integer 'exit' field cannot prove green — red."""
    wall_path, work = _env(tmp_path, monkeypatch)
    (work / "packs" / IDS[2] / "checks-exit.json").write_text(
        json.dumps([{"command": "a"}]), encoding="utf-8"
    )

    reds = machine_gate_reds(work, IDS)
    assert reds[IDS[2]] and "不可读" in reds[IDS[2]]


def test_missing_checks_exit_with_no_exit_field_is_green(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """No exit field in the manifest and no file: nothing to gate on (the
    pre-S-2 evidence shape), the verdict stands."""
    wall_path, work = _env(tmp_path, monkeypatch)
    for pid in IDS:
        (work / "packs" / pid / "checks-exit.json").unlink()

    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert all(p["verdict"] == "pass" for p in verdict["processes"])


# --- checks-failed.marker gate ----------------------------------------------


def test_marker_presence_overrides_pass_verdict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """A checks-failed.marker whose content reads RED fails the process
    regardless of the validator's pass verdict."""
    wall_path, work = _env(tmp_path, monkeypatch)
    (work / "packs" / IDS[2] / "checks-failed.marker").write_text(
        "checks failed\n", encoding="utf-8"
    )

    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    assert rc == 0
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in verdict["processes"]}
    assert by_id[IDS[2]]["verdict"] == "fail"
    assert "checks-failed.marker" in by_id[IDS[2]]["reason"]
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["overall"] == "fail"
    assert merged["validation"]["failed_process_ids"] == [IDS[2]]
    validate_with_jsonschema(merged)


def test_marker_red_beats_exit_127_exception(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Red-by-content marker and 127 together: the marker alone is red; the
    127 exception does not launder it."""
    wall_path, work = _env(tmp_path, monkeypatch)
    (work / "packs" / IDS[0] / "checks-exit.json").write_text(
        json.dumps([{"command": "pytest -q", "exit": 127}]), encoding="utf-8"
    )
    (work / "packs" / IDS[0] / "checks-failed.marker").write_text("x", encoding="utf-8")

    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in verdict["processes"]}
    assert by_id[IDS[0]]["verdict"] == "fail"


# --- gate placement: both adoption routes and the fail path -----------------


def test_gates_apply_to_machine_assembled_partial_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """I-6 route: exit 124 with a sealed full partial — the assembled draft
    enters the SAME gate path, so a red check still fails the process."""
    wall_path, work = _env(tmp_path, monkeypatch)
    (work / "verdict-droid.json").unlink()
    (work / "verdict-droid.md").unlink()
    salvage = salvage_verdict(
        work,
        analyzed={pid: {"verdict": "pass", "reason": "aligned"} for pid in IDS},
        round_num=1,
    )
    salvage["final"] = True
    (work / "verdict-partial.json").write_text(json.dumps(salvage), encoding="utf-8")
    (work / "packs" / IDS[1] / "checks-exit.json").write_text(
        json.dumps([{"command": "c", "exit": 2}]), encoding="utf-8"
    )

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    assert rc == 0
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in verdict["processes"]}
    assert verdict["salvage_assembled"] is True
    assert by_id[IDS[1]]["verdict"] == "fail"
    assert verdict["overall"] == "fail"
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "ok"
    assert merged["validation"]["overall"] == "fail"
    validate_with_jsonschema(merged)


def test_fail_verdict_with_red_gate_stays_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Red gate + a verdict that already says fail: still fail, and the
    machine reason replaces the model's (the gate evidence is authoritative)."""
    wall_path, work = _env(tmp_path, monkeypatch)
    draft = {
        "processes": [
            {"id": pid, "verdict": "pass" if pid != IDS[0] else "fail", "reason": "looks fine"}
            for pid in IDS
        ],
        "conflicts": [],
    }
    (work / "verdict-droid.json").write_text(json.dumps(draft), encoding="utf-8")
    (work / "packs" / IDS[0] / "checks-exit.json").write_text(
        json.dumps([{"command": "c", "exit": 1}]), encoding="utf-8"
    )

    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in verdict["processes"]}
    assert by_id[IDS[0]]["verdict"] == "fail"
    assert "checks-exit.json" in by_id[IDS[0]]["reason"]


def test_gate_failure_flips_overall_even_when_pytest_zero(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """A red-by-content marker alone turns the round red (overall=fail,
    empty failed list never happens): failed_process_ids carries the gated
    pid."""
    wall_path, work = _env(tmp_path, monkeypatch)
    (work / "packs" / IDS[0] / "checks-failed.marker").write_text("m", encoding="utf-8")

    rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["overall"] == "fail"
    assert merged["validation"]["failed_process_ids"] == [IDS[0]]
    assert merged["validation"]["unattributed_failure"] is False
