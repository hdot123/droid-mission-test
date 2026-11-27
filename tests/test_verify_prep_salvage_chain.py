"""BLK-1 workflow-level chain: the REAL verify step body -> the marker it
writes -> prep's pack semantics -> the salvage guard -> the adopt machine
gate, for both the green-checks+missing-files shape (expect: salvage +
adoption pass) and the red-check shape (expect: refusal + adoption fail).

Scrutiny round-1 BLK-1 (SV-1..SV-4): no existing test linked these four
steps, so `if: always()` on verify silently made the r58 death shape
unsalvageable — the marker a green worker's verify writes (problems are
only the missing evidence files) used to refuse salvage and adoption at
both consumers. This file is the anti-regression seam: every ring is the
pipeline's own code, executed for real.

Replay shape (per SV-1): the verify step body is extracted verbatim from
team.yml and run in a git-archive copy of the repo over the fixture's
worker-delivered files (reconstructed by applying the vendored diff.patch
to a base worktree — the r58 merged tree's bytes). PROCESS_JSON is the
fixture's real hslconv card.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from adopt_verdict import adopt, machine_gate_reds  # noqa: E402
from foreman_run_lib import init_wall, save_wall  # noqa: E402
from lint_workflow_wall_exits import job_spans  # noqa: E402
from merge_worker_deltas import apply_deltas  # noqa: E402
from worker_salvage import SALVAGE_MARKER_KEY, salvage_packs  # noqa: E402

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tests.replay_heredoc import (  # noqa: E402
    create_git_archive_copy,
    run_heredoc_in_clean_subprocess,
)

TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"
FIXTURE = ROOT / "tests" / "fixtures" / "worker-r58d"
PID = "hslconv"
IDS = [PID, "radixsort", "uuencode"]
WALL_KILLED_DELTA = json.loads((FIXTURE / "worker-delta-wall-killed.json").read_text())


def _verify_step_source(job: str = "worker") -> str:
    """The verify step's heredoc body, dedented to runnable Python."""
    text = TEAM_YML.read_text(encoding="utf-8")
    spans = job_spans(text)
    job_text = text[spans[job][0]:spans[job][1]]
    step = job_text.index("- name: Verify process checks and handoff")
    heredoc = job_text.index("python3 - <<'PY'\n", step) + len("python3 - <<'PY'\n")
    end = job_text.index("\n          PY\n", heredoc)
    return textwrap.dedent(job_text[heredoc:end])


def _worktree_with_delivered_files(work: Path) -> None:
    """A base worktree carrying the worker's delivered files: the vendored
    diff.patch applied to a fresh git worktree of the repo (the r58 merged
    tree's bytes). team/ protocol paths are pre-created empty so the verify
    step's commit loop sees a normal checkout."""
    subprocess.run(["git", "init", "-q", str(work)], check=True)
    # a commit so diff/apply has a base
    (work / ".gitkeep").write_text("", encoding="utf-8")
    subprocess.run(["git", "-C", str(work), "add", ".gitkeep"], check=True)
    subprocess.run(
        ["git", "-C", str(work), "-c", "user.email=t@l", "-c", "user.name=t",
         "commit", "-qm", "base"], check=True
    )
    patch = (FIXTURE / "evidence" / "packs" / PID / "diff.patch").read_bytes()
    apply_result = subprocess.run(
        ["git", "-C", str(work), "apply", "--whitespace=nowarn", "-"],
        input=patch, capture_output=True,
    )
    if apply_result.returncode != 0:
        raise AssertionError(f"diff.patch failed to apply:\n{apply_result.stderr.decode()}")
    (work / "team" / "handoffs").mkdir(parents=True, exist_ok=True)
    (work / "team" / "status").mkdir(parents=True, exist_ok=True)


