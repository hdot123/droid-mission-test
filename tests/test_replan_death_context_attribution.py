"""F1b replan death-context attribution (VAL-M1-004 / VAL-M1-005).

Round-58 D-run ground truth (tests/fixtures/worker-r58d/): the hslconv
worker session was killed by the 900s wall (droid exit 124, stream tail
"Tool execution was interrupted") before it could write its two evidence
files, yet prep's machine re-run of both checks was green. The replan
input panel had no session-outcome facts, so the hardcoded blocked-reason
template blamed the process ("缺件归该工序补齐") and round 2 redid already
green work.

Contract:
- the replan prompt's "In front of you" panel carries the worker-delta
  outcome facts (session_outcome / droid_exit_code) from the wall, so the
  wall-kill death is readable in the rendered prompt (wall_killed / 124);
- the blocked-reason template used by all four merge verdict steps
  (validate / revalidate / validate2 / revalidate2) branches on the
  wall's session_outcome_by_pid: a wall-killed process gets a neutral
  attribution stating the death facts and never the worker-blame suffix
  （缺件归该工序补齐）; without the death fact the wording stays exactly
  the current one (fail-closed), including the verdict.md report line.
"""
from __future__ import annotations

import ast
import json
import shutil
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from attribution_reason import blocked_reason, blocked_report_line, neutral_attribution  # noqa: E402
from foreman_run_lib import init_wall, merge_worker_slice, save_wall  # noqa: E402
from lint_workflow_wall_exits import job_spans, step_chunks  # noqa: E402
from merge_worker_deltas import apply_deltas  # noqa: E402

TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "worker-r58d"
CONTROL_ROOT = FIXTURE_ROOT / "control-ok-missing"

REPLAN_STEP = "- name: Foreman classifies failures and writes plan v2\n"

# The single-point worker-blame suffix pinned in the four merge steps'
# blocked-reason template. The neutral branch must never emit it.
BLAME_SUFFIX = "缺件归该工序补齐"

# The four merge verdict steps whose hardcoded blocked-reason template
# must branch on the wall's session outcome (verdict reason + report line
# each).
MERGE_JOBS = ["validate", "revalidate", "validate2", "revalidate2"]

# Full death fact (from the wall-kill delta) and its absence (control):
# both render the missing-list part identically, only the attribution
# branch differs.
WALL_KILLED_DELTA = {
    "pid": "hslconv",
    "result": "failure",
    "session_outcome": "wall_killed",
    "droid_exit_code": 124,
    "stream_tail_marker": True,
}
OK_DELTA = {
    "pid": "hslconv",
    "result": "failure",
    "session_outcome": "ok",
    "droid_exit_code": 0,
    "stream_tail_marker": False,
}
MISSING = ["handoff", "status"]
DEATH_FACT = "session_outcome=wall_killed"
LEGACY_REASON_PREFIX = "料不齐（没料不验收）：缺 handoff, status"


def _team_yml() -> str:
    return TEAM_YML.read_text(encoding="utf-8")


def _merge_step_source(job: str) -> str:
    """The merge heredoc body of a validate-chain job, dedented to
    compilable Python (the heredocs import only stdlib plus the repo's
    own salvage_assemble, like the r53c replan replay)."""
    yml = _team_yml()
    spans = job_spans(yml)
    assert job in spans, f"job {job} not found in team.yml"
    start, end = spans[job]
    job_text = yml[start:end]
    for chunk in step_chunks(job_text):
        if "Merge verdict, enforce gates" not in chunk:
            continue
        heredoc = chunk.index("python3 - <<'PY'\n") + len("python3 - <<'PY'\n")
        body = chunk[heredoc:]
        end_marker = body.index("\n          PY\n")
        return textwrap.dedent(body[:end_marker])
    raise AssertionError(f"merge verdict step not found in job {job}")


