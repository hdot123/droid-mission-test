"""M2 prep salvage packer (worker_salvage) — VAL-M2-002..006.

Round-58 D-run ground truth (tests/fixtures/worker-r58d/): the hslconv
worker session was killed by the 900s wall (droid exit 124) before it wrote
its two evidence files, yet prep's machine re-run of both checks on the
merged branch was green — machine-verified work orphaned by a session death.

Contract (all machine-judged, fail-closed):
- salvage guard = branch merged + no out-of-bounds files + checks-exit all
  zero + no checks-failed.marker in the pack + session abnormally
  terminated. Termination evidence is the wall's own outcome fields: wall
  outcome wall_killed, or a non-zero droid exit code (the exit-1 self-crash
  family the outcome classifier keeps "ok" is still an abnormal END for the
  guard). There is no stream lever on the salvage face (scrutiny NC-4: the
  old completion-absence clause was dead in production and fail-open when
  exercised). A session that exited 0 is a normal end: its missing files
  are a compliance failure and stay blocked (the control fixture pins that).
- handoff.md renders the death cause from the wall's own outcome fields
  (scrutiny BLK-1): a wall recording ok + a non-zero exit states the exit
  code and that the death family is not machine-determined, never 900s /
  wall_killed text; a job_wall_cancelled wall states the job-wall
  cancellation; the never-written sentence is derived from the files
  actually missing (a partial pack is never described as a total loss).
- salvage writes only the missing evidence files, renders them from machine
  facts, declares its machine origin in handoff.md, marks the manifest pack
  salvaged_from_machine=true, and the pack then passes the validator
  precheck's judgeable/blocked scan.
- prep2 salvage reads the ROUND-2 workers snapshot restricted to pids whose
  round-2 delta actually arrived (scrutiny NC-5): a stale round-1
  wall_killed never authorizes a round-2 salvage.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from foreman_run_lib import init_wall, save_wall  # noqa: E402
from lint_workflow_wall_exits import job_spans  # noqa: E402
from merge_worker_deltas import apply_deltas, round2_salvage_wall  # noqa: E402
from worker_salvage import (  # noqa: E402
    HANDOFF_NAME,
    SALVAGE_MARKER_KEY,
    STATUS_NAME,
    abnormal_termination_evidence,
    build_handoff,
    build_status,
    checks_all_green,
    evaluate_salvage_guard,
    salvage_packs,
)

TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"
FIXTURE = ROOT / "tests" / "fixtures" / "worker-r58d"
CONTROL = FIXTURE / "control-ok-missing"
PID = "hslconv"

WALL_KILLED_DELTA = json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text())
OK_DELTA = json.loads((CONTROL / "worker-delta.json").read_text())


# --- replay staging ----------------------------------------------------------


def stage_replay_dir(tmp_path: Path, fixture: Path = FIXTURE) -> Path:
    """A prep-shaped workspace: evidence/ (manifest inside it) + wall slot.

    The control fixture vendors no plan.json (its manifest scope is the
    delta/stream/packs contrast only), so the card always comes from the
    verbatim fixture's plan — the control models the same card by
    construction (see control README)."""
    ev = tmp_path / "evidence"
    ev.mkdir(parents=True)
    shutil.copytree(fixture / "evidence", ev, dirs_exist_ok=True)
    shutil.copy(fixture / "manifest.json", ev / "manifest.json")
    if not (ev / "plan.json").is_file():
        shutil.copy(FIXTURE / "evidence" / "plan.json", ev / "plan.json")
    return tmp_path


def write_wall(tmp_path: Path, deltas: list[dict]) -> Path:
    wall = apply_deltas(init_wall(run_id="45812793849", issue_number=929), deltas)
    if "workers" not in wall:
        wall["workers"] = {
            "schema_version": "worker-matrix.v1",
            "any_cancelled": False,
            "any_failed": False,
            "completed_pids": [],
            "cancelled_pids": [],
            "cancel_reason_by_pid": {},
        }
    path = tmp_path / "foreman-run.json"
    save_wall(wall, path)
    return path


def guard_for(ws: Path, *, wall: dict):
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text())
    plan = json.loads((ws / "evidence" / "plan.json").read_text())
    card = {p["id"]: p for p in plan["processes"]}[PID]
    info = manifest["packs"][PID]
    return evaluate_salvage_guard(
        info=info,
        pack_dir=ws / "evidence" / "packs" / PID,
        card=card,
        workers=(wall.get("workers") or {}),
        pid=PID,
    )


def apply_salvage(ws: Path, wall: dict) -> list[dict]:
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    plan = json.loads((ws / "evidence" / "plan.json").read_text())
    cards = {p["id"]: p for p in plan["processes"]}
    reports = salvage_packs(
        evidence_dir=ws / "evidence",
        cards=cards,
        packs=manifest["packs"],
        wall=wall,
        manifest=manifest,
    )
    # the workflow persists the refreshed packs only when something was
    # salvaged — mirror that so a refusal leaves the manifest byte-identical
    if any(r["salvaged"] for r in reports):
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return reports


def salvaged_wall(tmp_path: Path) -> Path:
    return write_wall(tmp_path, [WALL_KILLED_DELTA])


# --- VAL-M2-002: guard, one positive + four independent negatives ------------


def test_guard_all_four_true_allows_salvage(tmp_path):
    ws = stage_replay_dir(tmp_path)
    wall = json.loads(salvaged_wall(tmp_path).read_text())
    allowed, reasons = guard_for(ws, wall=wall)
    assert allowed is True
    joined = "\n".join(reasons)
    assert "wall_killed" in joined
    assert "124" in joined


def test_guard_rejects_normal_completion_missing(tmp_path):
    ws = stage_replay_dir(tmp_path, CONTROL)
    wall = json.loads(write_wall(tmp_path, [OK_DELTA]).read_text())
    allowed, reasons = guard_for(ws, wall=wall)
    assert allowed is False
    joined = "\n".join(reasons)
    assert "session_outcome=ok" in joined
    assert "wall_killed" not in joined


def test_guard_rejects_red_checks(tmp_path):
    ws = stage_replay_dir(tmp_path)
    exit_path = ws / "evidence" / "packs" / PID / "checks-exit.json"
    exits = json.loads(exit_path.read_text())
    exits[1]["exit"] = 1
    exit_path.write_text(json.dumps(exits, indent=2) + "\n")
    wall = json.loads(salvaged_wall(tmp_path).read_text())
    allowed, reasons = guard_for(ws, wall=wall)
    assert allowed is False
    assert any("checks" in r and "exit 1" in r for r in reasons)


def test_guard_rejects_out_of_bounds(tmp_path):
    ws = stage_replay_dir(tmp_path)
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["packs"][PID]["out_of_bounds"] = ["extra.py"]
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    wall = json.loads(salvaged_wall(tmp_path).read_text())
    allowed, reasons = guard_for(ws, wall=wall)
    assert allowed is False
    assert any("out_of_bounds" in r and "extra.py" in r for r in reasons)


def test_guard_rejects_unmerged_branch(tmp_path):
    ws = stage_replay_dir(tmp_path)
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["packs"][PID]["merged"] = False
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    wall = json.loads(salvaged_wall(tmp_path).read_text())
    allowed, reasons = guard_for(ws, wall=wall)
    assert allowed is False
    assert any("merged" in r for r in reasons)


def test_guard_rejects_branch_not_present(tmp_path):
    ws = stage_replay_dir(tmp_path)
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["packs"][PID]["branch_present"] = False
    manifest["packs"][PID]["merged"] = False
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    wall = json.loads(salvaged_wall(tmp_path).read_text())
    allowed, _ = guard_for(ws, wall=wall)
    assert allowed is False


# --- scrutiny round-1 guidance: termination evidence equivalences ------------


def test_termination_evidence_wall_killed_outcome():
    wall = apply_deltas(init_wall(run_id="u", issue_number=1), [WALL_KILLED_DELTA])
    abnormal, evidence = abnormal_termination_evidence(wall.get("workers") or {}, PID)
    assert abnormal is True
    assert any("session_outcome=wall_killed" in e for e in evidence)


@pytest.mark.parametrize("exit_code", [137, 1, 246])
def test_termination_evidence_nonzero_exit_is_abnormal_even_when_classifier_says_ok(exit_code):
    delta = {"pid": PID, "result": "failure", "session_outcome": "ok",
             "droid_exit_code": exit_code, "stream_tail_marker": False}
    wall = apply_deltas(init_wall(run_id="u", issue_number=1), [delta])
    abnormal, evidence = abnormal_termination_evidence(wall.get("workers") or {}, PID)
    assert abnormal is True
    assert any(str(exit_code) in e for e in evidence)


def test_termination_zero_exit_ok_outcome_is_normal_end():
    wall = apply_deltas(init_wall(run_id="u", issue_number=1), [OK_DELTA])
    abnormal, _ = abnormal_termination_evidence(wall.get("workers") or {}, PID)
    assert abnormal is False


def test_termination_zero_exit_ok_outcome_interrupted_tail_is_abnormal():
    delta = {"pid": PID, "result": "failure", "session_outcome": "ok",
             "droid_exit_code": 0, "stream_tail_marker": True}
    wall = apply_deltas(init_wall(run_id="u", issue_number=1), [delta])
    abnormal, evidence = abnormal_termination_evidence(wall.get("workers") or {}, PID)
    assert abnormal is True
    assert any("stream_tail_marker" in e for e in evidence)


def test_legacy_wall_without_outcome_maps_stays_closed(tmp_path):
    wall = init_wall(run_id="legacy", issue_number=1)
    ws = stage_replay_dir(tmp_path)
    allowed, reasons = guard_for(ws, wall=wall)
    assert allowed is False
    assert any("session" in r.lower() for r in reasons)


# --- scrutiny NC-4: the guard has no stream lever -----------------------------


def test_exit_zero_ok_outcome_never_salvaged_regardless_of_stream(tmp_path):
    """The removed stream clause must stay removed: an exit-0 + ok wall is a
    normal end no matter what stream text a caller claims, and salvage_packs
    no longer accepts streams at all (NC-4: the clause was dead in production
    and fail-open when exercised)."""
    ws = stage_replay_dir(tmp_path)
    wall = json.loads(write_wall(tmp_path, [OK_DELTA]).read_text())
    assert guard_for(ws, wall=wall)[0] is False
    import inspect

    salvage_sig = inspect.signature(salvage_packs)
    assert "streams" not in salvage_sig.parameters
    guard_sig = inspect.signature(evaluate_salvage_guard)
    assert "stream_text" not in guard_sig.parameters
    reports = apply_salvage(ws, wall)
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is False
    assert not (ws / "evidence" / "packs" / PID / "status.json").exists()
    assert not (ws / "evidence" / "packs" / PID / "handoff.md").exists()


# --- scrutiny NC-3: checks-failed.marker is a fail-closed refusal -------------


def test_guard_rejects_checks_failed_marker(tmp_path):
    ws = stage_replay_dir(tmp_path)
    pack = ws / "evidence" / "packs" / PID
    (pack / "checks-failed.marker").write_text("1 of 2 checks exited 1\n", encoding="utf-8")
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["packs"][PID]["checks_failed_marker"] = True
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    wall = json.loads(salvaged_wall(tmp_path).read_text())
    allowed, reasons = guard_for(ws, wall=wall)
    assert allowed is False
    assert any("checks-failed.marker" in r for r in reasons)


def test_wall_killed_with_marker_file_is_not_salvaged_bytes_unchanged(tmp_path):
    """M3 will give the verify step if: always(), making this path reachable:
    a wall-killed worker whose own checks failed must never be salvaged into
    state=done — the pack keeps prep's bytes exactly (fail-closed)."""
    ws = stage_replay_dir(tmp_path)
    pack = ws / "evidence" / "packs" / PID
    (pack / "checks-failed.marker").write_text("checks red\n", encoding="utf-8")
    before = {p.name: p.read_bytes() for p in sorted(pack.iterdir())}
    manifest_path = ws / "evidence" / "manifest.json"
    manifest_bytes_before = manifest_path.read_bytes()
    reports = apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text()))
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is False
    after = {p.name: p.read_bytes() for p in sorted(pack.iterdir())}
    assert after == before
    assert manifest_path.read_bytes() == manifest_bytes_before
    manifest = json.loads(manifest_path.read_text())
    assert SALVAGE_MARKER_KEY not in manifest["packs"][PID]
    assert not (pack / "status.json").exists()
    assert not (pack / "handoff.md").exists()


