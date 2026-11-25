"""Whole-chain execution check (scrutiny suggestedGuidanceUpdates): the real
CLI entry points, driven on the output each step actually produces, for the
exact m1-scrutiny-fixes faces:

  chain A — first timeout: adopt(124) -> compute_replan_gate ->
            compute_validate_conclusion (CLI) must leave human_stop OFF and
            the revalidate request ON through every step;
  chain B — torn draft + sealed partial: same CLI chain must adopt ok and
            derive success;
  chain C — after the revalidate job stamps its start marker and the retry
            dies again: every step must terminate human_stop (fail-closed);
  chain D/E — scrutiny R2-1/R2-3: the replan job's `if:` decides on the
            --github-output strings the real jobs emit. A retry that
            legitimately judges FAIL (revalidate=success, its gate says
            should_replan=true) must reach replan exactly like the same FAIL
            verdict without a timeout (revalidate=skipped, validate gate says
            should_replan=true); a failed retry must stay terminal.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402
from salvage_verdict import salvage_verdict  # noqa: E402
from test_revalidate_workflow_contract import _replan_condition  # noqa: E402

PIDS = ["damm", "easterorthodox", "graph"]
ENV = {**__import__("os").environ, "PYTHONPATH": str(ROOT / "scripts" / "team"),
       "FOREMAN_RUN_PATCH": "1"}


def _work(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text(json.dumps({"pytest_exit": 0}), encoding="utf-8")
    (work / "plan.json").write_text(
        json.dumps({"processes": [{"id": pid} for pid in PIDS]}), encoding="utf-8"
    )
    (work / "judgeable.json").write_text(json.dumps(PIDS), encoding="utf-8")
    (work / "blocked.json").write_text("{}", encoding="utf-8")
    return work


def _cli(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args], capture_output=True, text=True, timeout=60, env=ENV,
        cwd=str(cwd),
    )


def _wall(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_chain(tmp_path: Path, run_id: str, *, stamp_started: bool, torn: bool):
    """Drive adopt -> gate -> derive through the real CLI main() entry points."""
    monkey = pytest.MonkeyPatch()
    monkey.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id=run_id, issue_number=812), wall_path)
    work = _work(tmp_path)
    if torn:
        salvage = salvage_verdict(
            work,
            analyzed={pid: {"verdict": "pass", "reason": "aligned"} for pid in PIDS},
            round_num=1,
        )
        salvage["final"] = True
        (work / "verdict-partial.json").write_text(json.dumps(salvage), encoding="utf-8")
        (work / "verdict-droid.json").write_bytes(b"not json at all")
    if stamp_started:
        wall = _wall(wall_path)
        wall.setdefault("replan_gate", {})["revalidate_run_started"] = True
        save_wall(wall, wall_path)

    r1 = _cli(
        str(ROOT / "scripts/team/adopt_verdict.py"), "--wall", str(wall_path),
        "--work-dir", str(work), "--droid-exit", "124", cwd=tmp_path,
    )
    assert r1.returncode == 0, r1.stderr
    r2 = _cli(str(ROOT / "scripts/team/compute_replan_gate.py"), "--wall", str(wall_path), cwd=tmp_path)
    assert r2.returncode == 0, r2.stderr
    r3 = _cli(
        str(ROOT / "scripts/team/compute_validate_conclusion.py"), "--wall", str(wall_path),
        cwd=tmp_path,
    )
    return _wall(wall_path), r3


def test_cli_chain_first_timeout_keeps_revalidate_pending(tmp_path: Path):
    wall, _ = _run_chain(tmp_path / "a" if False else tmp_path, "cli-a", stamp_started=False, torn=False)
    gate = wall["replan_gate"]
    assert gate["should_revalidate"] is True
    assert not gate.get("revalidate_run_started")
    assert wall.get("human_stop") is not True
    assert "closeout" not in wall
    validate_with_jsonschema(wall)


def test_cli_chain_torn_draft_adopts_ok(tmp_path: Path):
    wall, r3 = _run_chain(tmp_path, "cli-b", stamp_started=False, torn=True)
    assert wall["validation"]["adoption_status"] == "ok"
    assert wall["validation"]["overall"] == "pass"
    assert wall["validation"]["job_conclusion_derived"] == "success"
    assert wall.get("human_stop") is not True
    assert r3.returncode == 0, r3.stdout + r3.stderr
    validate_with_jsonschema(wall)


def test_cli_chain_second_timeout_terminates_fail_closed(tmp_path: Path):
    wall, _ = _run_chain(tmp_path, "cli-c", stamp_started=True, torn=False)
    assert wall.get("human_stop") is True
    assert wall["closeout"]["run_must_fail"] is True
    assert wall["replan_gate"]["should_revalidate"] is False
    validate_with_jsonschema(wall)


# --- scrutiny R2-1/R2-3: the replan `if:` decides on real job outputs ------


def _draft_for(work: Path, verdict: str) -> None:
    v = "pass" if verdict == "pass" else "fail"
    draft = {"processes": [{"id": pid, "verdict": v, "reason": "evidence line up"} for pid in PIDS],
             "conflicts": []}
    (work / "verdict-droid.json").write_text(json.dumps(draft), encoding="utf-8")
    (work / "verdict-droid.md").write_text("# report\n", encoding="utf-8")


def _adopt_gate_derive(run_dir: Path, wall_path: Path, work: Path, *,
                       droid_exit: int, merge_step_ran: bool) -> dict[str, str]:
    """The validate/revalidate jobs' terminal steps verbatim: adopt (the
    run_adopt_step wrapper is GNU-timeout only; the library call is the same
    machinery), then gate and conclusion with --github-output. Returns the
    job outputs the `if:` conditions read."""
    gh_out = run_dir / "outputs.env"
    r = _cli(str(ROOT / "scripts/team/adopt_verdict.py"), "--wall", str(wall_path),
             "--work-dir", str(work), "--droid-exit", str(droid_exit),
             *(["--merge-step-ran"] if merge_step_ran else []), cwd=run_dir)
    assert r.returncode == 0, (droid_exit, r.stdout, r.stderr)
    r = _cli(str(ROOT / "scripts/team/compute_replan_gate.py"), "--wall", str(wall_path),
             "--github-output", str(gh_out), cwd=run_dir)
    assert r.returncode == 0, r.stderr
    r = _cli(str(ROOT / "scripts/team/compute_validate_conclusion.py"), "--wall", str(wall_path),
             "--github-output", str(gh_out), cwd=run_dir)
    assert r.returncode in (0, 1), r.stderr
    return _parse_outputs(gh_out)


def _run_validate_job(run_dir: Path, *, droid_exit: int, verdict: str | None) -> dict[str, str]:
    """First validation round: session outcome = droid_exit; a non-None verdict
    means the session finished and the inline merge step ran (draft on disk)."""
    run_dir.mkdir(parents=True)
    wall_path = run_dir / "foreman-run.json"
    save_wall(init_wall(run_id=run_dir.name, issue_number=812), wall_path)
    work = _work(run_dir)
    if verdict is not None:
        _draft_for(work, verdict)
    return _adopt_gate_derive(run_dir, wall_path, work,
                              droid_exit=droid_exit, merge_step_ran=verdict is not None)


def _run_revalidate_job(run_dir: Path, *, verdict: str | None) -> dict[str, str]:
    """The revalidate job: its guard stamps the start marker BEFORE the retry
    session runs; the retry either finishes with a verdict (adopted through
    the draft) or dies at the wall again."""
    run_dir.mkdir(parents=True)
    wall_path = run_dir / "foreman-run.json"
    wall = init_wall(run_id=run_dir.name, issue_number=812)
    wall.setdefault("replan_gate", {})["revalidate_run_started"] = True
    save_wall(wall, wall_path)
    work = _work(run_dir)
    if verdict is not None:
        _draft_for(work, verdict)
        return _adopt_gate_derive(run_dir, wall_path, work,
                                  droid_exit=0, merge_step_ran=True)
    return _adopt_gate_derive(run_dir, wall_path, work,
                              droid_exit=124, merge_step_ran=False)


def _parse_outputs(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out[k] = v
    return out


def _eval_replan_condition(cond: str, *, validate_result: str, validate_out: dict,
                           revalidate_result: str, revalidate_out: dict) -> bool:
    """Evaluate the job-level condition on the exact strings GitHub would
    supply: needs.<job>.result and needs.<job>.outputs.<name>."""
    env = {
        "needs.validate.result": validate_result,
        "needs.validate.outputs.should_replan": validate_out.get("should_replan", ""),
        "needs.revalidate.result": revalidate_result,
        "needs.revalidate.outputs.should_replan": revalidate_out.get("should_replan", ""),
    }
    expr = cond
    for k, v in env.items():
        expr = expr.replace(f"{k} ", f"'{v}' ")
    expr = expr.replace("&&", " and ").replace("||", " or")
    expr = expr.replace("!cancelled()", "True")
    return bool(eval(expr, {"__builtins__": {}}, {}))  # noqa: S307 (fixed-shape test expression)


def test_replan_routing_revalidate_success_fail_verdict_reaches_replan(tmp_path: Path):
    """R2-1, end to end on the real chain: first validator timeout -> the
    retry legitimately judges graph=fail (the r54A scenario) -> the revalidate
    job's own gate must route replan exactly like the same FAIL verdict
    without a timeout. The old validate-only condition reads false here
    (validate's gate ran while its adoption was still failed)."""
    v1_out = _run_validate_job(tmp_path / "ex-r1", droid_exit=124, verdict=None)
    assert v1_out["should_revalidate"] == "true"
    assert v1_out["should_replan"] == "false"
    assert v1_out["validate_job_conclusion"] == "failure"

    r_out = _run_revalidate_job(tmp_path / "ex-r2", verdict="fail")
    assert r_out["should_replan"] == "true", r_out
    assert r_out["validate_job_conclusion"] == "success"

    cond = _replan_condition((ROOT / ".github/workflows/team.yml").read_text(encoding="utf-8"))
    assert _eval_replan_condition(
        cond, validate_result="failure", validate_out=v1_out,
        revalidate_result="success", revalidate_out=r_out,
    ), "retry that judges FAIL must reach replan (VAL-P1-003 routing)"


def test_replan_routing_normal_chain_unchanged_when_retry_skipped(tmp_path: Path):
    """R2-3: a run whose first validator does not time out (same FAIL verdict)
    keeps replan routed through the validate job's gate — the skipped-retry
    arm must not lose it."""
    v1_out = _run_validate_job(tmp_path / "ex-s1", droid_exit=0, verdict="fail")
    assert v1_out["should_replan"] == "true"
    assert v1_out["validate_job_conclusion"] == "success"

    cond = _replan_condition((ROOT / ".github/workflows/team.yml").read_text(encoding="utf-8"))
    assert _eval_replan_condition(
        cond, validate_result="success", validate_out=v1_out,
        revalidate_result="skipped", revalidate_out={},
    ), "normal (no-timeout) FAIL chain must still reach replan"


def test_replan_routing_failed_retry_stays_terminal(tmp_path: Path):
    """Fail-closed: the retry dies at the wall again (second timeout) -> the
    revalidate job's gate keeps should_replan=false, human_stop landed, and
    replan must NOT run."""
    _run_validate_job(tmp_path / "ex-f1", droid_exit=124, verdict=None)
    r_out = _run_revalidate_job(tmp_path / "ex-f2", verdict=None)
    assert r_out["should_replan"] == "false"
    wall = _wall(tmp_path / "ex-f2" / "foreman-run.json")
    assert wall.get("human_stop") is True

    cond = _replan_condition((ROOT / ".github/workflows/team.yml").read_text(encoding="utf-8"))
    v1_out = {"should_replan": "false"}
    assert not _eval_replan_condition(
        cond, validate_result="failure", validate_out=v1_out,
        revalidate_result="failure", revalidate_out=r_out,
    ), "a failed retry must stay terminal (human_stop already landed)"