def _exec_merge_step(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, job: str, wall: dict) -> dict:
    """Stage work/ (manifest+plan precheck outputs) and the wall artifact at
    wall-in/, run the workflow's own merge heredoc exactly as CI does, and
    return the merged verdict.json it writes at the step cwd — pinning is
    on the generated artifact."""
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text(
        json.dumps({"pytest_exit": 0, "iteration": 1, "sha256": {}}, ensure_ascii=False),
        encoding="utf-8",
    )
    (work / "plan.json").write_text(
        json.dumps({"processes": [{"id": "hslconv"}]}, ensure_ascii=False),
        encoding="utf-8",
    )
    (work / "judgeable.json").write_text("[]", encoding="utf-8")
    (work / "blocked.json").write_text(
        json.dumps({"hslconv": MISSING}), encoding="utf-8"
    )
    wall_in = tmp_path / "wall-in"
    wall_in.mkdir(exist_ok=True)
    save_wall(wall, wall_in / "foreman-run.json")
    monkeypatch.setenv("GITHUB_WORKSPACE", str(tmp_path))
    # prep pins the manifest digest in CI (EXPECTED_MANIFEST_SHA gate);
    # the replay must satisfy the same gate with the staged bytes.
    import hashlib

    manifest_sha = hashlib.sha256((work / "manifest.json").read_bytes()).hexdigest()
    monkeypatch.setenv("EXPECTED_MANIFEST_SHA", manifest_sha)
    monkeypatch.setenv("GITHUB_OUTPUT", str(tmp_path / "gh-out"))
    source = _merge_step_source(job)
    ast.parse(source)  # the heredoc body must remain valid Python
    exec(compile(source, f"<merge step {job}>", "exec"), {"__name__": "merge_heredoc"})
    return json.loads((tmp_path / "verdict.json").read_text(encoding="utf-8"))


def _replan_step_source() -> str:
    """The replan heredoc body, dedented to compilable Python."""
    yml = _team_yml()
    step = yml.index(REPLAN_STEP)
    heredoc = yml.index("python3 - <<'PY'\n", step) + len("python3 - <<'PY'\n")
    end = yml.index("\n          PY\n", heredoc)
    return textwrap.dedent(yml[heredoc:end])