def test_marker_absent_guard_still_allows_salvage(tmp_path):
    """The marker clause must not need the manifest flag: a marker FILE in
    the pack is refused on sight even when info carries no flag (and the
    legacy no-marker shape keeps salvaging)."""
    ws = stage_replay_dir(tmp_path)
    pack = ws / "evidence" / "packs" / PID
    (pack / "checks-failed.marker").write_text("checks red\n", encoding="utf-8")
    wall = json.loads(salvaged_wall(tmp_path).read_text())
    allowed, reasons = guard_for(ws, wall=wall)
    assert allowed is False
    assert any("checks-failed.marker" in r for r in reasons)

    ws2 = stage_replay_dir(tmp_path / "clean")
    wall2 = json.loads(write_wall(tmp_path / "clean", [WALL_KILLED_DELTA]).read_text())
    reports = apply_salvage(ws2, wall2)
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True


# --- checks-all-green predicate ----------------------------------------------


def test_checks_all_green_predicate(tmp_path):
    pack = tmp_path / "pack"
    pack.mkdir()
    assert checks_all_green(None, pack) is False
    (pack / "checks-exit.json").write_text("[]")
    assert checks_all_green(json.loads((pack / "checks-exit.json").read_text()), pack) is False
    (pack / "checks-exit.json").write_text(json.dumps([{"command": "x", "exit": 0}]))
    assert checks_all_green(json.loads((pack / "checks-exit.json").read_text()), pack) is True
    (pack / "checks-exit.json").write_text(json.dumps([{"command": "x", "exit": 0},
                                                       {"command": "y", "exit": 2}]))
    assert checks_all_green(json.loads((pack / "checks-exit.json").read_text()), pack) is False
    (pack / "checks-exit.json").write_text("{not json")
    assert checks_all_green(None, pack) is False


