"""VAL-M4-002 / VAL-M4-005 replay: replan context truth and accounting semantics.

Round-53 factual ground (adversarial/round53-verify/verify-targeted.md):
- §4: all 12 round-2 redispatch cards' retry_note demanded a diff from the
  worker, but the validator's "missing diff" refers to prep's own
  git-diff-generated pack member; the packs were empty because F-1 rejected
  every worker session before its branch push (branch_present=false in all
  packs), so the real cause is the absent branch, not a missing worker
  deliverable. The C-ascii85 worker who followed the note literally wrote
  team/diffs/ascii85.diff — one more out-of-bounds file.
- §6: validate2 with judgeable==[] never started a droid session (the
  judging step's `if` skipped it, droid-exit.txt never existed), yet the
  wall recorded budgets.session_outcome = missing_output / exit_code -1 —
  an accounting artifact presented as a failed session.

Fixtures: tests/fixtures/validator-r53c/ — run C (45125143118) round-2
plan + manifest verbatim (extract.py and provenance.txt beside them).
"""
from __future__ import annotations

import ast
import copy
import json
import shutil
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from adopt_verdict import adopt  # noqa: E402
from budget_resolve import adopt_session_completion_status  # noqa: E402
from compute_validate_conclusion import derive  # noqa: E402
from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402

TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"
REPLAN_STEP = "- name: Foreman classifies failures and writes plan v2\n"
FIXTURES = ROOT / "tests" / "fixtures" / "validator-r53c"
PIDS = ["ascii85", "nthweekday", "substitution"]
RUN_ID = "45125143118"

# Diff-demand shapes the round-53 replan prompts actually carried (the
# worker-facing contract error; verify-targeted §4). None of these may
# appear in a replan prompt again — neither in the prompt template nor in
# the runtime-interpolated artifact.
DIFF_DEMAND_PHRASES = (
    "write the status file, the handoff document, and the diff",
    "as required by the team protocol",
    "write the diff",
    "commit the diff",
)
# Runtime-only shapes: the worker-facing forbidden path appears in the
# builder's explanatory prose as a bare literal; the runtime context block
# cites a worker-written out-of-bounds file as cause text. The forbidden
# demand (asking the worker to produce it) is what the phrases above pin.
RUNTIME_FORBIDDEN = ("team/diffs/",)


def _team_yml() -> str:
    return TEAM_YML.read_text(encoding="utf-8")


def _replan_prompt() -> str:
    yml = _team_yml()
    step = yml.index(REPLAN_STEP)
    start = yml.index('prompt = f"""', step) + len('prompt = f"""')
    end = yml.index('"""', start)
    return yml[start:end]


def _replan_step_source() -> str:
    """The replan heredoc body, dedented to compilable Python."""
    yml = _team_yml()
    step = yml.index(REPLAN_STEP)
    heredoc = yml.index("python3 - <<'PY'\n", step) + len("python3 - <<'PY'\n")
    end = yml.index("\n          PY\n", heredoc)
    return textwrap.dedent(yml[heredoc:end])


def _r53c_inputs() -> tuple[dict, dict]:
    manifest = json.loads((FIXTURES / "manifest.json").read_text(encoding="utf-8"))
    plan = json.loads((FIXTURES / "plan.json").read_text(encoding="utf-8"))
    return manifest, plan


def _blocked_from_manifest(manifest: dict) -> tuple[list, dict]:
    """Mirror of the team.yml evidence-precheck blocked-list construction
    ("Extract and precheck evidence packs" step, round-2 variant: the
    unmerged marker is 未合并/未替换). Kept verbatim so any wording drift in
    team.yml surfaces here as a red test."""
    judgeable, blocked = [], {}
    for pid, info in manifest["packs"].items():
        if info["complete"]:
            judgeable.append(pid)
        else:
            missing = [k for k, v in info["pack"].items() if not v]
            if not info["merged"]:
                missing.append("未合并/未替换")
            if info.get("out_of_bounds"):
                missing.append("越界文件：" + ", ".join(info["out_of_bounds"]))
            blocked[pid] = missing
    return judgeable, blocked


