"""BLK-1/BLK-3 fix face: the salvage guard and the adopt machine gate judge
a checks-failed.marker by its CONTENT (the design ruling: the marker is the
worker-side verify record; prep's own checks-exit.json is the green
authority), and a worker status skeleton is never the worker's final word.

- A marker whose problems are only the missing evidence files (green
  checks) must not refuse salvage and must not fail adoption — this is the
  r58 death shape the mission exists to cure.
- A marker with a non-zero check exit or a malformed-status problem stays
  red at BOTH consumers (one shared classifier, no drift).
- A status.json skeleton (state in_progress / empty checks / checks not
  matching the card) is machine-rendered and the salvage discloses the
  replacement; a worker-written COMPLETED status is never touched.
- v2.6.3 job-level semantics unchanged: the verify step's trailing
  fail-the-job step still keys on the marker file's existence (not its
  content) — red checks and missing files alike still fail the job.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from adopt_verdict import machine_gate_reds  # noqa: E402
from foreman_run_lib import init_wall, save_wall  # noqa: E402
from merge_worker_deltas import apply_deltas  # noqa: E402
from worker_salvage import (  # noqa: E402
    SALVAGE_MARKER_KEY,
    STATUS_NAME,
    evaluate_salvage_guard,
    salvage_packs,
)

FIXTURE = ROOT / "tests" / "fixtures" / "worker-r58d"
CONTROL = FIXTURE / "control-ok-missing"
PID = "hslconv"
WALL_KILLED_DELTA = json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text())
OK_DELTA = json.loads((CONTROL / "worker-delta.json").read_text())

GREEN_MISSING_MARKER = (
    f"process: {PID}\n"
    "check exit 0: python3 -m pytest tests/test_hslconv.py -q\n"
    "check exit 0: python3 -m pytest tests/ -q\n"
    f"problem: missing expected file: team/handoffs/{PID}.md\n"
    f"problem: missing expected file: team/status/{PID}.json\n"
)
RED_CHECK_MARKER = (
    f"process: {PID}\n"
    "check exit 0: python3 -m pytest tests/test_hslconv.py -q\n"
    "check exit 1: python3 -m pytest tests/ -q\n"
    "problem: check failed (exit 1): python3 -m pytest tests/ -q\n"
)


def stage_replay_dir(tmp_path: Path, fixture: Path = FIXTURE) -> Path:
    ev = tmp_path / "evidence"
    ev.mkdir(parents=True)
    shutil.copytree(fixture / "evidence", ev, dirs_exist_ok=True)
    shutil.copy(fixture / "manifest.json", ev / "manifest.json")
    if not (ev / "plan.json").is_file():
        shutil.copy(FIXTURE / "evidence" / "plan.json", ev / "plan.json")
    return tmp_path


def write_wall(tmp_path: Path, deltas: list[dict]) -> Path:
    wall = apply_deltas(init_wall(run_id="mk", issue_number=929), deltas)
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


def salvaged_wall(tmp_path: Path) -> Path:
    return write_wall(tmp_path, [WALL_KILLED_DELTA])


def add_marker(ws: Path, text: str, *, flag: bool = False) -> None:
    pack = ws / "evidence" / "packs" / PID
    (pack / "checks-failed.marker").write_text(text, encoding="utf-8")
    if flag:
        manifest_path = ws / "evidence" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["packs"][PID]["checks_failed_marker"] = True
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )


def apply_salvage(ws: Path, wall: dict) -> list[dict]:
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = json.loads((ws / "evidence" / "plan.json").read_text(encoding="utf-8"))
    cards = {p["id"]: p for p in plan["processes"]}
    reports = salvage_packs(
        evidence_dir=ws / "evidence",
        cards=cards,
        packs=manifest["packs"],
        wall=wall,
        manifest=manifest,
    )
    if any(r["salvaged"] for r in reports):
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return reports


# --- BLK-1: the guard reads the marker's content ------------------------------


def test_green_missing_files_marker_does_not_refuse_salvage(tmp_path):
    """The r58 anchor shape WITH the marker its own verify step writes: the
    guard must allow the salvage (the marker's problems are only the
    missing files; prep's checks-exit.json all-0 is the green authority)."""
    ws = stage_replay_dir(tmp_path)
    add_marker(ws, GREEN_MISSING_MARKER, flag=True)
    wall = json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8"))
    pack_dir = ws / "evidence" / "packs" / PID
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text(encoding="utf-8"))
    card = {p["id"]: p for p in json.loads((ws / "evidence" / "plan.json").read_text(encoding="utf-8"))["processes"]}[PID]
    allowed, reasons = evaluate_salvage_guard(
        info=manifest["packs"][PID],
        pack_dir=pack_dir,
        card=card,
        workers=wall.get("workers") or {},
        pid=PID,
    )
    assert allowed is True, reasons
    assert any("checks-failed.marker" in r for r in reasons), (
        "the decision trail must still record that the marker was present and "
        "judged by content"
    )
    reports = apply_salvage(ws, wall)
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True
    assert (pack_dir / STATUS_NAME).is_file()
    assert (pack_dir / "handoff.md").is_file()
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["packs"][PID][SALVAGE_MARKER_KEY] is True
    assert manifest["packs"][PID]["complete"] is True