# --- VAL-M2-003: salvaged status.json protocol fidelity -----------------------


def test_salvaged_status_json_fields_match_protocol(tmp_path):
    ws = stage_replay_dir(tmp_path)
    apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text()))
    status = json.loads((ws / "evidence" / "packs" / PID / "status.json").read_text())
    assert sorted(status.keys()) == ["checks", "files", "id", "state", "title"]
    card = json.loads((ws / "evidence" / "plan.json").read_text())["processes"][0]
    assert card["id"] == PID
    assert status["id"] == PID
    assert status["title"] == card["title"]
    assert status["state"] == "done"
    assert status["files"] == card["files"]
    exit_doc = json.loads((ws / "evidence" / "packs" / PID / "checks-exit.json").read_text())
    assert [c["command"] for c in status["checks"]] == [e["command"] for e in exit_doc]
    for entry, expected in zip(status["checks"], exit_doc):
        m = re.search(r"\[exit (-?\d+)\]", entry["result"])
        assert m and int(m.group(1)) == expected["exit"] == 0
    assert "21 passed" in status["checks"][0]["result"]
    assert "384 passed, 2 skipped" in status["checks"][1]["result"]


def test_build_status_is_pure_machine_rendering():
    card = {"id": "p", "title": "T", "files": ["p.py"],
            "checks": ["python3 -m pytest tests/test_p.py -q"]}
    checks_exit = [{"command": "python3 -m pytest tests/test_p.py -q", "exit": 0}]
    checks_output = "$ python3 -m pytest tests/test_p.py -q\n3 passed in 0.01s\n\n[exit 0]\n"
    status = build_status(card=card, checks_exit=checks_exit, checks_output=checks_output)
    assert status == {
        "id": "p", "title": "T", "state": "done", "files": ["p.py"],
        "checks": [{"command": "python3 -m pytest tests/test_p.py -q",
                    "result": "3 passed in 0.01s [exit 0]"}],
    }


# --- VAL-M2-004: handoff.md declares machine origin ---------------------------


def test_salvaged_handoff_declares_machine_origin(tmp_path):
    ws = stage_replay_dir(tmp_path)
    apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text()))
    text = (ws / "evidence" / "packs" / PID / "handoff.md").read_text(encoding="utf-8")
    assert "补卷器" in text and "生成" in text
    assert "非工人亲写" in text
    assert "落盘未遂" in text
    assert "wall_killed" in text and "124" in text
    assert "机器复验" in text and "全绿" in text
    assert "salvaged_from_machine=true" in text
    assert "[exit 0]" in text
    assert f"team/status/{PID}.json" in text and f"team/handoffs/{PID}.md" in text


# --- scrutiny BLK-1: the 死因 section states only what the wall recorded ------


