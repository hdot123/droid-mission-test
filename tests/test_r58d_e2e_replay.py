"""VAL-CROSS-001/002: the round-58 dead chain and its contrast, replayed
end to end offline against the vendored fixtures.

Two chains, one fixture pair (tests/fixtures/worker-r58d/):

Dead chain (verbatim r58 evidence, hslconv):
  wall-killed session (exit 124, interrupted tool_error tail) → the delta
  step classifies the outcome from the fixture's own stream bytes → the
  wall records the death facts → the blocked-reason template and the replan
  input panel both turn neutral → the salvage guard reads all conditions
  true → the machine writes status.json + handoff.md and marks the pack
  salvaged_from_machine → the validator precheck scan judges the pack
  judgeable (hslconv), nothing blocked.

Contrast chain (synthetic control, same run shape, session completed ok):
  delta ok → the wording stays exactly the current one (the worker-blame
  suffix survives) → the guard refuses (normal end = compliance failure) →
  no salvage products, manifest untouched → the precheck scan keeps the
  pack blocked.

Every ring is the pipeline's own code: the delta comes from the real CLI
(write_worker_delta.py), the wall from the real merge (merge_worker_deltas),
the reason from attribution_reason, the salvage from worker_salvage, the
panel from the workflow's own replan heredoc replayed in a clean
subprocess, and the judgeable/blocked scan from the workflow's own precheck
heredoc. Zero live triggers: fixtures only, no team.yml run.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from attribution_reason import BLAME_SUFFIX, blocked_reason, blocked_report_line  # noqa: E402
from foreman_run_lib import init_wall, save_wall  # noqa: E402
from merge_worker_deltas import apply_deltas  # noqa: E402
from worker_salvage import SALVAGE_MARKER_KEY, salvage_packs  # noqa: E402

# `python3 -m pytest` (the repo-mandated form) puts the repo root on
# sys.path; bare pytest does not, so seed it before the helper import.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tests.replay_heredoc import (  # noqa: E402
    create_git_archive_copy,
    replan_heredoc_source,
    run_heredoc_in_clean_subprocess,
    stage_replan_replay_dir,
)

TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"
FIXTURE = ROOT / "tests" / "fixtures" / "worker-r58d"
CONTROL = FIXTURE / "control-ok-missing"
PID = "hslconv"
MISSING = ["handoff", "status"]
PRECHECK_STEP = "- name: Extract and precheck evidence packs\n"
LEGACY_REASON_PREFIX = "料不齐（没料不验收）：缺 handoff, status"


# --- ring 1: the delta step, judged from the fixture's own stream bytes ------


def run_delta_writer(tmp_path: Path, *, exit_code: str, stream: Path) -> dict:
    """Run the workflow's real delta CLI the way the session step does
    (DROID_EXIT_CODE + stream file), from a workspace with no team/ marker
    tree, and return the delta it wrote."""
    out = tmp_path / "worker-delta.json"
    env = {k: v for k, v in os.environ.items() if k != "JOB_STATUS"}
    env["DROID_EXIT_CODE"] = exit_code
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "team" / "write_worker_delta.py"),
            "--pid", PID,
            "--result", "failure",
            "--out", str(out),
            "--stream", str(stream),
        ],
        cwd=str(tmp_path),
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, f"delta CLI failed:\n{proc.stderr}"
    return json.loads(out.read_text(encoding="utf-8"))


def wall_with(deltas: list[dict]) -> dict:
    """The wall shape the workers-wall-merge job writes for these deltas."""
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
    return wall


# --- rings 2-4 staging --------------------------------------------------------


def stage_evidence(tmp_path: Path, fixture: Path) -> Path:
    """A prep-shaped workspace: evidence/ (manifest+plan inside) + wall slot."""
    ev = tmp_path / "evidence"
    ev.mkdir(parents=True)
    shutil.copytree(fixture / "evidence", ev, dirs_exist_ok=True)
    shutil.copy(fixture / "manifest.json", ev / "manifest.json")
    if not (ev / "plan.json").is_file():
        shutil.copy(FIXTURE / "evidence" / "plan.json", ev / "plan.json")
    return tmp_path


def run_salvage(ws: Path, wall: dict) -> list[dict]:
    """The prep salvage block's library face, with the workflow's persistence
    rule: the refreshed manifest hits disk only when something was salvaged."""
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


def render_replan_panel(tmp_path: Path, wall: dict) -> str:
    """The workflow's own replan heredoc, replayed in a clean subprocess
    (CI import fidelity, tests/replay_heredoc.py) with the wall artifact at
    wall-in/; returns the prompt artifact the step writes."""
    replay_dir = tmp_path / "replan-replay"
    create_git_archive_copy(replay_dir)
    stage_replan_replay_dir(replay_dir)
    stage = replay_dir / "stage"
    (stage / "verdict.json").write_text(
        json.dumps(
            {"processes": [{"id": PID, "verdict": "blocked", "reason": LEGACY_REASON_PREFIX}]},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (stage / "plan-v1.json").write_text(
        json.dumps(
            {"summary": "r58 e2e replay", "processes": [{"id": PID, "title": "t", "files": [f"{PID}.py"]}]},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (stage / "manifest.json").write_text(
        (FIXTURE / "manifest.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    wall_in = replay_dir / "wall-in"
    wall_in.mkdir(exist_ok=True)
    save_wall(wall, wall_in / "foreman-run.json")
    proc = run_heredoc_in_clean_subprocess(replan_heredoc_source(), cwd=replay_dir)
    assert proc.returncode == 0, f"replan heredoc failed in clean subprocess:\n{proc.stderr}"
    return (replay_dir / "replan-prompt.txt").read_text(encoding="utf-8")


def _precheck_heredoc_source() -> str:
    yml = TEAM_YML.read_text(encoding="utf-8")
    step = yml.index(PRECHECK_STEP)
    heredoc = yml.index("python3 - <<'PY'\n", step) + len("python3 - <<'PY'\n")
    end = yml.index("\n          PY\n", heredoc)
    return textwrap.dedent(yml[heredoc:end])


def run_precheck(ws: Path) -> tuple[list, dict]:
    """Stage work/ the way the validate job sees it and run the workflow's
    own precheck heredoc verbatim; returns (judgeable, blocked).

    One replay-surface adaptation, documented per PROVENANCE: the sibling
    packs are attested debt (sha256 keys in the manifest, bytes not vendored),
    so the staged manifest drops exactly the keys whose bytes are absent —
    the packs dict is untouched, and the EXPECTED_MANIFEST_SHA gate is fed
    the reduced bytes. Kept keys are asserted non-empty so an empty sha walk
    can never fake a green."""
    work = ws / "work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text(encoding="utf-8"))
    manifest["sha256"] = {
        rel: digest
        for rel, digest in (manifest.get("sha256") or {}).items()
        if (ws / "evidence" / rel[len("evidence/"):]).is_file()
    }
    assert manifest["sha256"], "precheck staging dropped every sha key — not a green path"
    manifest_bytes = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    (work / "manifest.json").write_bytes(manifest_bytes.encode("utf-8"))
    for rel in manifest["sha256"]:
        dst = work / rel[len("evidence/"):]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ws / "evidence" / rel[len("evidence/"):], dst)
    for member in ("plan.json", "check-summary.json", "pytest-output.txt",
                   "pytest-exit.txt", "candidate-branch.txt"):
        src = ws / "evidence" / member
        if src.is_file() and not (work / member).exists():
            shutil.copy(src, work / member)
    gh_out = ws / "gh-output"
    old_cwd = Path.cwd()
    old_env = {k: os.environ.get(k)
               for k in ("GITHUB_WORKSPACE", "EXPECTED_MANIFEST_SHA", "GITHUB_OUTPUT")}
    os.environ["GITHUB_WORKSPACE"] = str(ws)
    os.environ["EXPECTED_MANIFEST_SHA"] = hashlib.sha256(manifest_bytes.encode("utf-8")).hexdigest()
    os.environ["GITHUB_OUTPUT"] = str(gh_out)
    try:
        os.chdir(ws)
        exec(compile(_precheck_heredoc_source(), "<precheck>", "exec"), {"__name__": "pre"})
    finally:
        os.chdir(old_cwd)
        for k, v in old_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return (
        json.loads((work / "judgeable.json").read_text(encoding="utf-8")),
        json.loads((work / "blocked.json").read_text(encoding="utf-8")),
    )


# --- VAL-CROSS-001: the dead chain, ring by ring ------------------------------


def test_ring1_delta_step_classifies_wall_killed_from_fixture_stream(tmp_path):
    delta = run_delta_writer(
        tmp_path, exit_code="124", stream=FIXTURE / "worker-stream.jsonl"
    )
    pinned = json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text(encoding="utf-8"))
    assert delta == pinned, "the CLI must classify the r58 stream exactly as the pinned contract"
    wall = wall_with([delta])
    workers = wall["workers"]
    assert workers["session_outcome_by_pid"][PID] == "wall_killed"
    assert workers["droid_exit_code_by_pid"][PID] == 124
    assert workers["stream_tail_marker_by_pid"][PID] is True


def test_ring2_attribution_turns_neutral_on_death_fact(tmp_path):
    wall = wall_with([json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text(encoding="utf-8"))])
    reason = blocked_reason(PID, MISSING, wall=wall)
    assert reason.startswith(LEGACY_REASON_PREFIX)
    assert BLAME_SUFFIX not in reason
    assert "中性归因" in reason
    assert "session_outcome=wall_killed" in reason
    assert "900s" in reason
    report_line = blocked_report_line(PID, MISSING, wall=wall)
    assert BLAME_SUFFIX not in report_line
    prompt = render_replan_panel(tmp_path, wall)
    assert "session_outcome=wall_killed" in prompt
    assert "droid exit 124" in prompt
    assert "Attribute this neutrally" in prompt
    assert BLAME_SUFFIX not in prompt


def test_ring3_salvage_guard_accepts_and_writes_machine_products(tmp_path):
    ws = stage_evidence(tmp_path, FIXTURE)
    wall = wall_with([json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text(encoding="utf-8"))])
    reports = run_salvage(ws, wall)
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True
    assert any("abnormal session end" in r for r in entry["reasons"])
    pack = ws / "evidence" / "packs" / PID
    status = json.loads((pack / "status.json").read_text(encoding="utf-8"))
    assert status["id"] == PID and status["title"]
    assert status["state"] == "done"
    assert isinstance(status["files"], list) and status["files"]
    checks_exit = json.loads((pack / "checks-exit.json").read_text(encoding="utf-8"))
    assert [c["command"] for c in status["checks"]] == [e["command"] for e in checks_exit]
    assert all(c["result"].endswith("[exit 0]") for c in status["checks"])
    handoff = (pack / "handoff.md").read_text(encoding="utf-8")
    assert "补卷器生成" in handoff and "非工人亲写" in handoff
    assert "900s" in handoff and "机器复验全绿" in handoff
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["packs"][PID][SALVAGE_MARKER_KEY] is True
    assert manifest["packs"][PID]["complete"] is True


def test_ring4_precheck_scan_judges_salvaged_pack(tmp_path):
    ws = stage_evidence(tmp_path, FIXTURE)
    wall = wall_with([json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text(encoding="utf-8"))])
    run_salvage(ws, wall)
    judgeable, blocked = run_precheck(ws)
    assert PID in judgeable
    assert blocked == {}


def test_r58_dead_chain_end_to_end(tmp_path):
    """VAL-CROSS-001 in one flow: delta → wall → neutral attribution →
    guard → salvage products → precheck judgeable. Every ring consumes the
    previous ring's artifact on the same workspace."""
    ws = stage_evidence(tmp_path / "dead", FIXTURE)
    # ring 1: the session step's exit code and stream → structured outcome
    delta = run_delta_writer(ws, exit_code="124", stream=FIXTURE / "worker-stream.jsonl")
    assert delta["session_outcome"] == "wall_killed"
    wall = wall_with([delta])
    assert wall["workers"]["droid_exit_code_by_pid"][PID] == 124
    # ring 2: the wall's death facts neutralize the blame template + panel
    reason = blocked_reason(PID, MISSING, wall=wall)
    assert BLAME_SUFFIX not in reason and "中性归因" in reason
    prompt = render_replan_panel(ws, wall)
    assert "session_outcome=wall_killed" in prompt and BLAME_SUFFIX not in prompt
    # ring 3: guard all-true → the two evidence files, machine-rendered
    reports = run_salvage(ws, wall)
    assert next(r for r in reports if r["pid"] == PID)["salvaged"] is True
    manifest = json.loads((ws / "evidence" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["packs"][PID]["complete"] is True
    # ring 4: the validator scan judges the pack — no longer blocked
    judgeable, blocked = run_precheck(ws)
    assert PID in judgeable and blocked == {}


# --- VAL-CROSS-002: the contrast chain stays blocked, fail-closed -------------


def test_control_chain_end_to_end_stays_blocked(tmp_path):
    ws = stage_evidence(tmp_path / "control", CONTROL)
    # ring 1: a healthy session (exit 0, normal completion tail) → ok
    delta = run_delta_writer(ws, exit_code="0", stream=CONTROL / "worker-stream-tail.jsonl")
    assert delta["session_outcome"] == "ok"
    assert delta["droid_exit_code"] == 0
    assert delta["stream_tail_marker"] is False
    wall = wall_with([delta])
    assert wall["workers"]["session_outcome_by_pid"][PID] == "ok"
    # ring 2: no death fact → the current wording, byte-for-byte
    reason = blocked_reason(PID, MISSING, wall=wall)
    assert reason == f"{LEGACY_REASON_PREFIX}（{BLAME_SUFFIX}）"
    report_line = blocked_report_line(PID, MISSING, wall=wall)
    assert report_line.endswith(f"（{BLAME_SUFFIX}）")
    assert "中性归因" not in reason and "900s" not in reason
    prompt = render_replan_panel(ws, wall)
    assert "session_outcome: ok" in prompt
    assert "droid_exit_code: 0" in prompt
    # no death fact → no neutral-attribution instruction on the panel (the
    # redispatch-vs-revise fork keeps its plain worker-blame framing); the
    # verdict reason itself carries the blame suffix
    assert "Attribute this neutrally" not in prompt
    assert BLAME_SUFFIX in reason
    # ring 3: the guard refuses a normal end — no salvage, manifest untouched
    manifest_before = (ws / "evidence" / "manifest.json").read_bytes()
    reports = run_salvage(ws, wall)
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is False
    assert any("normal session end" in r for r in entry["reasons"])
    assert not (ws / "evidence" / "packs" / PID / "status.json").exists()
    assert not (ws / "evidence" / "packs" / PID / "handoff.md").exists()
    assert SALVAGE_MARKER_KEY not in json.loads(
        (ws / "evidence" / "manifest.json").read_text(encoding="utf-8")
    )["packs"][PID]
    assert (ws / "evidence" / "manifest.json").read_bytes() == manifest_before
    # ring 4: the scan keeps the pack blocked with the missing evidence named
    judgeable, blocked = run_precheck(ws)
    assert judgeable == []
    assert PID in blocked
    assert "handoff" in blocked[PID] and "status" in blocked[PID]