def test_manifest_flag_true_with_green_missing_marker_still_salvages(tmp_path):
    """The flag and the file carry the same content verdict: even with the
    manifest flag set, a missing-file-only marker does not refuse."""
    ws = stage_replay_dir(tmp_path)
    add_marker(ws, GREEN_MISSING_MARKER, flag=True)
    wall = json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8"))
    reports = apply_salvage(ws, wall)
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True


def test_red_check_marker_still_refuses_salvage(tmp_path):
    ws = stage_replay_dir(tmp_path)
    add_marker(ws, RED_CHECK_MARKER, flag=True)
    wall = json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8"))
    pack_dir = ws / "evidence" / "packs" / PID
    before = {p.name: p.read_bytes() for p in sorted(pack_dir.iterdir())}
    reports = apply_salvage(ws, wall)
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is False
    assert any("checks-failed.marker" in r for r in entry["reasons"])
    after = {p.name: p.read_bytes() for p in sorted(pack_dir.iterdir())}
    assert after == before, "a refusal must leave the pack byte-identical"


def test_unrecognized_marker_content_refuses_salvage(tmp_path):
    """Marker bytes that cannot prove their entries green read red (the
    fail-closed default for tampered/foreign content)."""
    ws = stage_replay_dir(tmp_path)
    add_marker(ws, "checks red\n")
    wall = json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8"))
    reports = apply_salvage(ws, wall)
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is False


def test_guard_refusal_text_describes_content_not_a_green_verdict(tmp_path):
    """The refusal text must never tell a worker whose checks passed that
    its verify verdict went red: red-check markers name the exit, missing-
    file-only markers are not a refusal at all, and the present-but-green
    note stays factual."""
    ws = stage_replay_dir(tmp_path)
    add_marker(ws, RED_CHECK_MARKER)
    wall = json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8"))
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text(encoding="utf-8"))
    card = {p["id"]: p for p in json.loads((ws / "evidence" / "plan.json").read_text(encoding="utf-8"))["processes"]}[PID]
    allowed, reasons = evaluate_salvage_guard(
        info=manifest["packs"][PID],
        pack_dir=ws / "evidence" / "packs" / PID,
        card=card,
        workers=wall.get("workers") or {},
        pid=PID,
    )
    joined = "\n".join(reasons)
    assert allowed is False
    assert "went red" not in joined
    assert "exit 1" in joined
    assert "red by content" in joined
    assert "checks-failed.marker" in joined


# --- BLK-3: status skeletons are machine-rendered ------------------------------


def _skeleton_status() -> dict:
    return {
        "id": PID,
        "title": "RGB ↔ HSL 颜色换算组件与测试",
        "state": "in_progress",
        "files": ["hslconv.py", "tests/test_hslconv.py"],
        "checks": [],
    }