def _death_cause_section(handoff_text: str) -> str:
    """The 死因 section body: from its heading to the last line before the
    next top-level section (pins the narrative, not shared header tokens)."""
    m = re.search(r"^## 死因.*?^## ", handoff_text, re.S | re.M)
    assert m, "handoff must carry a 死因 section"
    return m.group(0)[: -len("## ")]


def test_handoff_exit1_self_crash_states_exit_code_never_wall_killed():
    """BLK-1 production-reachable shape: the wall says ok + exit 1 (droid
    self-crash). The salvaged handoff must state the exit code and that the
    death family is not machine-determined — never 900s / wall_killed text."""
    wall = {
        "workers": {
            "session_outcome_by_pid": {PID: "ok"},
            "droid_exit_code_by_pid": {PID: 1},
            "stream_tail_marker_by_pid": {PID: False},
        }
    }
    text = build_handoff(
        pid=PID,
        card={"id": PID, "title": "T", "files": []},
        checks_exit=[{"command": "pytest -q", "exit": 0}],
        checks_output="$ pytest -q\n1 passed\n",
        branch="team/x",
        workers=wall.get("workers") or {},
        missing_files=(HANDOFF_NAME, STATUS_NAME),
    )
    section = _death_cause_section(text)
    assert "900s" not in section
    assert "wall_killed" not in section
    assert "进程墙" not in section
    assert "droid exit 1" in section
    assert "session_outcome=ok" in section
    assert "死族" in section  # death family not machine-determined
    # header blockquote likewise must not assert a wall kill
    header = text.split("## ")[0]
    assert "900s" not in header
    assert "wall_killed" not in header
    assert "droid exit 1" in header


def test_handoff_job_wall_cancelled_states_job_wall_not_900s_wall():
    """BLK-1 second shape: the wall says job_wall_cancelled. The handoff
    says the job (25m envelope) cancelled the run — no 900s process-wall
    kill claim, and the wall_killed verdict does not appear as session
    outcome anywhere."""
    wall = {
        "workers": {
            "session_outcome_by_pid": {PID: "job_wall_cancelled"},
            "droid_exit_code_by_pid": {PID: 124},
            "stream_tail_marker_by_pid": {PID: True},
        }
    }
    text = build_handoff(
        pid=PID,
        card={"id": PID, "title": "T", "files": []},
        checks_exit=[{"command": "pytest -q", "exit": 0}],
        checks_output="$ pytest -q\n1 passed\n",
        branch="team/x",
        workers=wall.get("workers") or {},
        missing_files=(HANDOFF_NAME, STATUS_NAME),
    )
    section = _death_cause_section(text)
    assert "900s" not in section
    assert "25m" in section and "job" in section.lower()
    assert "session_outcome=job_wall_cancelled" in section
    header = text.split("## ")[0]
    assert "900s" not in header
    assert "wall_killed" not in header
    assert "job_wall_cancelled" in header


def test_handoff_wall_killed_keeps_900s_text():
    """The r58 target shape keeps the 900s wall-kill narrative — the branch
    must not lose the true statement for the shape it was built for."""
    wall = {
        "workers": {
            "session_outcome_by_pid": {PID: "wall_killed"},
            "droid_exit_code_by_pid": {PID: 124},
            "stream_tail_marker_by_pid": {PID: True},
        }
    }
    text = build_handoff(
        pid=PID,
        card={"id": PID, "title": "T", "files": []},
        checks_exit=[{"command": "pytest -q", "exit": 0}],
        checks_output="$ pytest -q\n1 passed\n",
        branch="team/x",
        workers=wall.get("workers") or {},
        missing_files=(HANDOFF_NAME, STATUS_NAME),
    )
    section = _death_cause_section(text)
    assert "900s" in section
    assert "wall_killed" in section
    assert "124" in section


def test_handoff_tail_marker_only_states_interrupted_tool_error():
    """Only a true stream_tail_marker on the wall (no outcome, no exit):
    the handoff reports the interrupted tool_error tail, inventing neither
    a wall kill nor a session outcome."""
    wall = {"workers": {"stream_tail_marker_by_pid": {PID: True}}}
    text = build_handoff(
        pid=PID,
        card={"id": PID, "title": "T", "files": []},
        checks_exit=[{"command": "pytest -q", "exit": 0}],
        checks_output="$ pytest -q\n1 passed\n",
        branch="team/x",
        workers=wall.get("workers") or {},
        missing_files=(HANDOFF_NAME, STATUS_NAME),
    )
    section = _death_cause_section(text)
    assert "900s" not in section
    assert "wall_killed" not in section
    assert "Tool execution was interrupted" in section


def test_handoff_missing_files_sentence_names_only_missing_files():
    """The never-written sentence is derived from the actually missing set:
    a partial pack (handoff written by the worker, status missing) must not
    be described as losing both files."""
    wall = {
        "workers": {
            "session_outcome_by_pid": {PID: "wall_killed"},
            "droid_exit_code_by_pid": {PID: 124},
            "stream_tail_marker_by_pid": {PID: True},
        }
    }
    text = build_handoff(
        pid=PID,
        card={"id": PID, "title": "T", "files": []},
        checks_exit=[{"command": "pytest -q", "exit": 0}],
        checks_output="$ pytest -q\n1 passed\n",
        branch="team/x",
        workers=wall.get("workers") or {},
        missing_files=(STATUS_NAME,),
    )
    assert f"team/handoffs/{PID}.md" not in text  # worker wrote it; never claimed lost
    assert f"team/status/{PID}.json" in text
    header = text.split("## ")[0]
    assert "落盘未遂" in header  # the salvage-origin declaration survives
    # the machine backfill line names exactly the file it wrote — never the
    # worker's own handoff bytes (evidence immutability in prose, too)
    assert "evidence/packs/" in header
    assert f"evidence/packs/{PID}/handoff.md" not in header
    # "两件" must not appear for a one-file salvage
    assert "两件" not in header


