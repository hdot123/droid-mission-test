"""Torn-draft scenario (scrutiny PR2-1, VAL-CROSS-003): a session killed
mid-write leaves an unparseable or truncated verdict-droid.json beside a
sealed full partial. The exact shape the wall produces most often — the kill
window covers the draft write itself.

Pinned contract: on exit 124 a draft that cannot PROVE its own completeness
(unparseable / truncated / empty) never falls into droid_step_failed or
human_stop. The I-6 assembler gets its chance on the sealed partial; when
that cannot cover the judgeable set either, the round lands the revalidate
chain (draft_timeout), exactly like the no-draft case.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from adopt_verdict import adopt  # noqa: E402
from compute_validate_conclusion import derive  # noqa: E402
from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402
from salvage_verdict import salvage_verdict  # noqa: E402


def _sealed_full_partial(work: Path, pids: list[str]) -> None:
    salvage = salvage_verdict(
        work,
        analyzed={pid: {"verdict": "pass", "reason": "five artifacts line up"} for pid in pids},
        round_num=1,
    )
    salvage["final"] = True
    (work / "verdict-partial.json").write_text(
        json.dumps(salvage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _work_dir(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    work.mkdir()
    (work / "manifest.json").write_text(json.dumps({"pytest_exit": 0}), encoding="utf-8")
    (work / "plan.json").write_text(
        json.dumps({"processes": [{"id": pid} for pid in PIDS]}), encoding="utf-8"
    )
    (work / "judgeable.json").write_text(json.dumps(PIDS), encoding="utf-8")
    (work / "blocked.json").write_text("{}", encoding="utf-8")
    return work


PIDS = ["dijkstra", "nthprime", "windscale"]


@pytest.mark.parametrize(
    "draft_bytes",
    [
        pytest.param(b"", id="zero-byte"),
        pytest.param(
            b'{"processes": [{"id": "dijkstra", "verdict": "pass", "reason": "art',
            id="truncated-mid-entry",
        ),
        pytest.param(b'{"processes": [', id="truncated-array"),
        pytest.param(b"not json at all", id="non-json"),
    ],
)
def test_torn_draft_with_sealed_partial_adopts_ok(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, draft_bytes: bytes
):
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id=f"torn-{len(draft_bytes)}", issue_number=812), wall_path)
    work = _work_dir(tmp_path)
    _sealed_full_partial(work, PIDS)
    (work / "verdict-droid.json").write_bytes(draft_bytes)

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_status"] == "ok", (
        f"torn draft must not veto the sealed partial, got "
        f"adoption_error={merged['validation'].get('adoption_error')}"
    )
    assert merged["validation"]["adoption_error"] is None
    assert merged.get("human_stop") is not True
    assert merged["validation"]["overall"] == "pass"
    verdict = json.loads(Path("verdict.json").read_text(encoding="utf-8"))
    assert verdict["salvage_assembled"] is True
    validate_with_jsonschema(merged)


def test_torn_draft_without_usable_partial_goes_revalidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Torn draft AND no sealed full partial: the revalidate chain, never
    droid_step_failed / human_stop."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="torn-reval", issue_number=812), wall_path)
    work = _work_dir(tmp_path)
    (work / "verdict-droid.json").write_bytes(b'{"processes": [{"id": "dijk')

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_error"] == "draft_timeout"
    assert merged.get("human_stop") is not True
    assert merged["replan_gate"]["should_revalidate"] is True
    validate_with_jsonschema(merged)


def test_torn_draft_partial_under_coverage_goes_revalidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Torn draft + sealed partial covering only part of judgeable: the
    revalidate chain (no guessing adoption from an under-covered partial)."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="torn-under", issue_number=812), wall_path)
    work = _work_dir(tmp_path)
    salvage = salvage_verdict(
        work,
        analyzed={PIDS[0]: {"verdict": "pass", "reason": "aligned"}},
        round_num=1,
    )
    salvage["final"] = True
    (work / "verdict-partial.json").write_text(json.dumps(salvage), encoding="utf-8")
    (work / "verdict-droid.json").write_bytes(b"")

    rc = adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    assert rc == 0
    merged = json.loads(wall_path.read_text(encoding="utf-8"))
    assert merged["validation"]["adoption_error"] == "draft_timeout"
    assert merged.get("human_stop") is not True
    assert merged["replan_gate"]["should_revalidate"] is True
    validate_with_jsonschema(merged)


def test_whole_chain_torn_draft_derives_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """End of the chain check: after adopt() adopts the torn-draft + sealed
    partial shape, derive() must keep human_stop off (the wall the validate
    job uploads carries no termination)."""
    monkeypatch.chdir(tmp_path)
    wall_path = tmp_path / "foreman-run.json"
    save_wall(init_wall(run_id="torn-derive", issue_number=812), wall_path)
    work = _work_dir(tmp_path)
    _sealed_full_partial(work, PIDS)
    (work / "verdict-droid.json").write_bytes(b"not json at all")

    adopt(work, wall_path, droid_exit=124, merge_step_ran=False, round_num=1)
    wall = json.loads(wall_path.read_text(encoding="utf-8"))
    merged, conclusion = derive(wall, round_num=1)
    assert conclusion == "success"
    assert merged.get("human_stop") is not True
    validate_with_jsonschema(merged)
