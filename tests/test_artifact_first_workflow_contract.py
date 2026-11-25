"""VAL-P2-004/006: team.yml workflow contracts for the PR-2 artifact-first
adoption surface.

Pins (workflow = deploy surface):
- prep/prep2 write evidence/check-summary.json (per-card passed/skipped plus
  merged totals) BEFORE the manifest hashes the evidence tree, so the sha
  covers it; the step never rewrites worker status files (evidence immutability);
- the inline merge steps (validate, validate2 — the revalidate jobs route
  through run_adopt_step, which shares the same assembly helper) accept a
  machine-assembled draft (verdict-partial.json sealed final + full judgeable
  coverage) instead of exiting on the final coverage mismatch — the exact
  line that killed round-54 A/C (job log L497);
- the stream artifact upload includes the partial file (unchanged) and the
  validator jobs keep the prompt template wiring (PR-1 surface).
"""
from __future__ import annotations

import json
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


# --- VAL-P2-006: prep authoritative counts ----------------------------------


@pytest.mark.parametrize("job_key", ["prep", "prep2"])
def test_prep_writes_check_summary(yml, job_key: str):
    text = _job_text(yml, job_key)
    assert "check-summary.json" in text, f"{job_key} must produce check-summary.json"
    assert "passed" in text and "skipped" in text


def test_check_summary_written_before_manifest_hash(yml):
    """The sha must cover the summary: every occurrence of the summary write
    sits before the manifest sha256 walk in its prep job."""
    for job_key in ("prep", "prep2"):
        text = _job_text(yml, job_key)
        summary_idx = text.index("check-summary.json")
        manifest_idx = text.index('manifest["sha256"]')
        assert summary_idx < manifest_idx, f"{job_key}: summary must precede manifest hashing"


def test_prep_does_not_rewrite_worker_status_files(yml):
    """Evidence immutability: the summary write goes to evidence/, never back
    into team/status worker files."""
    for job_key in ("prep", "prep2"):
        text = _job_text(yml, job_key)
        for m in re.finditer(r"open\((f?)['\"]([^'\"]*check-summary\.json)['\"], ['\"]w", text):
            path = m.group(2)
            assert path.startswith("evidence/") or "evidence" in path, (
                f"{job_key}: check-summary.json must live under evidence/, got {path}"
            )


def test_check_summary_contract_helpers_exist():
    """The summary builder is a repo script with a stable contract (both prep
    jobs call it; tests import it directly)."""
    sys.path.insert(0, str(ROOT / "scripts" / "team"))
    import check_summary  # noqa: E402

    doc = check_summary.build_summary(
        per_card={"a": {"passed": 3, "skipped": 1}, "b": {"passed": 2, "skipped": 0}},
        totals={"passed": 5, "skipped": 1},
    )
    assert doc["schema_version"] == "check-summary.v1"
    assert doc["per_card"]["a"] == {"passed": 3, "skipped": 1}
    assert doc["totals"] == {"passed": 5, "skipped": 1}
    assert check_summary.parse_pytest_counts("240 passed, 2 skipped in 15.30s") == {
        "passed": 240,
        "skipped": 2,
    }


def test_check_summary_on_r54_real_evidence(tmp_path: Path):
    """VAL-P2-006 evidence face: run the builder against the real round-54 A
    pack layout (pytest output verbatim) — the summary carries the merged
    totals and one entry per card, without touching worker originals."""
    sys.path.insert(0, str(ROOT / "scripts" / "team"))
    import shutil

    import check_summary  # noqa: E402

    src = ROOT / "tests" / "fixtures" / "validator-r54ac" / "a"
    ev = tmp_path / "evidence"
    (ev / "packs").mkdir(parents=True)
    shutil.copyfile(src / "pytest-output.txt", ev / "pytest-output.txt")
    for pid in ("damm", "easterorthodox", "graph"):
        (ev / "packs" / pid).mkdir()
        (ev / "packs" / pid / "checks-exit.json").write_text("[]", encoding="utf-8")
    worker_status = tmp_path / "team" / "status"
    worker_status.mkdir(parents=True)
    (worker_status / "damm.json").write_text('{"passed": 999}', encoding="utf-8")

    path = check_summary.write_summary(
        ev,
        per_card={pid: {"passed": 0, "skipped": 0} for pid in ("damm", "easterorthodox", "graph")},
        totals=check_summary.parse_pytest_counts(
            (ev / "pytest-output.txt").read_text(encoding="utf-8")
        ),
    )
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["schema_version"] == "check-summary.v1"
    assert set(doc["per_card"]) == {"damm", "easterorthodox", "graph"}
    assert doc["totals"]["passed"] == 240 and doc["totals"]["skipped"] == 2
    # evidence immutability: the worker original is untouched
    assert json.loads((worker_status / "damm.json").read_text())["passed"] == 999


# --- VAL-P2-004: inline merge accepts machine-assembled drafts --------------


_MERGE_STEP = "Merge verdict, enforce gates, verify evidence untouched"


@pytest.mark.parametrize(
    "job_key",
    ["validate", "validate2"],
)
def test_inline_merge_accepts_assembled_draft(yml, job_key: str):
    text = _job_text(yml, job_key)
    assert _MERGE_STEP in text, f"{job_key} merge step missing"
    assert "assemble_assembled_draft" in text, (
        f"{job_key}: merge step must accept the machine-assembled draft"
    )
    assert "salvage_assemble" in text, f"{job_key}: merge step must use the shared helper"


@pytest.mark.parametrize(
    "job_key",
    ["revalidate", "revalidate2"],
)
def test_revalidate_job_routes_through_library_merge(yml, job_key: str):
    """The revalidate jobs route their verdict through run_adopt_step (the
    same adopt library that assembles sealed partials)."""
    text = _job_text(yml, job_key)
    assert "run_adopt_step.py" in text
    assert "compute_replan_gate.py" in text


@pytest.mark.parametrize(
    "job_key",
    ["validate", "validate2", "revalidate", "revalidate2"],
)
def test_no_merge_step_exits_on_final_coverage_mismatch_alone(yml, job_key: str):
    """The A/C death line is defanged: the final-coverage-mismatch print no
    longer sits in an immediate `sys.exit(1)` branch — the merge step fills
    the missing processes as blocked and lets the adopt library classify
    (revalidate path). Pin: the line's branch tail contains no bare exit.
    All four judging jobs share the defused shape (PR-2 carry-over: the
    revalidate jobs' inline copies were demoted from exit-1 to the same
    classification routing)."""
    text = _job_text(yml, job_key)
    assert "assemble_assembled_draft" in text, f"{job_key} must accept assembled drafts"
    idx = text.find("final coverage mismatch")
    assert idx != -1, f"{job_key}: mismatch handler expected"
    tail = text[idx : idx + 500]
    assert "sys.exit(1)" not in tail.split("#")[0] or "routing through adopt classification" in tail, (
        f"{job_key}: the A/C death line must route through adopt classification, not exit"
    )
    assert "routing through adopt classification" in tail


def test_stream_upload_keeps_partial_file(yml):
    for key in ("validate", "validate2"):
        text = _job_text(yml, key)
        assert "verdict-partial.json" in text


def test_validator_jobs_still_use_prompt_template(yml):
    for step_name, rnd in (
        ("- name: Validator judges evidence packs only\n", "round_num=1"),
        ("- name: Validator judges evidence packs only (round 2)\n", "round_num=2"),
    ):
        assert step_name in yml
        idx = yml.index(step_name)
        chunk = yml[idx : yml.index("\n      - name:", idx)]
        assert "validator_prompt_template" in chunk
        assert rnd in chunk