def test_salvage_partial_pack_handoff_states_one_file_only(tmp_path):
    """End-to-end partial pack through the real salvage path: the worker's
    handoff survives untouched, the machine-rendered status lands, and the
    reason trail names only status.json."""
    ws = stage_replay_dir(tmp_path)
    pack = ws / "evidence" / "packs" / PID
    worker_handoff = "# Handoff: hslconv\n\nWorker-written bytes.\n"
    (pack / "handoff.md").write_text(worker_handoff, encoding="utf-8")
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["packs"][PID]["pack"]["handoff"] = True
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    reports = apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text()))
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True
    assert any("status.json" in r for r in entry["reasons"])
    assert (pack / "handoff.md").read_text(encoding="utf-8") == worker_handoff
    assert (pack / "status.json").is_file()


@pytest.mark.parametrize(
    ("outcome", "exit_code", "marker"),
    [("ok", 1, False), ("job_wall_cancelled", 124, True), ("wall_killed", 124, True)],
)
def test_salvaged_handoff_death_cause_pinned_end_to_end(tmp_path, outcome, exit_code, marker):
    """Delete-the-section red guard, through the real salvage path: each
    death family's handoff carries a 死因 section whose body states the
    recorded outcome and exit code; the wall_killed body carries the 900s
    text, the other two never do."""
    delta = {"pid": PID, "result": "failure", "session_outcome": outcome,
             "droid_exit_code": exit_code, "stream_tail_marker": marker}
    ws = stage_replay_dir(tmp_path)
    wall = json.loads(write_wall(tmp_path, [delta]).read_text())
    apply_salvage(ws, wall)
    text = (ws / "evidence" / "packs" / PID / "handoff.md").read_text(encoding="utf-8")
    section = _death_cause_section(text)
    assert f"droid exit {exit_code}" in section
    assert f"session_outcome={outcome}" in section
    if outcome == "wall_killed":
        assert "900s" in section
    else:
        assert "900s" not in section
        assert "wall_killed" not in section


# --- VAL-M2-005: manifest salvage marker --------------------------------------


def test_manifest_marks_salvage_only_on_salvaged_pack(tmp_path):
    ws = stage_replay_dir(tmp_path)
    apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text()))
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text())
    assert manifest["packs"][PID][SALVAGE_MARKER_KEY] is True
    for other in ("radixsort", "uuencode"):
        assert SALVAGE_MARKER_KEY not in manifest["packs"][other]


def test_control_manifest_has_no_salvage_marker(tmp_path):
    ws = stage_replay_dir(tmp_path, CONTROL)
    apply_salvage(ws, json.loads(write_wall(tmp_path, [OK_DELTA]).read_text()))
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text())
    assert SALVAGE_MARKER_KEY not in manifest["packs"][PID]
    assert not (ws / "evidence" / "packs" / PID / "status.json").exists()
    assert not (ws / "evidence" / "packs" / PID / "handoff.md").exists()


# --- VAL-M2-006: validator precheck replay (judgeable/blocked scan) -----------

PRECHECK_STEP = "- name: Extract and precheck evidence packs\n"


def _precheck_heredoc_source() -> str:
    yml = TEAM_YML.read_text(encoding="utf-8")
    step = yml.index(PRECHECK_STEP)
    heredoc = yml.index("python3 - <<'PY'\n", step) + len("python3 - <<'PY'\n")
    end = yml.index("\n          PY\n", heredoc)
    return textwrap.dedent(yml[heredoc:end])


def _run_precheck(ws: Path, tmp_path: Path) -> tuple[list, dict]:
    """Stage work/ the way the validate job sees it (extracted tar) and run
    the workflow's own precheck heredoc verbatim against it.

    One replay-surface adaptation, documented per PROVENANCE: the sibling
    packs (radixsort/uuencode) are attested-debt — their sha256 keys stay in
    the manifest but their bytes were deliberately NOT vendored. CI verifies
    every sha entry against real bytes; a replay cannot, so the staging
    drops exactly the sha keys whose files are absent and hashes the reduced
    manifest for the EXPECTED_MANIFEST_SHA gate. The packs dict itself is
    staged untouched; the replay exercises the hslconv salvage chain."""
    import os
    from io import StringIO
    from contextlib import redirect_stdout

    work = tmp_path / "work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text())
    manifest["sha256"] = {
        rel: digest
        for rel, digest in (manifest.get("sha256") or {}).items()
        if (ws / "evidence" / rel[len("evidence/"):]).is_file()
    }
    manifest_bytes = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    (work / "manifest.json").write_bytes(manifest_bytes.encode("utf-8"))
    for rel in manifest["sha256"]:
        src = ws / "evidence" / rel[len("evidence/"):]
        dst = work / rel[len("evidence/"):]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst)
    for member in ("plan.json", "check-summary.json", "pytest-output.txt",
                   "pytest-exit.txt", "candidate-branch.txt"):
        src = ws / "evidence" / member
        if src.is_file() and not (work / member).exists():
            shutil.copy(src, work / member)
    monkey_out = tmp_path / "gh-output"
    old_cwd = Path.cwd()
    old_env = {
        k: os.environ.get(k)
        for k in ("GITHUB_WORKSPACE", "EXPECTED_MANIFEST_SHA", "GITHUB_OUTPUT")
    }
    os.environ["GITHUB_WORKSPACE"] = str(tmp_path)
    os.environ["EXPECTED_MANIFEST_SHA"] = hashlib.sha256(manifest_bytes.encode("utf-8")).hexdigest()
    os.environ["GITHUB_OUTPUT"] = str(monkey_out)
    try:
        os.chdir(tmp_path)
        with redirect_stdout(StringIO()):
            exec(compile(_precheck_heredoc_source(), "<precheck>", "exec"), {"__name__": "pre"})
    finally:
        os.chdir(old_cwd)
        # restore all three: adopt_verdict's in-process adopt() reads
        # EXPECTED_MANIFEST_SHA (empty = no check) — a leaked real hash
        # would turn later adopt() calls into false evidence_tampered
        for k, v in old_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    judgeable = json.loads((work / "judgeable.json").read_text())
    blocked = json.loads((work / "blocked.json").read_text())
    return judgeable, blocked