def _r53c_work(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    manifest: dict | None = None,
    judgeable: list | None = None,
    blocked: dict | None = None,
) -> tuple[Path, Path]:
    """Run-C-shaped validate2 pre-work: fixture manifest/plan plus the given
    precheck outputs; droid-exit.txt deliberately absent (the session the
    `if` gate skipped never writes one)."""
    monkeypatch.chdir(tmp_path)
    manifest = manifest if manifest is not None else _r53c_inputs()[0]
    plan = _r53c_inputs()[1]
    judgeable = PIDS if judgeable is None else judgeable
    blocked = {} if blocked is None else blocked
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="r53c", issue_number=792), wall_path)
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    (work / "judgeable.json").write_text(json.dumps(judgeable), encoding="utf-8")
    (work / "blocked.json").write_text(json.dumps(blocked), encoding="utf-8")
    return wall_path, work


# ---------------------------------------------------------------------------
# VAL-M4-002: the replan context speaks the real cause, never demands a diff
# ---------------------------------------------------------------------------


def _exec_replan_prompt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    manifest: dict,
    plan: dict,
) -> str:
    """Run the workflow's replan heredoc exactly as CI does (stage/ prepared,
    the manifest the replan job unpacks placed beside it) and return the
    prompt artifact it writes — the f-string collapses braces and
    interpolates the failed/blocked line blocks, so pinning is on the
    generated artifact."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GITHUB_OUTPUT", str(tmp_path / "gh-out"))
    stage = tmp_path / "stage"
    stage.mkdir(exist_ok=True)
    (stage / "verdict.json").write_text(
        json.dumps({"processes": []}, ensure_ascii=False), encoding="utf-8"
    )
    (stage / "plan-v1.json").write_text(
        json.dumps(plan, ensure_ascii=False), encoding="utf-8"
    )
    (stage / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
    )
    source = _replan_step_source()
    ast.parse(source)  # the heredoc body must remain valid Python
    exec(compile(source, "<replan step>", "exec"), {"__name__": "replan_heredoc"})
    return (tmp_path / "replan-prompt.txt").read_text(encoding="utf-8")


def _r53c_manifest_r1() -> dict:
    """The round-1 evidence manifest — the file the replan job actually
    unpacks into stage/ (the round-2 one sits beside it for the adopt-side
    replays)."""
    path = FIXTURES / "manifest-r1.json"
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# VAL-M4-002: the replan context speaks the real cause, never demands a diff
# ---------------------------------------------------------------------------


def _r53c_manifest_with_oob() -> dict:
    manifest, _ = _r53c_inputs()
    manifest = copy.deepcopy(manifest)
    manifest["packs"]["ascii85"]["out_of_bounds"] = ["team/diffs/ascii85.diff"]
    return manifest


def test_replan_prompt_names_absent_branch_as_real_cause(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    manifest, plan = _r53c_inputs()
    judgeable, blocked = _blocked_from_manifest(manifest)
    assert judgeable == [] and set(blocked) == set(PIDS)
    prompt = _exec_replan_prompt(
        tmp_path, monkeypatch, _r53c_manifest_r1(), plan
    )
    for pid in PIDS:
        line = (
            f"the round-1 branch for process `{pid}` was never pushed "
            "(the F-1 check rejected the session before its branch push)"
        )
        assert line in prompt, pid
        assert prompt.count(line) == 1


def test_replan_prompt_names_out_of_bounds_without_relaunching_the_loop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    manifest = _r53c_manifest_with_oob()
    plan = _r53c_inputs()[1]
    prompt = _exec_replan_prompt(tmp_path, monkeypatch, manifest, plan)
    for pid in PIDS:
        if pid == "ascii85":
            continue
        line = (
            f"the round-1 branch for process `{pid}` was never pushed "
            "(the F-1 check rejected the session before its branch push)"
        )
        assert line in prompt
    assert (
        "out-of-bounds file(s) the worker session wrote "
        "(the only worker-side file violation): team/diffs/ascii85.diff"
    ) in prompt
    assert "must not be recreated by the next session" in prompt


def test_replan_prompt_never_demands_diff_from_worker():
    prompt = _replan_prompt()
    hits = [p for p in DIFF_DEMAND_PHRASES if p in prompt]
    assert not hits, f"replan prompt template still demands a worker-produced diff: {hits}"
    # repo-wide belt: the round-53 contract-error phrase family must not live
    # anywhere in the workflow text (fixtures keep the real 53 retry_notes
    # verbatim as evidence, so the walk-through excludes tests/fixtures the
    # same way the mission's grep discipline excludes read-only evidence)
    yml = _team_yml()
    assert "as required by the team protocol" not in yml


def test_workflow_sources_free_of_diff_demand_phrases():
    """grep discipline (rg --hidden --no-ignore): the phrase family is gone
    from every tracked workflow/script/test source; fixtures are excluded —
    they are the verbatim round-53 evidence (immutable by convention)."""
    for path in TEAM_YML, *sorted((ROOT / "scripts" / "team").glob("*.py")):
        text = path.read_text(encoding="utf-8")
        hits = [p for p in DIFF_DEMAND_PHRASES if p in text]
        assert not hits, f"{path.name} still carries diff-demand phrases: {hits}"


def test_runtime_prompt_artifact_never_demands_diff_from_worker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    manifest = _r53c_manifest_with_oob()
    plan = _r53c_inputs()[1]
    prompt = _exec_replan_prompt(tmp_path, monkeypatch, manifest, plan)
    hits = [p for p in DIFF_DEMAND_PHRASES if p in prompt]
    assert not hits, f"generated replan prompt demands a worker-produced diff: {hits}"
    # The only legitimate mention of a worker-written out-of-bounds path is
    # the cause citation paired with the do-not-recreate instruction.
    for hit in RUNTIME_FORBIDDEN:
        idx = 0
        while True:
            idx = prompt.find(hit, idx)
            if idx == -1:
                break
            window = prompt[idx : idx + 200]
            assert "must not be recreated by the next session" in window, (
                f"bare forbidden path without the do-not-recreate instruction: {window!r}"
            )
            idx += len(hit)


def test_generated_replan_prompt_carries_pinned_lines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The string production sends to the foreman session must carry the
    real-cause lines for the 53C inputs and be deterministic."""
    prompt = _exec_replan_prompt(
        tmp_path, monkeypatch, _r53c_manifest_r1(), _r53c_inputs()[1]
    )
    for pid in PIDS:
        assert (
            f"the round-1 branch for process `{pid}` was never pushed "
            "(the F-1 check rejected the session before its branch push)"
        ) in prompt, pid
    assert (
        "no branch — the worker session was rejected before its branch push"
    ) in prompt
    # determinism: same inputs -> byte-identical prompt artifact
    again = _exec_replan_prompt(
        tmp_path, monkeypatch, _r53c_manifest_r1(), _r53c_inputs()[1]
    )
    assert again == prompt