def _exec_replan_prompt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    wall: dict,
) -> str:
    """Run the workflow's replan heredoc exactly as CI does (stage/
    prepared, the wall artifact placed at wall-in/) and return the prompt
    artifact it writes."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GITHUB_OUTPUT", str(tmp_path / "gh-out"))
    stage = tmp_path / "stage"
    stage.mkdir(exist_ok=True)
    (stage / "verdict.json").write_text(
        json.dumps(
            {
                "processes": [
                    {
                        "id": "hslconv",
                        "verdict": "blocked",
                        "reason": "料不齐（没料不验收）：缺 handoff, status",
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (stage / "plan-v1.json").write_text(
        json.dumps(
            {"summary": "r58 replay", "processes": [{"id": "hslconv", "title": "t", "files": ["hslconv.py"]}]},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (stage / "manifest.json").write_text(
        json.dumps(
            json.loads((FIXTURE_ROOT / "manifest.json").read_text(encoding="utf-8")),
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    wall_in = tmp_path / "wall-in"
    wall_in.mkdir()
    save_wall(wall, wall_in / "foreman-run.json")
    source = _replan_step_source()
    ast.parse(source)  # the heredoc body must remain valid Python
    exec(compile(source, "<replan step>", "exec"), {"__name__": "replan_heredoc"})
    return (tmp_path / "replan-prompt.txt").read_text(encoding="utf-8")


def _wall_from_delta(delta: dict) -> dict:
    """A wall carrying one delta's outcome facts via the F1 merge path —
    the unit-level shape of what the workers-wall-merge job writes."""
    return apply_deltas(init_wall(run_id="45812793849", issue_number=929), [delta])


def _wall_with_outcome(delta: dict) -> dict:
    """A wall whose workers slice carries the delta's outcome facts —
    the same machine path the workers-wall-merge job uses (F1)."""
    return _wall_from_delta(delta)


# ---------------------------------------------------------------------------
# VAL-M1-004: the replan input panel carries the session outcome facts
# ---------------------------------------------------------------------------


def test_r58_death_wall_renders_outcome_facts_into_replan_panel(
    tmp_path, monkeypatch
):
    wall = _wall_with_outcome(WALL_KILLED_DELTA)
    prompt = _exec_replan_prompt(tmp_path, monkeypatch, wall=wall)
    assert "session_outcome=wall_killed" in prompt
    assert "droid exit 124" in prompt


def test_control_ok_wall_renders_ok_outcome_into_replan_panel(
    tmp_path, monkeypatch
):
    wall = _wall_with_outcome(OK_DELTA)
    prompt = _exec_replan_prompt(tmp_path, monkeypatch, wall=wall)
    assert "session_outcome: ok" in prompt
    assert "droid_exit_code: 0" in prompt


def test_r58_replan_panel_wording_rules_on_death_shape(tmp_path, monkeypatch):
    wall = _wall_with_outcome(WALL_KILLED_DELTA)
    prompt = _exec_replan_prompt(tmp_path, monkeypatch, wall=wall)
    # neutral attribution wording must be present verbatim...
    assert neutral_attribution(pid="hslconv", exit_code=124) in prompt
    # ...and the worker-blame suffix must never appear in a death-shaped
    # prompt (the prompt template carries no unconditional blame line).
    assert BLAME_SUFFIX not in prompt


def test_r58_replan_panel_pins_exact_input_facts_block(tmp_path, monkeypatch):
    """The panel is part of the "In front of you" input face, stated as
    machine-recorded facts (no judge language)."""
    wall = _wall_with_outcome(WALL_KILLED_DELTA)
    prompt = _exec_replan_prompt(tmp_path, monkeypatch, wall=wall)
    assert "Worker session outcome facts (machine-recorded, from the ForemanRun wall)" in prompt
    assert "- process `hslconv`:" in prompt


def test_replan_panel_absent_outcome_facts_say_absent(tmp_path, monkeypatch):
    """Legacy walls (pre-F1) carry no outcome maps: the panel must say so
    explicitly instead of dropping the block (death-absence is also a
    fact the foreman needs for fail-closed attribution)."""
    wall = init_wall(run_id="45812793849", issue_number=929)
    prompt = _exec_replan_prompt(tmp_path, monkeypatch, wall=wall)
    assert "no session outcome facts recorded on the wall (pre-delta run)" in prompt


# ---------------------------------------------------------------------------
# VAL-M1-005: the blocked-reason template branches on the session outcome
# ---------------------------------------------------------------------------


def test_neutral_attribution_states_death_facts_without_worker_blame():
    reason = blocked_reason("hslconv", MISSING, wall=_wall_from_delta(WALL_KILLED_DELTA))
    assert reason.startswith("料不齐（没料不验收）：缺 handoff, status")
    assert DEATH_FACT in reason
    assert "exit 124" in reason
    assert "900s 墙杀" in reason
    assert BLAME_SUFFIX not in reason


def test_neutral_attribution_no_worker_compliance_wording():
    reason = blocked_reason("hslconv", MISSING, wall=_wall_from_delta(WALL_KILLED_DELTA))
    assert "补齐" not in reason
    assert "工序" not in reason.split("（")[0]


def test_reason_without_death_fact_keeps_current_wording_fail_closed():
    delta = {k: v for k, v in OK_DELTA.items() if k != "session_outcome"}
    reason = blocked_reason("hslconv", MISSING, wall=_wall_from_delta(delta))
    assert reason == "料不齐（没料不验收）：缺 handoff, status（缺件归该工序补齐）"


def test_reason_with_session_ok_keeps_current_wording_fail_closed():
    reason = blocked_reason("hslconv", MISSING, wall=_wall_from_delta(OK_DELTA))
    assert reason == "料不齐（没料不验收）：缺 handoff, status（缺件归该工序补齐）"


def test_reason_without_wall_keeps_current_wording():
    assert blocked_reason("hslconv", MISSING) == (
        "料不齐（没料不验收）：缺 handoff, status（缺件归该工序补齐）"
    )


def test_reason_with_wall_but_no_record_for_pid_keeps_current_wording():
    delta = dict(WALL_KILLED_DELTA)
    delta["pid"] = "another"
    reason = blocked_reason("hslconv", MISSING, wall=_wall_from_delta(delta))
    assert reason == "料不齐（没料不验收）：缺 handoff, status（缺件归该工序补齐）"


def test_wall_killed_reason_carries_only_the_truth_not_machine_green_claims():
    """The blocked reason is the validator's failure record; it must state
    the death fact but must not claim checks were green (that evidence
    lives in the manifest, not in the delta-backed reason)."""
    reason = blocked_reason("hslconv", MISSING, wall=_wall_from_delta(WALL_KILLED_DELTA))
    assert "全绿" not in reason
    assert "salvage" not in reason


def test_blocked_report_line_neutral_branch_matches_reason_branch():
    wall = _wall_from_delta(WALL_KILLED_DELTA)
    line = blocked_report_line("hslconv", MISSING, wall=wall)
    reason = blocked_reason("hslconv", MISSING, wall=wall)
    assert line == f"- `hslconv`：blocked — 料不齐，缺 handoff, status（{reason[len('料不齐（没料不验收）：缺 handoff, status（'):]}"
    assert BLAME_SUFFIX not in line


def test_blocked_report_line_without_death_fact_matches_current_wording():
    line = blocked_report_line("hslconv", MISSING, wall=_wall_from_delta(OK_DELTA))
    assert line == "- `hslconv`：blocked — 料不齐，缺 handoff, status（缺件归该工序补齐）"


# ---------------------------------------------------------------------------
# Wiring: all four merge steps and their report-line twins use the module
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("job", MERGE_JOBS)
def test_merge_step_branches_blocked_reason_on_wall(tmp_path, monkeypatch, job):
    wall = _wall_with_outcome(WALL_KILLED_DELTA)
    verdict = _exec_merge_step(tmp_path, monkeypatch, job, wall)
    entry = next(p for p in verdict["processes"] if p["id"] == "hslconv")
    assert entry["verdict"] == "blocked"
    assert DEATH_FACT in entry["reason"]
    assert "exit 124" in entry["reason"]
    assert BLAME_SUFFIX not in entry["reason"]


@pytest.mark.parametrize("job", MERGE_JOBS)
def test_merge_step_without_death_fact_keeps_current_reason(
    tmp_path, monkeypatch, job
):
    wall = _wall_with_outcome(OK_DELTA)
    verdict = _exec_merge_step(tmp_path, monkeypatch, job, wall)
    entry = next(p for p in verdict["processes"] if p["id"] == "hslconv")
    assert entry["reason"] == (
        "料不齐（没料不验收）：缺 handoff, status（缺件归该工序补齐）"
    )


@pytest.mark.parametrize("job", MERGE_JOBS)
def test_merge_step_reads_outcome_from_copied_wall(tmp_path, monkeypatch, job):
    """The steps copy wall-in/foreman-run.json to workdir foreman-run.json
    before merging (r58 shape, upload-artifact overwrite); with the workdir
    copy present it must be honored (it is what adopt later reads)."""
    wall = _wall_with_outcome(WALL_KILLED_DELTA)
    wall_in = tmp_path / "wall-in"
    wall_in.mkdir(exist_ok=True)
    save_wall(wall, wall_in / "foreman-run.json")
    shutil.copy(wall_in / "foreman-run.json", tmp_path / "foreman-run.json")
    verdict = _exec_merge_step(tmp_path, monkeypatch, job, wall)
    assert DEATH_FACT in next(
        p["reason"] for p in verdict["processes"] if p["id"] == "hslconv"
    )


@pytest.mark.parametrize("job", MERGE_JOBS)
def test_merge_step_report_line_branches_with_reason(
    tmp_path, monkeypatch, job
):
    wall = _wall_with_outcome(WALL_KILLED_DELTA)
    _exec_merge_step(tmp_path, monkeypatch, job, wall)
    report = (tmp_path / "verdict.md").read_text(encoding="utf-8")
    assert BLAME_SUFFIX not in report
    assert "blocked — 料不齐" in report
    assert DEATH_FACT in report


@pytest.mark.parametrize("job", MERGE_JOBS)
def test_merge_step_report_line_without_death_fact_keeps_wording(
    tmp_path, monkeypatch, job
):
    wall = _wall_with_outcome(OK_DELTA)
    _exec_merge_step(tmp_path, monkeypatch, job, wall)
    report = (tmp_path / "verdict.md").read_text(encoding="utf-8")
    assert BLAME_SUFFIX in report


def test_merge_steps_wire_attribution_module_and_context():
    """Structural wiring lock: each merge heredoc imports the module, loads
    the wall (workdir copy first, else wall-in), and passes it straight to
    the attribution calls — no hardcoded template may survive in the step."""
    wall_load = (
        'wall = json.load(open("foreman-run.json")) if os.path.exists("foreman-run.json") '
        'else (json.load(open("wall-in/foreman-run.json")) if os.path.exists("wall-in/foreman-run.json") else {})'
    )
    for job in MERGE_JOBS:
        src = _merge_step_source(job)
        assert "from attribution_reason import" in src, job
        assert wall_load in src, job
        assert "blocked_reason(pid, missing, wall=wall)" in src, job
        assert "blocked_report_line(pid, missing, wall=wall)" in src, job


def test_workflow_has_zero_hardcoded_blame_templates():
    """Single-point eradication: the blame suffix appears nowhere in
    team.yml — all eight template sites (4 steps x reason + report line)
    go through the attribution module, whose no-death branch carries the
    only copy (fail-closed wording lives in one reviewed place)."""
    assert BLAME_SUFFIX not in _team_yml()


def test_workflow_carries_eight_attribution_call_sites():
    """Four merge steps x (verdict reason + report line) = 8 module call
    sites; no hardcoded 同款 template may remain."""
    yml = _team_yml()
    assert yml.count("blocked_reason(") == len(MERGE_JOBS)
    assert yml.count("blocked_report_line(") == len(MERGE_JOBS)


# ---------------------------------------------------------------------------
# Module contract: the wall is the single death-fact source
# ---------------------------------------------------------------------------


def test_module_reason_reads_outcome_only_from_wall():
    """The death fact must come from the wall's workers slice (F1), never
    from a heuristic on the missing list (a full pack can still belong to
    a wall-killed worker whose files were salvaged later; the wall stays
    the machine-recorded outcome source)."""
    import inspect

    src = inspect.getsource(blocked_reason)
    assert "wall" in src
    assert "session_outcome_by_pid" in src
    assert "missing" in src  # missing list only shapes the 缺 list


def test_merge_worker_slice_neutral_wall_roundtrip():
    """Wall-level replay: the F1 delta path (apply_deltas) feeding the
    attribution module with the full wall — proving the death fact rides
    the same slice the workers-wall-merge job writes and the merge steps
    load."""
    wall = init_wall(run_id="45812793849", issue_number=929)
    wall = apply_deltas(wall, [WALL_KILLED_DELTA])
    workers = wall["workers"]
    assert workers["session_outcome_by_pid"]["hslconv"] == "wall_killed"
    reason = blocked_reason("hslconv", MISSING, wall=wall)
    assert DEATH_FACT in reason
    assert "exit 124" in reason
    merge_worker_slice(wall, "hslconv", "failure")  # idempotent merge path stays callable