def test_salvaged_pack_passes_precheck_control_stays_blocked(tmp_path):
    salvaged_ws = stage_replay_dir(tmp_path / "s", FIXTURE)
    apply_salvage(salvaged_ws, json.loads(salvaged_wall(tmp_path / "s").read_text()))
    judgeable, blocked = _run_precheck(salvaged_ws, tmp_path)
    assert PID in judgeable
    assert blocked == {}

    control_ws = stage_replay_dir(tmp_path / "c", CONTROL)
    judgeable_c, blocked_c = _run_precheck(control_ws, tmp_path)
    assert judgeable_c == []
    assert PID in blocked_c
    assert "handoff" in blocked_c[PID] and "status" in blocked_c[PID]


# --- pack digest coverage (PR #836 artifact-first: sha covers salvage) -------


def test_salvage_products_are_covered_by_manifest_digests(tmp_path):
    ws = stage_replay_dir(tmp_path)
    apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text()))
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text())
    for name in ("status.json", "handoff.md"):
        key = f"evidence/packs/{PID}/{name}"
        path = ws / "evidence" / "packs" / PID / name
        assert key in manifest["sha256"], f"{key} missing from manifest sha table"
        assert manifest["sha256"][key] == hashlib.sha256(path.read_bytes()).hexdigest()


# --- CI-fidelity replay: the workflow's own salvage block ---------------------


def _salvage_block_source(job: str) -> str:
    """The prep/prep2 salvage block, verbatim from the workflow heredoc,
    dedented to runnable Python (mirrors _extract_summary_heredoc in
    test_check_summary_focused_counts.py)."""
    yml = TEAM_YML.read_text(encoding="utf-8")
    text = _job_text(yml, job)
    start = text.index("          try:\n              import sys as _salvage_sys")
    end = text.index("packs left as produced", start)
    end = text.index("\n", end) + 1
    raw = text[start:end]
    return "\n".join(ln[10:] if ln.startswith(" " * 10) else ln for ln in raw.splitlines())


WALL_SHAPE = {
    "schema_version": "foreman-run.v1",
    "run_id": "45812793849",
    "issue_number": 929,
    "foreman_mode": "test",
    "env": {},
    "budgets": {},
    "chain": {},
    "artifacts": {},
    "workers": {
        "schema_version": "worker-matrix.v1",
        "any_failed": True,
        "any_cancelled": False,
        "completed_pids": [PID],
        "cancelled_pids": [],
        "cancel_reason_by_pid": {},
        "session_outcome_by_pid": {PID: "wall_killed"},
        "droid_exit_code_by_pid": {PID: 124},
        "stream_tail_marker_by_pid": {PID: True},
    },
}

WALL_SHAPE_ROUND2 = {
    **WALL_SHAPE,
    # what prep2 must judge on: the round-2 snapshot (the workers2-wall-merge
    # step ran apply_deltas --round 2) restricted to the pids whose round-2
    # delta actually arrived
    "round2": {
        "workers": WALL_SHAPE["workers"],
        "delta_pids": [PID],
    },
}

WALL_SHAPE_ROUND2_STALE = {
    **WALL_SHAPE,
    "round2": {
        "workers": WALL_SHAPE["workers"],
        "delta_pids": ["someotherpid"],
    },
}