def test_skeleton_status_is_replaced_when_only_handoff_missing(tmp_path):
    """Shape A (handoff only missing): a worker-written skeleton in the pack
    is NOT the worker's final word — the machine renders the status from
    prep's facts. The worker's own handoff bytes are never touched (evidence
    immutability), so the disclosure rides the decision trail (reasons)
    there; the machine-written handoff carries it in shape B below."""
    ws = stage_replay_dir(tmp_path)
    pack = ws / "evidence" / "packs" / PID
    worker_handoff = "# Handoff: hslconv\n\nWorker-written handoff bytes.\n"
    (pack / "handoff.md").write_text(worker_handoff, encoding="utf-8")
    (pack / STATUS_NAME).write_text(json.dumps(_skeleton_status(), ensure_ascii=False), encoding="utf-8")
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["packs"][PID]["pack"]["handoff"] = True
    manifest["packs"][PID]["pack"]["status"] = True
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    reports = apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8")))
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True
    status = json.loads((pack / STATUS_NAME).read_text(encoding="utf-8"))
    assert status["state"] == "done"
    assert len(status["checks"]) == 2
    assert all(c["result"].endswith("[exit 0]") for c in status["checks"])
    assert (pack / "handoff.md").read_text(encoding="utf-8") == worker_handoff, (
        "the worker's own handoff bytes are never touched"
    )
    assert any("骨架" in r or "skeleton" in r for r in entry["reasons"]), (
        "shape A (worker handoff kept): the replacement must be disclosed on "
        "the decision trail"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["packs"][PID]["complete"] is True


def test_skeleton_status_is_replaced_when_both_files_missing(tmp_path):
    """Shape B (both missing): the machine-written handoff carries the
    disclosure that the status was machine-rendered over an unfinished
    skeleton."""
    ws = stage_replay_dir(tmp_path)
    pack = ws / "evidence" / "packs" / PID
    (pack / STATUS_NAME).write_text(json.dumps(_skeleton_status(), ensure_ascii=False), encoding="utf-8")
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["packs"][PID]["pack"]["status"] = True
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    reports = apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8")))
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True
    status = json.loads((pack / STATUS_NAME).read_text(encoding="utf-8"))
    assert status["state"] == "done" and len(status["checks"]) == 2
    handoff = (pack / "handoff.md").read_text(encoding="utf-8")
    assert "补卷器生成" in handoff and "status 由机器渲染" in handoff
    assert "未完成骨架" in handoff
    assert any("骨架" in r or "skeleton" in r for r in entry["reasons"])


def test_completed_worker_status_is_never_touched(tmp_path):
    """A status the worker actually finished (state=done, checks present and
    matching the card) is the worker's final word — salvage writes only the
    missing handoff and leaves the worker's bytes exact."""
    ws = stage_replay_dir(tmp_path)
    pack = ws / "evidence" / "packs" / PID
    completed = {
        "id": PID,
        "title": "RGB ↔ HSL 颜色换算组件与测试",
        "state": "done",
        "files": ["hslconv.py", "tests/test_hslconv.py"],
        "checks": [
            {"command": "python3 -m pytest tests/test_hslconv.py -q",
             "result": "21 passed in 0.05s"},
            {"command": "python3 -m pytest tests/ -q",
             "result": "384 passed, 2 skipped in 1.02s"},
        ],
    }
    worker_bytes = json.dumps(completed, ensure_ascii=False, indent=2) + "\n"
    (pack / STATUS_NAME).write_text(worker_bytes, encoding="utf-8")
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["packs"][PID]["pack"]["status"] = True
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    reports = apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8")))
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True
    assert (pack / STATUS_NAME).read_text(encoding="utf-8") == worker_bytes, (
        "a completed worker status is the worker's own final word"
    )
    assert (pack / "handoff.md").is_file()
    handoff = (pack / "handoff.md").read_text(encoding="utf-8")
    assert "status 由机器渲染" not in handoff


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda s: {**s, "checks": []}, id="empty-checks"),
        pytest.param(
            lambda s: {
                **s,
                "state": "done",
                "checks": [{"command": "python3 -m pytest tests/test_hslconv.py -q",
                            "result": "21 passed in 0.05s"}],
            },
            id="checks-do-not-match-card",
        ),
        pytest.param(lambda s: {**s, "state": "done"}, id="done-but-no-checks"),
    ],
)
def test_non_final_status_shapes_are_machine_rendered(tmp_path, mutate):
    """Any non-final shape (empty checks / done without checks / checks not
    matching the card's commands) is a skeleton, never the worker's final
    word. These shapes run with the machine handoff written too (shape B):
    the handoff carries the disclosure."""
    ws = stage_replay_dir(tmp_path)
    pack = ws / "evidence" / "packs" / PID
    (pack / STATUS_NAME).write_text(json.dumps(mutate(_skeleton_status()), ensure_ascii=False), encoding="utf-8")
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["packs"][PID]["pack"]["status"] = True
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    reports = apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8")))
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True
    status = json.loads((pack / STATUS_NAME).read_text(encoding="utf-8"))
    assert status["state"] == "done" and len(status["checks"]) == 2
    handoff = (pack / "handoff.md").read_text(encoding="utf-8")
    assert "status 由机器渲染" in handoff


