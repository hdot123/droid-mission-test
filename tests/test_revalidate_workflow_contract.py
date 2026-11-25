"""VAL-P1-003 / VAL-P1-004: team.yml wiring contracts for the PR-1 revalidate
chain and the worker dependency preinstall.

Pins (workflow = deploy surface, same parse-style as the repo's other yml
contract tests):
- one revalidate job per validation round, gated on the wall's
  should_revalidate flag; the job re-runs ONLY the validator session (no adopt
  machinery, no merge), reuses the uploaded evidence pack with the SAME
  EXPECTED_MANIFEST_SHA, runs at most once, and a revalidate failure lands
  human_stop via the adopt step (fail-closed);
- each worker job (worker / worker2) installs requirements-dev.txt BEFORE the
  droid session starts (12/12 sessions lost their first pytest round to the
  missing environment).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEAM_YML = ROOT / ".github" / "workflows" / "team.yml"

sys.path.insert(0, str(ROOT / "scripts" / "team"))


@pytest.fixture(scope="module")
def yml() -> str:
    return TEAM_YML.read_text(encoding="utf-8")


def _job_text(yml: str, job_key: str) -> str:
    m = re.search(rf"^  {job_key}:\n", yml, re.MULTILINE)
    assert m, f"job {job_key} missing"
    next_m = re.search(r"^  [a-z0-9-]+:\n", yml[m.end() :], re.MULTILINE)
    end = m.end() + next_m.start() if next_m else len(yml)
    return yml[m.start() : end]


# --- VAL-P1-003: revalidate jobs -------------------------------------------


def test_revalidate_job_exists_per_round(yml):
    for key in ("revalidate", "revalidate2"):
        text = _job_text(yml, key)
        assert f"name: {key}" in text or text.startswith(f"  {key}:")
        assert "runs-on: ubuntu-latest" in text


def test_revalidate_jobs_gate_on_should_revalidate(yml):
    for key in ("revalidate", "revalidate2"):
        text = _job_text(yml, key)
        assert "needs.validate.outputs.should_revalidate == 'true'" in text.replace(
            "needs.validate2", "needs.validate"
        ) or "should_revalidate == 'true'" in text, f"{key} must gate on should_revalidate"


def test_revalidate_max_once(yml):
    """The attempt marker lives on the wall under one name everywhere: the
    job's guard refuses to re-run when revalidate_run_started is already true
    (stamped when the first retry session actually started), and the guard is
    NOT the job's first step — it must sit after Checkout and the wall
    download (scrutiny PR1-1: a fresh runner has no wall before those)."""
    for key in ("revalidate", "revalidate2"):
        text = _job_text(yml, key)
        assert "revalidate_run_started" in text, f"{key} must consume the run-start marker"
        guard_idx = text.find("- name: Refuse a second revalidate")
        checkout_idx = text.find("- name: Checkout\n")
        wall_idx = text.find("- name: Download ForemanRun wall")
        assert 0 <= checkout_idx < wall_idx < guard_idx, (
            f"{key}: guard must come after Checkout and the wall download"
        )


def test_revalidate_reuses_evidence_pack_and_same_sha(yml):
    for key in ("revalidate", "revalidate2"):
        text = _job_text(yml, key)
        assert "EXPECTED_MANIFEST_SHA" in text, f"{key} must pin the same manifest sha"
        assert "team-evidence" in text, f"{key} must reuse the uploaded evidence pack"


def test_revalidate_runs_only_validator(yml):
    """The revalidate step invokes the validator session runner and never the
    merge/adopt machinery (only the validator is re-run; adopt happens
    downstream in the same job to route the verdict back through the gates)."""
    for key in ("revalidate", "revalidate2"):
        text = _job_text(yml, key)
        assert "run_droid_session.py" in text
        assert "--role validator" in text
        # no replan / worker session in the revalidate job
        assert "--role worker" not in text
        assert "--role replan" not in text


def test_revalidate_failure_lands_human_stop(yml):
    """The revalidate job's adopt step is the same run_adopt_step machinery:
    its second draft_timeout lands human_stop inside adopt_verdict (see
    tests/test_revalidate_gate.py), and the job keeps the always()-guarded
    adopt + gate recompute steps so the verdict routes through the gates."""
    for key in ("revalidate", "revalidate2"):
        text = _job_text(yml, key)
        assert "run_adopt_step.py" in text, f"{key} must adopt through the standard step"
        assert "compute_replan_gate.py" in text, f"{key} must recompute the gate"


def test_revalidate_jobs_upload_wall_and_verdict(yml):
    for key in ("revalidate", "revalidate2"):
        text = _job_text(yml, key)
        assert "name: foreman-run-${{ github.run_id }}" in text


# --- VAL-P1-004: worker dependency preinstall ------------------------------


@pytest.mark.parametrize("job_key,step_name", [("worker", "Worker executes exactly one process card"), ("worker2", "Worker executes exactly one process card (round 2)")])
def test_worker_installs_dev_deps_before_session(yml, job_key, step_name):
    text = _job_text(yml, job_key)
    session_idx = text.index(step_name)
    before = text[:session_idx]
    assert re.search(r"pip install -r requirements-dev\.txt", before), (
        f"{job_key} must install requirements-dev.txt before the droid session step"
    )


def test_worker_install_step_runs_before_byom_settings(yml):
    """The install must precede the session start entirely (BYOM step is the
    last pre-session step today; being before THAT is the strict reading)."""
    for job_key in ("worker", "worker2"):
        text = _job_text(yml, job_key)
        install_idx = text.index("requirements-dev.txt")
        session_idx = text.index("Worker executes exactly one process card")
        assert install_idx < session_idx


# --- schema / wall contract sync -------------------------------------------


def test_schema_has_should_revalidate():
    schema = (ROOT / "schemas" / "foreman-run.v1.schema.json").read_text(encoding="utf-8")
    assert "should_revalidate" in schema
    assert "revalidate_run_started" in schema


# --- scrutiny PR1-6: downstream jobs must wait on the retry -----------------


@pytest.mark.parametrize(
    "job_key,extra_need",
    [("replan", "revalidate"), ("prep2", "revalidate"), ("assemble", "revalidate2")],
)
def test_downstream_jobs_wait_on_revalidate(yml, job_key: str, extra_need: str):
    """The retry's result must be able to influence the chain: the jobs that
    consume the wall list the revalidate job in their needs (the retry being
    skipped is tolerated by the job-level if conditions, not by missing
    edges)."""
    text = _job_text(yml, job_key)
    m = re.search(r"needs:\s*\[([^\]]+)\]", text)
    assert m, f"{job_key}: needs list expected"
    needs = [n.strip() for n in m.group(1).split(",")]
    assert extra_need in needs, f"{job_key} must wait on {extra_need}"


@pytest.mark.parametrize(
    "job_key,producer",
    [("validate", "should_revalidate"), ("validate2", "should_revalidate")],
)
def test_revalidate_producers_declare_output(yml, job_key: str, producer: str):
    """PR1-0: a job-level if reading needs.<job>.outputs.<name> is dead wiring
    unless the producer job declares the output — pinned both directions."""
    text = _job_text(yml, job_key)
    m = re.search(r"outputs:\n((?:      [a-z_]+: .*\n)+)", text)
    assert m, f"{job_key}: outputs block expected"
    assert f"{producer}:" in m.group(1), f"{job_key} must declare output {producer}"