@pytest.mark.parametrize("job", ["prep", "prep2"])
def test_workflow_salvage_block_replays_and_persists_manifest(tmp_path, job):
    """Run the workflow's own salvage block in a clean subprocess (fresh
    interpreter, PYTHONPATH/GITHUB_WORKSPACE stripped — the CI shape) against
    the r58 fixture, and pin the persistence: on-disk manifest gains the
    marker, complete flips true, and the salvaged bytes hash into the sha
    walk that follows the block."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from tests.replay_heredoc import create_git_archive_copy, run_heredoc_in_clean_subprocess

    ws = tmp_path / f"ws-{job}"
    create_git_archive_copy(ws)
    ev = ws / "evidence"
    ev.mkdir()
    shutil.copytree(FIXTURE / "evidence", ev, dirs_exist_ok=True)
    shutil.copy(FIXTURE / "manifest.json", ev / "manifest.json")
    (ws / "wall-in").mkdir()
    wall_shape = WALL_SHAPE_ROUND2 if job == "prep2" else WALL_SHAPE
    (ws / "wall-in" / "foreman-run.json").write_text(json.dumps(wall_shape))
    script = _salvage_block_source(job)
    if job == "prep2":
        script = "rerun = {p['id']: p for p in plan['processes']}\n" + script
    source = (
        "import json, os\n"
        'plan = json.load(open("evidence/plan.json"))\n'
        'manifest = json.load(open("evidence/manifest.json"))\n'
        'packs = manifest["packs"]\n'
        f"{script}\n"
        f"print('SALVAGE-REPLAY-OK', {job!r})\n"
    )
    r = run_heredoc_in_clean_subprocess(source, cwd=ws)
    assert r.returncode == 0, f"{job} salvage block failed in clean subprocess:\n{r.stderr}"
    assert "SALVAGE-REPLAY-OK" in r.stdout
    # persistence: the on-disk manifest carries the salvage (not just the
    # in-memory dict the block started with)
    manifest = json.loads((ev / "manifest.json").read_text())
    pack = manifest["packs"][PID]
    assert pack.get(SALVAGE_MARKER_KEY) is True, (
        f"{job}: salvage marker never reached evidence/manifest.json on disk"
    )
    assert pack["complete"] is True
    assert pack["pack"]["handoff"] is True and pack["pack"]["status"] is True
    # simulate the workflow's os.walk digest pass over the salvaged tree
    sha = {}
    for root, _dirs, files in os.walk(ev):
        for name in files:
            path = os.path.join(root, name)
            rel = os.path.relpath(path, ws)
            if rel == "evidence/manifest.json":
                continue
            sha[rel] = hashlib.sha256(open(path, "rb").read()).hexdigest()
    for key in (f"evidence/packs/{PID}/status.json", f"evidence/packs/{PID}/handoff.md"):
        assert key in sha, f"{key} absent from the post-salvage digest walk"


def test_workflow_prep2_salvage_refuses_stale_round1_fact(tmp_path):
    """NC-5 end-to-end through the workflow's own prep2 block: a wall whose
    round-2 merge heard from no delta for this pid must leave the pack
    exactly as prep2 produced it (the round-1 wall_killed stays history)."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from tests.replay_heredoc import create_git_archive_copy, run_heredoc_in_clean_subprocess

    ws = tmp_path / "ws-prep2-stale"
    create_git_archive_copy(ws)
    ev = ws / "evidence"
    ev.mkdir()
    shutil.copytree(FIXTURE / "evidence", ev, dirs_exist_ok=True)
    shutil.copy(FIXTURE / "manifest.json", ev / "manifest.json")
    (ws / "wall-in").mkdir()
    (ws / "wall-in" / "foreman-run.json").write_text(json.dumps(WALL_SHAPE_ROUND2_STALE))
    script = _salvage_block_source("prep2")
    script = "rerun = {p['id']: p for p in plan['processes']}\n" + script
    source = (
        "import json, os\n"
        'plan = json.load(open("evidence/plan.json"))\n'
        'manifest = json.load(open("evidence/manifest.json"))\n'
        'packs = manifest["packs"]\n'
        f"{script}\n"
        "print('SALVAGE-REPLAY-DONE')\n"
    )
    r = run_heredoc_in_clean_subprocess(source, cwd=ws)
    assert r.returncode == 0, r.stderr
    assert "SALVAGE-REPLAY-DONE" in r.stdout
    pack = json.loads((ev / "manifest.json").read_text())["packs"][PID]
    assert SALVAGE_MARKER_KEY not in pack
    assert pack["complete"] is False
    assert not (ev / "packs" / PID / "status.json").exists()
    assert not (ev / "packs" / PID / "handoff.md").exists()


def test_salvage_is_idempotent(tmp_path):
    ws = stage_replay_dir(tmp_path)
    wall = json.loads(salvaged_wall(tmp_path).read_text())
    apply_salvage(ws, wall)
    status_before = (ws / "evidence" / "packs" / PID / "status.json").read_bytes()
    handoff_before = (ws / "evidence" / "packs" / PID / "handoff.md").read_bytes()
    manifest_before = (ws / "evidence" / "manifest.json").read_bytes()
    reports = apply_salvage(ws, wall)
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is False
    assert any("already" in r for r in entry["reasons"])
    assert (ws / "evidence" / "packs" / PID / "status.json").read_bytes() == status_before
    assert (ws / "evidence" / "packs" / PID / "handoff.md").read_bytes() == handoff_before
    assert (ws / "evidence" / "manifest.json").read_bytes() == manifest_before


def test_salvage_fills_only_missing_files_and_keeps_worker_handoff(tmp_path):
    ws = stage_replay_dir(tmp_path)
    pack = ws / "evidence" / "packs" / PID
    worker_handoff = "# Handoff: hslconv\n\nWorker-written handoff bytes.\n"
    (pack / "handoff.md").write_text(worker_handoff, encoding="utf-8")
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["packs"][PID]["pack"]["handoff"] = True
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text()))
    assert (pack / "handoff.md").read_text(encoding="utf-8") == worker_handoff
    assert (pack / "status.json").is_file()
    manifest = json.loads(manifest_path.read_text())
    assert manifest["packs"][PID][SALVAGE_MARKER_KEY] is True
    assert manifest["packs"][PID]["complete"] is True


# --- workflow wiring pins (prep + prep2) ---------------------------------------


def _job_text(yml: str, job: str) -> str:
    spans = job_spans(yml)
    start, end = spans[job]
    return yml[start:end]


@pytest.mark.parametrize("job", ["prep", "prep2"])
def test_prep_and_prep2_wire_worker_salvage(job: str):
    text = _job_text(TEAM_YML.read_text(encoding="utf-8"), job)
    assert "from worker_salvage import" in text, f"{job} must invoke the salvage module"
    assert "salvage_packs(" in text
    # CI import fidelity: the heredoc seeds scripts/team itself (r58 scrutiny
    # round-1 blocking class of defect).
    assert 'os.path.join(os.environ.get("GITHUB_WORKSPACE", "."), "scripts", "team")' in text
    assert "except Exception" in text, "salvage failure must be fail-closed, not fatal to prep"
    # PR #836 artifact-first: the in-memory packs dict is not what downstream
    # judges — a salvage that updates the manifest on disk is part of the
    # wiring, in the same step (validator precheck reads evidence/manifest.json).
    assert 'json.dump(_m, open("evidence/manifest.json", "w")' in text, (
        f"{job}: salvage must persist the refreshed packs into evidence/manifest.json"
    )