@pytest.mark.parametrize(
    "red",
    [False, True],
    ids=["green-missing-files", "red-check"],
)
def test_verify_marker_prep_guard_adopt_chain(tmp_path, red: bool):
    """The full chain, both shapes, every ring real:

    ring A: the workflow's own verify step over the reconstructed worker
            tree -> the marker on disk (its content shape pinned);
    ring B: prep's per-card pack block over that workspace -> the pack
            carries prep's own checks-exit.json (green, the authority) and
            the marker copy;
    ring C: the salvage guard on the pack (green shape -> salvaged);
    ring D: the adopt machine gate (green shape -> pass stands).

    Red-shape staging mirrors the scrutiny A/B (SV-3): the same green pack
    facts with the marker toggled to a non-zero check-exit body — the red
    shape's redness lives in the worker-side marker, exactly the fact the
    content ruling keys on."""
    ws = tmp_path / "ws"
    create_git_archive_copy(ws)
    work = ws / "worktree"
    _worktree_with_delivered_files(work)

    plan = json.loads((FIXTURE / "evidence" / "plan.json").read_text(encoding="utf-8"))
    card = {p["id"]: p for p in plan["processes"]}[PID]
    proc_json = json.dumps(card, ensure_ascii=False)

    script = ws / "verify-step.sh"
    # single-quote the JSON for bash (the card body carries parentheses and
    # double quotes); the lone-quote escape keeps the export safe for any card
    quoted = "'" + proc_json.replace("'", "'\\''") + "'"
    script.write_text(
        "#!/usr/bin/env bash\n"
        f"export PROCESS_JSON={quoted}\n"
        "set -o pipefail\n"
        "python3 - <<'PY'\n"
        + _verify_step_source("worker")
        + "\nPY\n",
        encoding="utf-8",
    )
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("PROCESS_JSON", "PYTHONPATH", "GITHUB_WORKSPACE")
    }
    # CI shape: GITHUB_WORKSPACE is the checkout (the import path the step
    # seeds), cwd is the worker tree the step judges
    env["GITHUB_WORKSPACE"] = str(ws)
    env["PATH"] = os.pathsep.join([str(Path(sys.executable).parent), env.get("PATH", "")])
    proc = subprocess.run(
        ["bash", str(script)], cwd=work, env=env, capture_output=True, text=True, timeout=300
    )
    assert proc.returncode == 0, f"verify step failed:\n{proc.stdout}\n{proc.stderr}"

    marker_path = work / "team" / "status" / f"{PID}.checks-failed.marker"
    assert marker_path.is_file(), "the r58 shape (missing protocol files) must write a marker"
    marker_text = marker_path.read_text(encoding="utf-8")
    assert f"process: {PID}" in marker_text
    if red:
        # A/B toggle: same green checks, one flipped check-exit line + the
        # red problem line (the real verify step's output for a red check)
        red_text = marker_text.replace("check exit 0", "check exit 1", 1)
        red_text += f"problem: check failed (exit 1): python3 -m pytest tests/ -q\n"
        marker_path.write_text(red_text, encoding="utf-8")
        marker_text = red_text
        assert "check exit 1" in marker_text
    else:
        # the reconstruction delivered both card files, so this run's
        # problems are only the two protocol files — the green shape the
        # r58 worker actually produced (scrutiny SV-1)
        assert marker_text.count("check exit 0") == 2
        assert "missing expected file: team/handoffs/" in marker_text
        assert "missing expected file: team/status/" in marker_text

    # ring B: prep's per-card pack block — prep re-runs the card's checks
    # on the merged tree itself (here: the reconstructed worktree; both
    # shapes run them green, prep's checks-exit.json is the authority)
    ev = ws / "evidence"
    ev.mkdir()
    pack_dir = ev / "packs" / PID
    pack_dir.mkdir(parents=True)
    exits = []
    out_lines = []
    for cmd in card["checks"]:
        r = subprocess.run(cmd, shell=True, cwd=work, capture_output=True, text=True, timeout=300)
        out_lines.append(f"$ {cmd}\n{r.stdout}{r.stderr}\n[exit {r.returncode}]")
        exits.append({"command": cmd, "exit": r.returncode})
    assert all(e["exit"] == 0 for e in exits), "the reconstructed tree must re-run green"
    (pack_dir / "checks-output.txt").write_text("\n".join(out_lines), encoding="utf-8")
    (pack_dir / "checks-exit.json").write_text(json.dumps(exits, indent=2), encoding="utf-8")
    shutil.copy(work / "team" / "status" / f"{PID}.checks-failed.marker",
                pack_dir / "checks-failed.marker")
    manifest = {
        "issue": 929,
        "run_id": 1,
        "iteration": 1,
        "candidate_branch": "team/issue-929/run-1",
        "pytest_exit": 0,
        "pytest_note": "",
        "packs": {
            PID: {
                "branch": "team/issue-929/run-1/hslconv",
                "branch_present": True,
                "merged": True,
                "merge_conflict": False,
                "out_of_bounds": [],
                "checks_failed_marker": True,
                "pack": {"process_card": True, "handoff": False, "status": False,
                         "diff": True, "checks_output": True},
                "complete": False,
            }
        },
        "sha256": {},
    }
    (ev / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ev / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ring C: salvage on the wall the workers-wall-merge would have built
    wall = apply_deltas(init_wall(run_id="chain", issue_number=929), [WALL_KILLED_DELTA])
    save_wall(wall, tmp_path / "foreman-run.json")
    wall = json.loads((tmp_path / "foreman-run.json").read_text(encoding="utf-8"))
    manifest = json.loads((ev / "manifest.json").read_text(encoding="utf-8"))
    cards = {p["id"]: p for p in plan["processes"]}
    reports = salvage_packs(evidence_dir=ev, cards=cards, packs=manifest["packs"], wall=wall, manifest=manifest)
    entry = next(r for r in reports if r["pid"] == PID)

    if red:
        assert entry["salvaged"] is False
        assert any("checks-failed.marker" in r for r in entry["reasons"])
        assert not (pack_dir / "status.json").exists()
    else:
        assert entry["salvaged"] is True
        assert (pack_dir / "status.json").is_file()
        assert (pack_dir / "handoff.md").is_file()
        manifest["packs"][PID][SALVAGE_MARKER_KEY] is True
        status = json.loads((pack_dir / "status.json").read_text(encoding="utf-8"))
        assert status["state"] == "done"

    # ring D: the adopt machine gate (validator pass verdict + pack gates)
    adopt_work = tmp_path / "adopt"
    adopt_work.mkdir()
    (adopt_work / "manifest.json").write_text(json.dumps({"pytest_exit": 0, "iteration": 1}), encoding="utf-8")
    (adopt_work / "plan.json").write_text(
        json.dumps({"processes": [{"id": pid} for pid in IDS]}), encoding="utf-8"
    )
    (adopt_work / "judgeable.json").write_text(json.dumps(IDS), encoding="utf-8")
    (adopt_work / "blocked.json").write_text("{}", encoding="utf-8")
    (adopt_work / "pytest-output.txt").write_text("192 passed in 15.61s\n", encoding="utf-8")
    draft = {
        "processes": [
            {"id": pid, "verdict": "pass", "reason": "line up"} for pid in IDS
        ],
        "conflicts": [],
    }
    (adopt_work / "verdict-droid.json").write_text(json.dumps(draft), encoding="utf-8")
    (adopt_work / "verdict-droid.md").write_text("# report\n", encoding="utf-8")
    for pid in IDS:
        (adopt_work / "packs" / pid).mkdir(parents=True)
        (adopt_work / "packs" / pid / "checks-exit.json").write_text("[]", encoding="utf-8")
    shutil.copy(pack_dir / "checks-exit.json", adopt_work / "packs" / PID / "checks-exit.json")
    if (pack_dir / "checks-failed.marker").is_file():
        shutil.copy(pack_dir / "checks-failed.marker",
                    adopt_work / "packs" / PID / "checks-failed.marker")
    adopt_wall = tmp_path / "adopt-wall.json"
    save_wall(init_wall(run_id="chainadopt", issue_number=929), adopt_wall)

    old_cwd = Path.cwd()
    os.chdir(tmp_path)
    try:
        rc = adopt(adopt_work, adopt_wall, droid_exit=0, merge_step_ran=True)
    finally:
        os.chdir(old_cwd)
    assert rc == 0
    verdict = json.loads((tmp_path / "verdict.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in verdict["processes"]}
    reds = machine_gate_reds(adopt_work, IDS)
    if red:
        assert reds.get(PID), "a red-check marker must gate the process red"
        assert by_id[PID]["verdict"] == "fail"
    else:
        assert reds == {}, "a missing-file-only marker must not gate the process red"
        assert by_id[PID]["verdict"] == "pass"


def test_e2e_variant_b_marker_in_place_chain_passes(tmp_path):
    """Scrutiny SV-4 variant B made a must-pass green path: the e2e fixture
    staged WITH the marker bytes the real verify step writes (and
    checks_failed_marker=True) now ends salvaged + judgeable + not blocked."""
    e2e = pytest.importorskip("tests.test_r58d_e2e_replay")
    ws = e2e.stage_evidence(tmp_path / "variantb", e2e.FIXTURE)
    pack = ws / "evidence" / "packs" / PID
    marker = (
        f"process: {PID}\n"
        "check exit 0: python3 -m pytest tests/test_hslconv.py -q\n"
        "check exit 0: python3 -m pytest tests/ -q\n"
        f"problem: missing expected file: team/handoffs/{PID}.md\n"
        f"problem: missing expected file: team/status/{PID}.json\n"
    )
    (pack / "checks-failed.marker").write_text(marker, encoding="utf-8")
    manifest_path = ws / "evidence" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["packs"][PID]["checks_failed_marker"] = True
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    delta = e2e.run_delta_writer(ws, exit_code="124", stream=e2e.FIXTURE / "worker-stream.jsonl")
    assert delta["session_outcome"] == "wall_killed"
    wall = e2e.wall_with([delta])
    reports = e2e.run_salvage(ws, wall)
    entry = next(r for r in reports if r["pid"] == PID)
    assert entry["salvaged"] is True
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["packs"][PID][SALVAGE_MARKER_KEY] is True
    assert manifest["packs"][PID]["complete"] is True
    judgeable, blocked = e2e.run_precheck(ws)
    assert PID in judgeable
    assert blocked == {}


def test_salvage_content_verdict_module_wired_into_adopt():
    """The adopt gate must classify the marker through the shared module
    (no private re-implementation to drift)."""
    text = (ROOT / "scripts" / "team" / "adopt_verdict.py").read_text(encoding="utf-8")
    assert "marker_verdict" in text
    assert "marker_verdict_red(" in text


def test_salvage_guard_content_verdict_module_wired():
    text = (ROOT / "scripts" / "team" / "worker_salvage.py").read_text(encoding="utf-8")
    assert "marker_verdict" in text
    assert "marker_verdict_red(" in text
