"""M2 prep salvage packer (worker_salvage) — VAL-M2-002..006.

Round-58 D-run ground truth (tests/fixtures/worker-r58d/): the hslconv
worker session was killed by the 900s wall (droid exit 124) before it wrote
its two evidence files, yet prep's machine re-run of both checks on the
merged branch was green — machine-verified work orphaned by a session death.

Contract (all machine-judged, fail-closed):
- salvage guard = branch merged + no out-of-bounds files + checks-exit all
  zero + session abnormally terminated. Termination evidence is any of:
  wall outcome wall_killed, a non-zero droid exit code (the exit-1 self-crash
  family the outcome classifier keeps "ok" is still an abnormal END for the
  guard), or a supplied stream that never recorded a completion event. A
  session that exited 0 is a normal end: its missing files are a compliance
  failure and stay blocked (the control fixture pins that).
- salvage writes only the missing evidence files, renders them from machine
  facts, declares its machine origin in handoff.md, marks the manifest pack
  salvaged_from_machine=true, and the pack then passes the validator
  precheck's judgeable/blocked scan.
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
from merge_worker_deltas import apply_deltas  # noqa: E402
from worker_salvage import (  # noqa: E402
    SALVAGE_MARKER_KEY,
    abnormal_termination_evidence,
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


def guard_for(ws: Path, *, wall: dict, stream_text: str | None = None):
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
        stream_text=stream_text,
    )


def apply_salvage(ws: Path, wall: dict, streams: dict | None = None) -> list[dict]:
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
        streams=streams or {},
    )
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


def test_termination_zero_exit_ok_outcome_clean_stream_is_normal_end():
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


def test_legacy_wall_without_outcome_maps_stays_closed_without_stream(tmp_path):
    wall = init_wall(run_id="legacy", issue_number=1)
    ws = stage_replay_dir(tmp_path)
    allowed, reasons = guard_for(ws, wall=wall)
    assert allowed is False
    assert any("session" in r.lower() for r in reasons)


def test_legacy_wall_with_stream_lacking_completion_is_abnormal(tmp_path):
    wall = init_wall(run_id="legacy", issue_number=1)
    stream_text = (FIXTURE / "worker-stream.jsonl").read_text(encoding="utf-8")
    abnormal, evidence = abnormal_termination_evidence(
        wall.get("workers") or {}, PID, stream_text=stream_text
    )
    assert abnormal is True
    assert any("completion" in e for e in evidence)


def test_stream_with_completion_event_is_not_abnormal_evidence():
    wall = init_wall(run_id="legacy", issue_number=1)
    stream_text = '{"type":"completion","result":"success"}\n'
    abnormal, _ = abnormal_termination_evidence(
        wall.get("workers") or {}, PID, stream_text=stream_text
    )
    assert abnormal is False


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
    old_ws = os.environ.get("GITHUB_WORKSPACE")
    os.environ["GITHUB_WORKSPACE"] = str(tmp_path)
    os.environ["EXPECTED_MANIFEST_SHA"] = hashlib.sha256(manifest_bytes.encode("utf-8")).hexdigest()
    os.environ["GITHUB_OUTPUT"] = str(monkey_out)
    try:
        os.chdir(tmp_path)
        with redirect_stdout(StringIO()):
            exec(compile(_precheck_heredoc_source(), "<precheck>", "exec"), {"__name__": "pre"})
    finally:
        os.chdir(old_cwd)
        if old_ws is None:
            os.environ.pop("GITHUB_WORKSPACE", None)
        else:
            os.environ["GITHUB_WORKSPACE"] = old_ws
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
    (ws / "wall-in" / "foreman-run.json").write_text(json.dumps(WALL_SHAPE))
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
    # the sha walk that follows the block covers the salvaged bytes
    for name in ("status.json", "handoff.md"):
        key = f"evidence/packs/{PID}/{name}"
        path = ev / "packs" / PID / name
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == hashlib.sha256(
            path.read_bytes()
        ).hexdigest()  # bytes stable for the walk below
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
