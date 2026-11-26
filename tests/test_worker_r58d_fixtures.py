"""worker-r58d fixtures: vendored round-58 D-run worker-seat death chain.

Two fixtures under ``tests/fixtures/worker-r58d/``:

- the fixture root vendors the verbatim round-58 hslconv wall-kill evidence
  (CI run 45812793849): the worker branch was merged and prep's machine
  re-run of both checks was green, yet ``handoff``/``status`` were never
  written because the 900s wall killed the worker session mid-checks-run
  (droid exit 124, last stream event "Tool execution was interrupted").
  This is the positive replay shape for the salvage guard and the replan
  death-context attribution.
- ``control-ok-missing/`` is the synthetic contrast shape: the session
  completed normally (``session_outcome=ok``, droid exit 0) while the pack
  is still missing ``handoff``/``status``. Fail-closed semantics must judge
  this a true compliance failure, never salvageable.

Fixtures are read-only replay data: no test writes into ``tests/fixtures/``.
Replay-style consumers must copy to a temporary directory before mutating.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "worker-r58d"
CONTROL_ROOT = FIXTURE_ROOT / "control-ok-missing"

STREAM_INTERRUPT_MARKER = "Error: Tool execution was interrupted"

# manifest sha256 keys that resolve to vendored bytes (verbatim evidence)
VENDORED_MANIFEST_KEYS = [
    "evidence/candidate-branch.txt",
    "evidence/check-summary.json",
    "evidence/plan.json",
    "evidence/packs/hslconv/checks-exit.json",
    "evidence/packs/hslconv/checks-output.txt",
    "evidence/packs/hslconv/diff.patch",
    "evidence/packs/hslconv/process-card.json",
    "evidence/pytest-exit.txt",
    "evidence/pytest-output.txt",
]

# manifest sha256 keys deliberately not vendored: the run's two sibling
# workers (radixsort / uuencode) whose packs were complete — out of this
# fixture's death-shape scope (the r53c "attested debt" pattern).
UNVENDORED_MANIFEST_KEYS = [
    "evidence/packs/radixsort/checks-exit.json",
    "evidence/packs/radixsort/checks-output.txt",
    "evidence/packs/radixsort/diff.patch",
    "evidence/packs/radixsort/handoff.md",
    "evidence/packs/radixsort/process-card.json",
    "evidence/packs/radixsort/status.json",
    "evidence/packs/uuencode/checks-exit.json",
    "evidence/packs/uuencode/checks-output.txt",
    "evidence/packs/uuencode/diff.patch",
    "evidence/packs/uuencode/handoff.md",
    "evidence/packs/uuencode/process-card.json",
    "evidence/packs/uuencode/status.json",
]

# files attested in the PROVENANCE sha256 vendor table (everything verbatim
# under the fixture root: the evidence tree plus the manifest, the CI-recorded
# legacy delta, and the full worker stream)
VERBATIM_FILES = sorted(
    [
        FIXTURE_ROOT / "manifest.json",
        FIXTURE_ROOT / "worker-delta.json",
        FIXTURE_ROOT / "worker-stream.jsonl",
        *(FIXTURE_ROOT / key for key in VENDORED_MANIFEST_KEYS),
    ]
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _parse_provenance_vendor_table() -> dict[str, str]:
    """Parse the ``<digest>  <path>`` table inside PROVENANCE.txt."""
    table: dict[str, str] = {}
    for line in (FIXTURE_ROOT / "PROVENANCE.txt").read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if len(stripped) > 65 and stripped[64:65].isspace() and stripped[:64].isalnum():
            digest, rel = stripped[:64], stripped[66:] if stripped[65:66].isspace() else stripped[65:]
            table[rel.strip()] = digest
    return table


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_r58d_fixture_tree_present():
    assert FIXTURE_ROOT.is_dir()
    for rel in [
        "PROVENANCE.txt",
        "manifest.json",
        "worker-delta.json",
        "worker-delta-wall-killed.json",
        "worker-stream.jsonl",
        *VENDORED_MANIFEST_KEYS,
    ]:
        assert (FIXTURE_ROOT / rel).is_file(), f"missing fixture member: {rel}"
    for rel in [
        "README.txt",
        "manifest.json",
        "worker-delta.json",
        "worker-stream-tail.jsonl",
        "evidence/packs/hslconv/checks-exit.json",
        "evidence/packs/hslconv/checks-output.txt",
    ]:
        assert (CONTROL_ROOT / rel).is_file(), f"missing control member: {rel}"


def test_r58d_provenance_vendor_table_covers_every_verbatim_file():
    table = _parse_provenance_vendor_table()
    expected = {p.relative_to(FIXTURE_ROOT).as_posix(): _sha256(p) for p in VERBATIM_FILES}
    assert table == expected, (
        "PROVENANCE vendor table must list exactly the verbatim files with "
        f"their real digests; drift: {set(table.items()) ^ set(expected.items())}"
    )


def test_r58d_manifest_sha256_attestations_match_vendored_bytes():
    manifest = _json(FIXTURE_ROOT / "manifest.json")
    assert sorted(manifest["sha256"]) == sorted(VENDORED_MANIFEST_KEYS + UNVENDORED_MANIFEST_KEYS)
    for key in VENDORED_MANIFEST_KEYS:
        entity = FIXTURE_ROOT / key
        assert entity.is_file(), f"attested key not vendored: {key}"
        assert _sha256(entity) == manifest["sha256"][key], f"digest drift at {key}"
    for key in UNVENDORED_MANIFEST_KEYS:
        assert not (FIXTURE_ROOT / key).exists(), f"unvendored key must stay absent: {key}"


def test_r58d_manifest_death_shape():
    manifest = _json(FIXTURE_ROOT / "manifest.json")
    assert manifest["issue"] == "929"
    assert manifest["run_id"] == "45812793849"
    assert manifest["iteration"] == 1
    assert manifest["pytest_exit"] == 0
    pack_meta = manifest["packs"]["hslconv"]
    assert pack_meta["branch_present"] is True
    assert pack_meta["merged"] is True
    assert pack_meta["merge_conflict"] is False
    assert pack_meta["out_of_bounds"] == []
    assert pack_meta["checks_failed_marker"] is False
    assert pack_meta["pack"] == {
        "process_card": True,
        "handoff": False,
        "status": False,
        "diff": True,
        "checks_output": True,
    }
    assert pack_meta["complete"] is False


def test_r58d_machine_checks_green_in_death_run():
    checks = _json(FIXTURE_ROOT / "evidence/packs/hslconv/checks-exit.json")
    assert [c["command"] for c in checks] == [
        "python3 -m pytest tests/test_hslconv.py -q",
        "python3 -m pytest tests/ -q",
    ]
    assert all(c["exit"] == 0 for c in checks)
    output = (FIXTURE_ROOT / "evidence/packs/hslconv/checks-output.txt").read_text(encoding="utf-8")
    assert "21 passed" in output
    assert "384 passed, 2 skipped" in output
    summary = _json(FIXTURE_ROOT / "evidence/check-summary.json")
    assert summary["totals"] == {"passed": 384, "skipped": 2}
    assert summary["per_card"]["hslconv"] == {"passed": 21, "skipped": 0}


def test_r58d_legacy_delta_records_no_death_fact():
    delta = _json(FIXTURE_ROOT / "worker-delta.json")
    # verbatim CI-recorded delta (job log line "delta: {...}"): the death
    # facts (exit 124 / interrupted tail) are absent — the defect under repair
    assert delta == {"pid": "hslconv", "result": "failure"}
    assert "session_outcome" not in delta
    assert "droid_exit_code" not in delta


def test_r58d_wall_killed_delta_shape():
    delta = _json(FIXTURE_ROOT / "worker-delta-wall-killed.json")
    assert delta["pid"] == "hslconv"
    assert delta["result"] == "failure"
    assert delta["session_outcome"] == "wall_killed"
    assert delta["droid_exit_code"] == 124
    assert delta["stream_tail_marker"] is True


def test_r58d_stream_tail_is_interrupted_without_completion():
    lines = (FIXTURE_ROOT / "worker-stream.jsonl").read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) for line in lines]
    assert len(events) == 52
    last = events[-1]
    assert last["type"] == "tool_result"
    assert last["isError"] is True
    assert last["error"]["message"] == STREAM_INTERRUPT_MARKER
    assert not any(e["type"] == "result" for e in events), "no completion event expected"


def test_r58d_provenance_declares_readonly_source_and_usage():
    provenance = (FIXTURE_ROOT / "PROVENANCE.txt").read_text(encoding="utf-8")
    lines = provenance.splitlines()
    # line-level guards: the source declaration must be the first line and
    # the run pin must be the Source line itself, so a contradictory
    # relabel anywhere else cannot satisfy the guard
    assert lines[0].startswith("worker-r58d fixture: round-58 D-run worker-seat death chain")
    assert any(line.startswith("Source: CI run 45812793849 ") for line in lines)
    assert "read-only" in provenance.lower()
    assert "test_worker_r58d_fixtures.py" in provenance
    # repo convention: no machine-local absolute paths in vendored fixtures
    assert "/Users/" not in provenance


def test_r58d_provenance_worker_delta_row_is_precise_about_rebuild():
    """The blanket verbatim claim must stay gone and the worker-delta.json
    disclosure must carry the byte-exact rebuild semantics: the file has
    no CI artifact counterpart, so verbatim over-claiming is a provenance
    defect (W-18)."""
    provenance = (FIXTURE_ROOT / "PROVENANCE.txt").read_text(encoding="utf-8")
    lines = provenance.splitlines()
    delta_bullet = next(
        (i for i, line in enumerate(lines) if line.startswith("- The CI-recorded worker delta")),
        None,
    )
    assert delta_bullet is not None, "the worker-delta disclosure bullet is gone"
    row = " ".join(lines[delta_bullet : delta_bullet + 2])
    assert "byte-exact rebuild" in row
    assert "CI delta artifact was not pulled" in row
    assert "verbatim" not in row
    assert "verbatim source for every file" not in provenance


def test_r58d_control_shape_is_self_consistent():
    manifest = _json(CONTROL_ROOT / "manifest.json")
    pack_meta = manifest["packs"]["hslconv"]
    # same merged-branch green-checks facts as the death run... the session
    # outcome facts ride on the delta (the F1 carrier), never the manifest —
    # the control manifest stays faithful to the prep manifest schema
    delta = _json(CONTROL_ROOT / "worker-delta.json")
    assert delta["session_outcome"] == "ok"
    assert delta["droid_exit_code"] == 0
    # ...but the pack is still missing the two evidence files
    assert pack_meta["pack"]["handoff"] is False
    assert pack_meta["pack"]["status"] is False
    assert pack_meta["complete"] is False
    assert not (CONTROL_ROOT / "evidence/packs/hslconv/handoff.md").exists()
    assert not (CONTROL_ROOT / "evidence/packs/hslconv/status.json").exists()
    # manifest claims match disk exactly
    checks = _json(CONTROL_ROOT / "evidence/packs/hslconv/checks-exit.json")
    assert all(c["exit"] == 0 for c in checks)
    assert (CONTROL_ROOT / "evidence/packs/hslconv/checks-output.txt").is_file()


def test_r58d_control_digests_attested_and_matching():
    manifest = _json(CONTROL_ROOT / "manifest.json")
    assert sorted(manifest["sha256"]) == [
        "evidence/packs/hslconv/checks-exit.json",
        "evidence/packs/hslconv/checks-output.txt",
        "worker-delta.json",
        "worker-stream-tail.jsonl",
    ]
    for key, digest in manifest["sha256"].items():
        entity = CONTROL_ROOT / key
        assert entity.is_file(), f"control key not vendored: {key}"
        assert _sha256(entity) == digest, f"digest drift at control {key}"


def test_r58d_control_delta_ok_outcome_with_failure_result():
    delta = _json(CONTROL_ROOT / "worker-delta.json")
    # session ok (droid exit 0) yet job failure: the verify step fails on the
    # missing handoff even without a wall kill — the guard must key on
    # session_outcome, never on the job result alone
    assert delta["session_outcome"] == "ok"
    assert delta["droid_exit_code"] == 0
    assert delta["stream_tail_marker"] is False
    assert delta["result"] == "failure"


def test_r58d_control_stream_tail_has_no_interrupt_marker():
    tail = (CONTROL_ROOT / "worker-stream-tail.jsonl").read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) for line in tail]
    assert events, "control stream tail must not be empty"
    assert not any(
        e.get("error", {}).get("message") == STREAM_INTERRUPT_MARKER for e in events
    )
    assert events[-1]["type"] != "tool_result" or events[-1].get("isError") is not True


def test_r58d_control_declared_synthetic_in_readme():
    readme_lines = (CONTROL_ROOT / "README.txt").read_text(encoding="utf-8").splitlines()
    # line-level guard: the SYNTHETIC label must be on the first line, so
    # a synthetic-vs-verbatim relabel buried deeper cannot sneak through
    assert readme_lines[0].startswith("control-ok-missing: SYNTHETIC contrast fixture")
    assert "synthetic" in "\n".join(readme_lines).lower()
    assert any("45812793849" in line for line in readme_lines)  # cross-references the run it contrasts with
    assert "/Users/" not in "\n".join(readme_lines)


def test_r58d_control_excluded_from_provenance_verbatim_scope():
    table = _parse_provenance_vendor_table()
    assert table, "PROVENANCE vendor table must not be empty"
    assert not any(rel.startswith("control-ok-missing/") for rel in table), (
        "control fixture is synthetic and must never be attested as verbatim"
    )