def test_corrupt_status_json_is_machine_rendered(tmp_path):
    """A status file that does not even parse is a skeleton by definition."""
    ws = stage_replay_dir(tmp_path)
    pack = ws / "evidence" / "packs" / PID
    (pack / STATUS_NAME).write_text("{oops", encoding="utf-8")
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["packs"][PID]["pack"]["status"] = True
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    reports = apply_salvage(ws, json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8")))
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True
    status = json.loads((pack / STATUS_NAME).read_text(encoding="utf-8"))
    assert status["state"] == "done"


# --- BLK-1: the adopt machine gate reads the marker's content -----------------


def _adopt_env(tmp_path: Path, *, marker_text: str | None, checks_exit: str):
    """Minimal complete evidence environment, mirrors test_machine_gates_s2."""
    from adopt_verdict import adopt

    work = tmp_path / "work"
    work.mkdir()
    ids = ["dijkstra", "nthprime", "windscale"]
    manifest = {"pytest_exit": 0, "iteration": 1}
    (work / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work / "plan.json").write_text(
        json.dumps({"processes": [{"id": pid} for pid in ids]}), encoding="utf-8"
    )
    (work / "judgeable.json").write_text(json.dumps(ids), encoding="utf-8")
    (work / "blocked.json").write_text("{}", encoding="utf-8")
    (work / "pytest-output.txt").write_text("192 passed in 15.61s\n", encoding="utf-8")
    draft = {
        "processes": [
            {"id": pid, "verdict": "pass", "reason": "five artifacts line up"}
            for pid in ids
        ],
        "conflicts": [],
    }
    (work / "verdict-droid.json").write_text(json.dumps(draft), encoding="utf-8")
    (work / "verdict-droid.md").write_text("# report\n", encoding="utf-8")
    for pid in ids:
        (work / "packs" / pid).mkdir(parents=True)
        (work / "packs" / pid / "checks-exit.json").write_text("[]", encoding="utf-8")
    (work / "packs" / "windscale" / "checks-exit.json").write_text(checks_exit, encoding="utf-8")
    if marker_text is not None:
        (work / "packs" / "windscale" / "checks-failed.marker").write_text(
            marker_text, encoding="utf-8"
        )
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="mkadopt", issue_number=812), wall_path)
    return work, wall_path, ids