@pytest.mark.parametrize("job", ["prep", "prep2"])
def test_salvage_sits_after_checks_loop_before_summary_and_manifest_hash(job: str):
    text = _job_text(TEAM_YML.read_text(encoding="utf-8"), job)
    loop_idx = text.find('json.dump(exits, open(f"{pack_dir}/checks-exit.json"')
    salvage_idx = text.find("from worker_salvage import")
    summary_idx = text.find('json.dump({"schema_version": "check-summary.v1"')
    manifest_idx = text.find('manifest["sha256"]')
    assert loop_idx != -1 and salvage_idx != -1 and summary_idx != -1 and manifest_idx != -1
    assert loop_idx < salvage_idx, "salvage must run after the per-card checks loop"
    assert salvage_idx < summary_idx, "salvage must run before the authoritative summary"
    assert summary_idx < manifest_idx, "summary must precede the manifest digest walk"


def test_prep_salvage_reads_wall_from_wall_in():
    text = _job_text(TEAM_YML.read_text(encoding="utf-8"), "prep")
    assert 'wall-in/foreman-run.json' in text, (
        "prep salvage must read the worker-delta outcome facts from the wall artifact"
    )


def test_prep2_salvage_is_scoped_to_rerun_processes():
    text = _job_text(TEAM_YML.read_text(encoding="utf-8"), "prep2")
    m = re.search(r"salvage_cards = \{([^}]*)\}", text)
    assert m, "prep2 salvage must pass an explicit cards mapping"
    assert "rerun" in m.group(1), "prep2 salvage must only consider rerun processes"


# --- scrutiny NC-5: prep2 salvage reads the round-2 snapshot only -------------


def _round2_wall(tmp_path: Path, deltas: list[dict], round1: list[dict]) -> dict:
    """The real round-2 wall shape: round-1 deltas merged into the top-level
    workers slice, round-2 deltas merged with round_tag="2" on top."""
    wall = apply_deltas(init_wall(run_id="r58r2", issue_number=929), round1)
    wall = apply_deltas(wall, deltas, round_tag="2")
    path = tmp_path / "foreman-run.json"
    save_wall(wall, path)
    return json.loads(path.read_text())


def test_round2_salvage_wall_with_round2_delta_uses_round2_facts(tmp_path):
    """worker2 re-crashed to the wall in round 2: the round-2 snapshot
    carries its own wall_killed and the salvage sees exactly that."""
    wall = _round2_wall(
        tmp_path,
        [{"pid": PID, "result": "failure", "session_outcome": "wall_killed",
          "droid_exit_code": 124, "stream_tail_marker": True}],
        [dict(OK_DELTA)],
    )
    workers = round2_salvage_wall(wall)
    outcome = (workers.get("session_outcome_by_pid") or {}).get(PID)
    assert outcome == "wall_killed"
    abnormal, evidence = abnormal_termination_evidence(workers, PID)
    assert abnormal is True
    assert any("124" in e for e in evidence)


def test_round2_salvage_wall_without_round2_delta_refuses_stale_round1_fact(tmp_path):
    """NC-5 loss shape: worker2 died before its delta step, so no round-2
    delta exists for the pid. The round-1 wall_killed must NOT authorize the
    round-2 salvage — the pid falls out of the snapshot entirely."""
    wall = _round2_wall(
        tmp_path,
        [],  # worker2 never delivered a delta
        [json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text())],
    )
    workers = round2_salvage_wall(wall)
    assert PID not in (workers.get("session_outcome_by_pid") or {})
    abnormal, _ = abnormal_termination_evidence(workers, PID)
    assert abnormal is False


def test_round2_salvage_wall_without_snapshot_is_closed(tmp_path):
    """A round-2 salvage against a wall with no round-2 snapshot at all (no
    round-2 merge ran) must never fall back to the round-1 top-level slice."""
    wall = apply_deltas(init_wall(run_id="r58r2", issue_number=929),
                        [json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text())])
    workers = round2_salvage_wall(wall)
    assert not (workers or {}).get("session_outcome_by_pid")
    abnormal, _ = abnormal_termination_evidence(workers, PID)
    assert abnormal is False


def test_round2_stale_fact_does_not_salvage_end_to_end(tmp_path):
    """Full prep2-shape negative: round-1 wall_killed on the wall, worker2
    delta missing, the round-2 pack missing both files — no salvage, the
    pack stays exactly as prep2 produced it."""
    wall = _round2_wall(
        tmp_path,
        [],
        [json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text())],
    )
    ws = stage_replay_dir(tmp_path)
    reports = apply_salvage(ws, {"workers": round2_salvage_wall(wall)})
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is False
    assert SALVAGE_MARKER_KEY not in json.loads((ws / "evidence" / "manifest.json").read_text())["packs"][PID]
    assert not (ws / "evidence" / "packs" / PID / "status.json").exists()
    assert not (ws / "evidence" / "packs" / PID / "handoff.md").exists()


def test_round2_fresh_delta_salvages_end_to_end(tmp_path):
    """The healthy round-2 shape: worker2's own delta records the wall kill,
    and the round-2 pack is salvaged on those round-2 facts."""
    wall = _round2_wall(
        tmp_path,
        [{"pid": PID, "result": "failure", "session_outcome": "wall_killed",
          "droid_exit_code": 124, "stream_tail_marker": True}],
        [dict(OK_DELTA)],
    )
    ws = stage_replay_dir(tmp_path)
    reports = apply_salvage(ws, {"workers": round2_salvage_wall(wall)})
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text())
    assert manifest["packs"][PID][SALVAGE_MARKER_KEY] is True
    assert manifest["packs"][PID]["complete"] is True


def test_prep2_salvage_reads_round2_snapshot():
    """Wiring pin: the prep2 salvage block must derive its workers slice via
    round2_salvage_wall (the NC-5 helper) instead of reading the merged
    top-level maps."""
    text = _job_text(TEAM_YML.read_text(encoding="utf-8"), "prep2")
    assert "round2_salvage_wall" in text
    prep_text = _job_text(TEAM_YML.read_text(encoding="utf-8"), "prep")
    assert "round2_salvage_wall" not in prep_text