def test_precheck_branch_absence_contract_lock():
    """Drift lock: the workflow's precheck must keep deriving the blocked list
    from branch presence (branch_present / merged), so the prompt's factual
    cause and the verdict's missing list stay one contract."""
    yml = _team_yml()
    assert 'info["branch_present"]' in yml
    assert 'info["merged"]' in yml
    assert 'info.get("out_of_bounds")' in yml


# ---------------------------------------------------------------------------
# VAL-M4-005: skipped_no_judgeable accounting semantics
# ---------------------------------------------------------------------------


def test_adopt_session_skipped_when_no_judgeable_droid_step_skipped(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    manifest, _ = _r53c_inputs()
    judgeable, blocked = _blocked_from_manifest(manifest)
    assert judgeable == []
    wall_path, work = _r53c_work(tmp_path, monkeypatch, judgeable=judgeable, blocked=blocked)
    # round-53 C reality: the judging step's if skipped the droid session
    # (no droid-exit.txt ever), but verdict.json existed from the merge
    # step, so merge_step_ran was recorded true.
    rc = adopt(work, wall_path, droid_exit=None, merge_step_ran=True, round_num=2)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    outcome = merged["budgets"]["session_outcome"]
    assert outcome["role"] == "validator2"
    assert outcome["completion_status"] == "skipped_no_judgeable"
    assert outcome["exit_code"] is None
    validate_with_jsonschema(merged)
    _, conclusion = derive(merged)
    assert conclusion == "failure", "a no-judgeable round must stay red downstream"


def test_adopt_session_skipped_records_null_exit_not_sentinel_minus_one():
    # The low-level mapper keeps its expected-but-absent semantics; the skip
    # decision is adopt()'s, keyed on the empty judgeable set (see adopt().
    assert adopt_session_completion_status(None) == "missing_output"
    assert adopt_session_completion_status(124) == "timeout"
    assert adopt_session_completion_status(0) == "ok"
    assert adopt_session_completion_status(2) == "droid_failed"


def test_replay_run_c_r2_accounting_semantics(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Full 53C replay: fixtures -> precheck -> adopt2 -> wall; the new
    semantics must sit beside the old artifact shape (blocked verdict,
    red round) so this is an in-place re-accounting, not a re-judging."""
    manifest, _ = _r53c_inputs()
    judgeable, blocked = _blocked_from_manifest(manifest)
    wall_path, work = _r53c_work(tmp_path, monkeypatch, judgeable=judgeable, blocked=blocked)
    rc = adopt(work, wall_path, droid_exit=None, merge_step_ran=True, round_num=2)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    outcome = merged["budgets"]["session_outcome"]
    assert outcome["completion_status"] == "skipped_no_judgeable"
    # old artifact: {"role": "validator2", "completion_status":
    # "missing_output", "exit_code": -1} (round-53 C wall) — both fields
    # change under the new semantics, nothing else in the slice moves.
    assert merged["validation"]["adoption_status"] == "ok"
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert verdict["adoption_status"] == "ok"
    assert [p["id"] for p in verdict["processes"]] == PIDS
    assert all(p["verdict"] == "blocked" for p in verdict["processes"])
    for p in verdict["processes"]:
        assert p["reason"].startswith("料不齐：缺 handoff, status, diff, 未合并/未替换")
    validate_with_jsonschema(merged)
    _, conclusion = derive(merged)
    assert conclusion == "failure"


def test_adopt_not_started_still_missing_output_when_session_was_expected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """No over-reach: a missing session that SHOULD have run (judgeable
    processes exist, merge step never produced a draft) keeps the
    missing_output semantics."""
    judgeable = ["somepid"]
    wall_path, work = _r53c_work(tmp_path, monkeypatch, judgeable=judgeable)
    rc = adopt(work, wall_path, droid_exit=None, merge_step_ran=False, round_num=2)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    outcome = merged["budgets"]["session_outcome"]
    assert outcome["completion_status"] == "missing_output"
    assert outcome["exit_code"] == -1
    assert merged["validation"]["adoption_status"] == "failed"
    assert merged["validation"]["adoption_error"] == "merge_skipped"
    validate_with_jsonschema(merged)


def test_adopt_recorded_exit_keeps_exit_semantics_on_empty_judgeable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Feature wording: the skip semantics are keyed on the droid step being
    skipped (no droid-exit.txt). A recorded exit on judgeable==[] keeps its
    own meaning (timeout is a timeout, whatever the judgeable set was)."""
    manifest, _ = _r53c_inputs()
    judgeable, blocked = _blocked_from_manifest(manifest)
    wall_path, work = _r53c_work(tmp_path, monkeypatch, judgeable=judgeable, blocked=blocked)
    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=2)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    outcome = merged["budgets"]["session_outcome"]
    assert outcome["completion_status"] == "timeout"
    assert outcome["exit_code"] == 124
    validate_with_jsonschema(merged)


def test_adopt_missing_manifest_still_writes_session_outcome(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Robustness: no manifest/plan at all -> the accounting tail must still
    patch the wall (the try block raising early binds judgeable=[] first)."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="r53c-x", issue_number=792), wall_path)
    work = tmp_path / "work"
    work.mkdir()
    rc = adopt(work, wall_path, droid_exit=None, merge_step_ran=False, round_num=2)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    outcome = merged["budgets"]["session_outcome"]
    # work/judgeable.json absent -> judgeable==[] -> skip semantics on the
    # ok path; adoption failed on missing manifest but the outcome is still
    # recorded with the real (missing) exit semantics.
    assert outcome["completion_status"] in ("missing_output", "skipped_no_judgeable")
    validate_with_jsonschema(merged)


def test_session_outcome_schema_enumerates_skipped_no_judgeable():
    schema = json.loads(
        (ROOT / "schemas" / "foreman-run.v1.schema.json").read_text(encoding="utf-8")
    )
    outcome_schema = schema["$defs"]["budget_slice"]["properties"]["session_outcome"][
        "properties"
    ]
    assert "skipped_no_judgeable" in outcome_schema["completion_status"]["enum"]
    assert "missing_output" in outcome_schema["completion_status"]["enum"]
    # a skipped session has no real exit code: null, never the -1 sentinel
    assert outcome_schema["exit_code"]["type"] == ["integer", "null"]


def test_round1_no_judgeable_records_validator_role(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Run-C round 1 had the same shape (all packs blocked -> judgeable==[]):
    the skip semantics apply to the round-1 validator role too."""
    manifest, _ = _r53c_inputs()
    judgeable, blocked = _blocked_from_manifest(manifest)
    wall_path, work = _r53c_work(tmp_path, monkeypatch, judgeable=judgeable, blocked=blocked)
    rc = adopt(work, wall_path, droid_exit=None, merge_step_ran=True, round_num=1)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    outcome = merged["budgets"]["session_outcome"]
    assert outcome["role"] == "validator"
    assert outcome["completion_status"] == "skipped_no_judgeable"
    assert outcome["exit_code"] is None
    validate_with_jsonschema(merged)


def test_replay_run_c_real_wall_new_semantics(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """VAL-M4-005 replay against the real run-C final wall (verbatim fixture):
    the old artifact carried completion_status=missing_output / exit_code=-1 /
    plan_output_shape=complete; re-running the same adopt inputs on that wall
    must leave the new semantics in place, everything else untouched."""
    wall_fixture = ROOT / "tests" / "fixtures" / "foreman_wall_r53c" / "foreman-run.json"
    old = json.loads(wall_fixture.read_text(encoding="utf-8"))
    assert old["budgets"]["session_outcome"]["completion_status"] == "missing_output"
    assert old["budgets"]["session_outcome"]["exit_code"] == -1

    manifest, plan = _r53c_inputs()
    judgeable, blocked = _blocked_from_manifest(manifest)
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    (work / "judgeable.json").write_text(json.dumps(judgeable), encoding="utf-8")
    (work / "blocked.json").write_text(json.dumps(blocked), encoding="utf-8")
    wall_path = tmp_path / "foreman-run.json"
    shutil.copyfile(wall_fixture, wall_path)

    rc = adopt(work, wall_path, droid_exit=None, merge_step_ran=True, round_num=2)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    outcome = merged["budgets"]["session_outcome"]
    assert outcome["role"] == "validator2"
    assert outcome["completion_status"] == "skipped_no_judgeable"
    assert outcome["exit_code"] is None
    # untouched neighbors: the old wall's session_outcome extras and the
    # validation slice keep their values (deep_merge, not a rewrite)
    assert outcome["plan_output_shape"] == "complete"
    assert merged["validation"]["adoption_status"] == "ok"
    assert merged["artifacts"]["team-verdict2-issue-792-run-45125143118"]["complete"] is True
    validate_with_jsonschema(merged)
    _, conclusion = derive(merged)
    assert conclusion == "failure"


def test_new_accounting_holds_without_jsonschema(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Round-53 lucas context: a bare venv without jsonschema must reach the
    same wall state (the fallback validator accepts the new value)."""
    import subprocess

    probe = tmp_path / "probe.py"
    probe.write_text(
        "import sys\n"
        "sys.modules['jsonschema'] = None\n"  # mirror validate_with_jsonschema's ImportError path
        "import json\n"
        "sys.path.insert(0, r'%s')\n"
        "from adopt_verdict import adopt\n"
        "from pathlib import Path\n"
        "rc = adopt(Path('work'), Path('foreman-run.json'), droid_exit=None,"
        " merge_step_ran=True, round_num=2)\n"
        "w = json.load(open('foreman-run.json'))\n"
        "print(rc, w['budgets']['session_outcome']['completion_status'])\n"
        % (ROOT / "scripts" / "team")
    )
    manifest, plan = _r53c_inputs()
    judgeable, blocked = _blocked_from_manifest(manifest)
    monkeypatch.chdir(tmp_path)
    save_wall(init_wall(run_id="r53c-ns", issue_number=792), tmp_path / "foreman-run.json")
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
    (work / "judgeable.json").write_text(json.dumps(judgeable), encoding="utf-8")
    (work / "blocked.json").write_text(json.dumps(blocked), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(probe)], cwd=tmp_path, capture_output=True, text=True, timeout=30
    )
    assert proc.returncode == 0, proc.stderr
    tail = proc.stdout.strip().splitlines()[-1].strip()
    assert tail == "0 skipped_no_judgeable", proc.stdout