def test_adopt_gate_green_missing_files_marker_keeps_pass(tmp_path):
    """The adopt-side machine gate judges content: a missing-file-only
    marker with all-0 checks-exit.json must NOT fail the process (BLK-1's
    second consumer)."""
    work, wall_path, ids = _adopt_env(
        tmp_path,
        marker_text=GREEN_MISSING_MARKER,
        checks_exit=json.dumps([{"command": "a", "exit": 0}, {"command": "b", "exit": 0}]),
    )
    from adopt_verdict import adopt
    import os

    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    finally:
        os.chdir(old)
    assert rc == 0
    verdict = json.loads((tmp_path / "verdict.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in verdict["processes"]}
    assert by_id["windscale"]["verdict"] == "pass"
    reds = machine_gate_reds(work, ids)
    assert reds == {}


def test_adopt_gate_red_check_marker_fails(tmp_path):
    """A marker with a non-zero check line stays red at the adopt gate —
    same verdict as the salvage guard, one shared classifier. The pack's
    checks-exit.json here reads green (all 0): the marker alone is the red
    fact gating the process, mirroring the salvage guard's content verdict."""
    work, wall_path, ids = _adopt_env(
        tmp_path,
        marker_text=RED_CHECK_MARKER,
        checks_exit=json.dumps([{"command": "a", "exit": 0}, {"command": "b", "exit": 0}]),
    )
    reds = machine_gate_reds(work, ids)
    assert reds.get("windscale")
    assert "checks-failed.marker" in reds["windscale"]

    import os
    from adopt_verdict import adopt

    old = Path.cwd()
    os.chdir(tmp_path)
    try:
        rc = adopt(work, wall_path, droid_exit=0, merge_step_ran=True)
    finally:
        os.chdir(old)
    assert rc == 0
    verdict = json.loads((tmp_path / "verdict.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in verdict["processes"]}
    assert by_id["windscale"]["verdict"] == "fail"
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["overall"] == "fail"
    assert merged["validation"]["failed_process_ids"] == ["windscale"]


def test_adopt_gate_unrecognized_marker_fails_fail_closed(tmp_path):
    work, _wall_path, ids = _adopt_env(
        tmp_path, marker_text="checks failed\n", checks_exit="[]"
    )
    reds = machine_gate_reds(work, ids)
    assert reds.get("windscale")


# --- v2.6.3 job-level accounting unchanged (regression pins) -------------------


def test_trailing_job_fail_step_keys_on_marker_existence_not_content():
    """v2.6.3: the trailing step fails the job whenever the marker file
    exists — red checks AND missing files alike still fail the job (the
    content ruling changes the salvage/adopt consumers, never the job
    conclusion)."""
    text = (ROOT / ".github" / "workflows" / "team.yml").read_text(encoding="utf-8")
    for job in ("worker", "worker2"):
        from lint_workflow_wall_exits import job_spans

        spans = job_spans(text)
        job_text = text[spans[job][0]:spans[job][1]]
        i = job_text.index("Fail the job when process checks failed")
        seg = job_text[i:i + 1200]
        assert 'if [ -f "$MARKER" ]; then' in seg
        assert "exit 1" in seg


def test_marker_is_still_an_evidence_item_of_the_pack(tmp_path):
    """prep's marker copy semantics unchanged: the marker lands in the pack
    as evidence (a flag the salvage reports on), whether or not it reads
    red. Pinned via the guard reasons on the salvaged path."""
    ws = stage_replay_dir(tmp_path)
    add_marker(ws, GREEN_MISSING_MARKER, flag=True)
    wall = json.loads(salvaged_wall(tmp_path).read_text(encoding="utf-8"))
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text(encoding="utf-8"))
    card = {p["id"]: p for p in json.loads((ws / "evidence" / "plan.json").read_text(encoding="utf-8"))["processes"]}[PID]
    allowed, reasons = evaluate_salvage_guard(
        info=manifest["packs"][PID],
        pack_dir=ws / "evidence" / "packs" / PID,
        card=card,
        workers=wall.get("workers") or {},
        pid=PID,
    )
    joined = "\n".join(reasons)
    assert allowed is True
    assert "marker" in joined
    assert "green by content" in joined
