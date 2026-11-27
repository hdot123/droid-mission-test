"""Design contract tests for 领班面墙 API 设计稿 v3.0 (mission F5/design-master).

Pure additions (mission AGENTS.md boundary): asserts the structure and anchor
resolvability of docs/领班制-面墙API设计稿-v3.md. The single data source is
tests/fixtures/wall-v3/design-contract.json — edit the fixture and this file
in the same change batch (schema-lock discipline).

Anchor resolution: test-repo anchors resolve against the repo this test runs
in; engine-repo anchors resolve against WALL_V3_ENGINE_REPO (default: the
`infraro-core` checkout under the user home). The engine repo is a read-only
reference that does not exist in CI, so engine anchors skip there — locally
they must pass (VAL-MASTER-003: anchors verified on the real trees).
"""

from __future__ import annotations

import json
import os
import re
import tomllib
import unicodedata
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[1]
# Engine repo is a read-only reference checkout (mission environment); the
# default resolves the same checkout without hardcoding an absolute home path.
ENGINE_REPO_ROOT = Path(
    os.environ.get("WALL_V3_ENGINE_REPO", str(Path.home() / "infraro-core"))
).expanduser()
FIXTURE_PATH = REPO_ROOT / "tests/fixtures/wall-v3/design-contract.json"


def _load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


FIXTURE = _load_fixture()
DOC_PATH = REPO_ROOT / FIXTURE["doc_path"]


@pytest.fixture(scope="module")
def doc_text() -> str:
    return DOC_PATH.read_text(encoding="utf-8")


def _section(text: str, header: str) -> str:
    """Return the body of one `## ` section (up to the next `## ` heading)."""
    start = text.index(header)
    nxt = text.find("\n## ", start + len(header))
    return text[start:nxt] if nxt != -1 else text[start:]


# ---------------------------------------------------------------------------
# Existence and version declaration (VAL-MASTER-001 / VAL-MASTER-006)
# ---------------------------------------------------------------------------


class TestDocExists:
    def test_main_design_doc_exists(self):
        assert DOC_PATH.is_file(), f"missing design doc: {DOC_PATH}"

    def test_fixture_files_exist(self):
        assert FIXTURE_PATH.is_file()


class TestVersionDeclaration:
    @pytest.mark.parametrize("marker", FIXTURE["preamble_markers"])
    def test_preamble_declares_v3_lineage(self, doc_text: str, marker: str):
        assert marker in doc_text, f"version/ban declaration marker missing: {marker!r}"

    def test_no_full_length_secret_shapes_in_doc(self, doc_text: str):
        # Zero-value rule: full-length token shapes must never appear; the
        # registered I8-B dummy fragment (short prefix form) is allowed.
        leak = re.search(
            r"ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|"
            r"github_pat_[A-Za-z0-9_]{20,}|fk-[A-Za-z0-9]{20,}",
            doc_text,
        )
        assert leak is None, f"full-length secret-shaped value leaked at {leak.start() if leak else 0}"


# ---------------------------------------------------------------------------
# Three-piece structure: sections (VAL-MASTER-001)
# ---------------------------------------------------------------------------


class TestThreePieceSections:
    @pytest.mark.parametrize("header", list(FIXTURE["sections"].values()))
    def test_required_section_present(self, doc_text: str, header: str):
        assert header in doc_text, f"required section missing: {header!r}"


class TestDefaultDenyCharter:
    @pytest.mark.parametrize("marker", FIXTURE["charter_markers"])
    def test_charter_states_default_deny(self, doc_text: str, marker: str):
        assert marker in doc_text, f"default-deny charter marker missing: {marker!r}"


# ---------------------------------------------------------------------------
# Ten hard rules placement (VAL-MASTER-001, cross-area mapping)
# ---------------------------------------------------------------------------


class TestTenHardRulesPlaced:
    @pytest.mark.parametrize("rule", FIXTURE["hard_rules"])
    def test_rule_has_placement_row(self, doc_text: str, rule: str):
        # Key on the 1.3 mapping table specifically: a `| ① |` row must exist
        # inside §1.3 itself. (round-1 finding: the bare `| {rule} |` check
        # was shadowed by §3.2 rows; scoping to the section removes the
        # shadow without assuming table order.)
        mapping = _section(doc_text, "### 1.3 十条硬规则逐条落位映射")
        assert f"| {rule} |" in mapping, f"hard rule {rule} has no placement row in §1.3"

    @pytest.mark.parametrize("rule", FIXTURE["hard_rules"])
    def test_rule_maps_to_own_samples(self, doc_text: str, rule: str):
        # Per-rule keying (round-1 finding: a row count >= 10 let one rule's
        # samples be deleted while a decoy `SL-` row kept the suite green).
        # Each hard rule's own row must reference at least one SL-/RS- sample.
        mapping = _section(doc_text, "### 1.3 十条硬规则逐条落位映射")
        row = next(
            (ln for ln in mapping.splitlines() if ln.startswith(f"| {rule} |")),
            None,
        )
        assert row is not None, f"hard rule {rule} has no placement row in §1.3"
        assert re.search(r"(SL|RS)-\d", row), (
            f"hard rule {rule} row references no SL-/RS- sample: {row!r}"
        )

    def test_every_rule_maps_to_samples(self, doc_text: str):
        mapping = _section(doc_text, "### 1.3 十条硬规则逐条落位映射")
        rows = [
            ln for ln in mapping.splitlines()
            if ln.startswith("| ") and ("SL-" in ln or "RS-" in ln)
        ]
        assert len(rows) >= 10, f"expected ≥10 rule rows with sample refs, got {len(rows)}"


# ---------------------------------------------------------------------------
# Seat gates and M-CAP comparison matrix (VAL-GATES-001 / VAL-GATES-002)
# ---------------------------------------------------------------------------


class TestSevenSeatGateLists:
    @pytest.mark.parametrize("seat", FIXTURE["seats"])
    def test_seat_has_gate_section(self, doc_text: str, seat: str):
        gates = _section(doc_text, FIXTURE["sections"]["gates"])
        assert f"**{seat}**" in gates, f"seat {seat} has no gate entry"

    @pytest.mark.parametrize("seat", FIXTURE["seats"])
    def test_seat_has_default_deny_declaration(self, doc_text: str, seat: str):
        gates = _section(doc_text, FIXTURE["sections"]["gates"])
        seat_body_start = gates.index(f"**{seat}**")
        nxt = gates.find(f"\n**", seat_body_start + 1)
        body = gates[seat_body_start:nxt] if nxt != -1 else gates[seat_body_start:]
        assert "default-deny" in body, f"seat {seat} lacks default-deny declaration"


class TestComparisonMatrixFullCoverage:
    def _matrix_rows(self, doc_text: str) -> dict[str, list[str]]:
        matrix = _section(doc_text, "### 2.3 与引擎 M-CAP 的对位表")
        rows: dict[str, list[str]] = {}
        for line in matrix.splitlines():
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if cells and cells[0] in FIXTURE["matrix_keys"]:
                rows[cells[0]] = cells[1:]
        return rows

    def test_all_keys_covered_for_all_seats(self, doc_text: str):
        rows = self._matrix_rows(doc_text)
        missing = [k for k in FIXTURE["matrix_keys"] if k not in rows]
        assert not missing, f"matrix keys missing rows: {missing}"
        for key in FIXTURE["matrix_keys"]:
            cells = rows[key]
            assert len(cells) == len(FIXTURE["seats"]), (
                f"key {key}: expected {len(FIXTURE['seats'])} seat cells, got {len(cells)}"
            )
            assert all(cells), f"key {key} has empty cells"

    def test_matrix_cells_match_fixture_baseline(self, doc_text: str):
        rows = self._matrix_rows(doc_text)
        for key, expected in FIXTURE["matrix_expected"].items():
            for seat_idx, verdict in enumerate(expected):
                cell = rows[key][seat_idx]
                assert cell.startswith(verdict), (
                    f"key {key} seat#{seat_idx}: {cell!r} does not carry fixture verdict {verdict!r}"
                )

    def test_boundary_event_declaration_present(self, doc_text: str):
        assert "动门＝边界事件" in doc_text


class TestExtraAndMissingGates:
    def test_extra_gates_table_complete(self, doc_text: str):
        gates = _section(doc_text, FIXTURE["sections"]["gates"])
        extra = _section(gates, "### 2.4 多出的门总表")
        n_rows = len([ln for ln in extra.splitlines() if re.match(r"^\| \d+ \|", ln)])
        assert n_rows >= FIXTURE["extra_gates_rows"], f"extra-gates rows {n_rows} < {FIXTURE['extra_gates_rows']}"
        assert extra.count("默认删") >= FIXTURE["extra_gates_rows"]
        assert "单独呈" in extra

    def test_default_delete_verdicts_present(self, doc_text: str):
        gates = _section(doc_text, FIXTURE["sections"]["gates"])
        baseline = sum(
            row.count("多出默认删") for row in FIXTURE["matrix_expected"].values()
        )
        assert gates.count("多出默认删") >= baseline, (
            f"matrix default-delete cell verdicts {gates.count('多出默认删')} < fixture baseline {baseline}"
        )

    def test_missing_gates_have_remediation(self, doc_text: str):
        gates = _section(doc_text, FIXTURE["sections"]["gates"])
        assert gates.count("缺门补齐") >= FIXTURE["missing_gates_rows"] * len(FIXTURE["seats"]) // 2
        assert "补齐" in gates


# ---------------------------------------------------------------------------
# Handoff schemas (VAL-GATES-003)
# ---------------------------------------------------------------------------


class TestHandoffSchemas:
    @pytest.mark.parametrize("schema_id", FIXTURE["schema_ids"])
    def test_four_handoff_schemas_referenced(self, doc_text: str, schema_id: str):
        assert schema_id in doc_text, f"handoff schema {schema_id} not referenced"

    @pytest.mark.parametrize("marker", FIXTURE["handoff_markers"])
    def test_handoff_principles_stated(self, doc_text: str, marker: str):
        assert marker in doc_text, f"handoff principle marker missing: {marker!r}"


# ---------------------------------------------------------------------------
# Handoff schema instance validation (VAL-GATES-003, scrutiny round-1 BLK-1)
#
# Extracts the four JSON Schema samples from docs/wall-v3/handoff-schemas.md
# itself (the draft is the source of truth, not a copy) and runs the doc's own
# negative-case tables (W-1..W-6 worker-delta, V-1..V-6 verdict, P-1..P-4
# plan-v2) plus green controls as real jsonschema instances, so a schema that
# contradicts the doc's stated evidence rules fails here. Parser contract:
# schemas live in ```json fenced blocks whose $id is foreman/<schema_id>;
# case ids appear in table rows as `| <ID> |`.
# ---------------------------------------------------------------------------

HANDOFF_DRAFT_PATH = REPO_ROOT / "docs/wall-v3/handoff-schemas.md"


def _extract_schema_samples() -> dict[str, dict]:
    """Extract $id-keyed JSON Schema objects from the draft's ```json blocks."""
    text = HANDOFF_DRAFT_PATH.read_text(encoding="utf-8")
    schemas: dict[str, dict] = {}
    for block in re.findall(r"```json\s*\n(.*?)```", text, re.DOTALL):
        try:
            obj = json.loads(block)
        except json.JSONDecodeError:
            continue
        sid = obj.get("$id", "")
        if sid.startswith("foreman/"):
            schemas[sid.removeprefix("foreman/")] = obj
    return schemas


def _judged(cause: str, refs: list[str], verdict: str = "fail", reason: str = "narrative only") -> dict:
    return {
        "id": "p1",
        "verdict": verdict,
        "cause": cause,
        "evidence_refs": refs,
        "reason": reason,
    }


def _overall(cause: str, refs: list[str], verdict: str = "fail") -> dict:
    return {"verdict": verdict, "cause": cause, "evidence_refs": refs}


def _worker_delta(cause: str, refs: list[str]) -> dict:
    return {
        "schema_version": "worker-delta.v2",
        "pid": "p1",
        "result": "failure",
        "session_outcome": "wall_killed",
        "droid_exit_code": 124,
        "stream_tail_marker": True,
        "cause": cause,
        "evidence_refs": refs,
        "narrative": "narrative only",
    }


def _plan_v2(cause: str, refs: list[str]) -> dict:
    return {
        "schema_version": "plan-v2.v1",
        "issue_number": 1,
        "death_facts": [
            {
                "pid": "p1",
                "session_outcome": "wall_killed",
                "cause": cause,
                "evidence_refs": refs,
                "note": "narrative only",
            }
        ],
        "changes": [],
    }


def _death_fact(cause: str, refs: list[str]) -> dict:
    return {
        "pid": "p1",
        "session_outcome": "wall_killed",
        "cause": cause,
        "evidence_refs": refs,
        "note": "narrative only",
    }


def _handoff() -> dict:
    return {
        "schema_version": "handoff.v1",
        "id": "p1",
        "title": "t",
        "state": "done",
        "files": [],
        "checks": [{"command": "pytest -q", "result": "pass"}],
    }


def _schema_instance_cases() -> list:
    eid = "$eid:x"
    cases = [
        # worker-delta.v2 — the doc's own table W-1..W-5 (W-6 is a
        # construction-rights verdict, not a schema instance) + green control.
        ("worker-delta.v2", "W-1", _worker_delta("unknown", [eid]), False),
        ("worker-delta.v2", "W-2", _worker_delta("wall_kill", []), False),
        ("worker-delta.v2", "W-3", _worker_delta("F-1 检查拒绝", [eid]), False),
        ("worker-delta.v2", "W-4", {k: v for k, v in _worker_delta("wall_kill", [eid]).items() if k != "cause"}, False),
        ("worker-delta.v2", "control", _worker_delta("wall_kill", [eid]), True),
        ("worker-delta.v2", "control-unknown-empty", _worker_delta("unknown", []), True),
        # verdict.v2 — judged[] rows V-1..V-4 + overall rows V-5/V-6 + controls.
        ("verdict.v2", "V-1", {"schema_version": "verdict.v2", "round": 1, "final": True, "judged": [_judged("unknown", [eid])], "conflicts": [], "overall": _overall("all_processes_judged", [eid])}, False),
        ("verdict.v2", "V-2", {"schema_version": "verdict.v2", "round": 1, "final": True, "judged": [_judged("checks_red", [])], "conflicts": [], "overall": _overall("all_processes_judged", [eid])}, False),
        ("verdict.v2", "V-3", {"schema_version": "verdict.v2", "round": 1, "final": True, "judged": [_judged("checks_red", [eid], verdict="pass with concerns")], "conflicts": [], "overall": _overall("all_processes_judged", [eid])}, False),
        ("verdict.v2", "V-4", {"schema_version": "verdict.v2", "round": 1, "final": True, "judged": [_judged("checks_red", [eid])], "conflicts": [{"process": "p1", "kind": "other", "evidence_refs": [], "summary": "s"}], "overall": _overall("all_processes_judged", [eid])}, False),
        ("verdict.v2", "V-5", {"schema_version": "verdict.v2", "round": 1, "final": True, "judged": [_judged("checks_red", [eid])], "conflicts": [], "overall": _overall("unknown", [eid], verdict="unknown")}, False),
        ("verdict.v2", "V-6", {"schema_version": "verdict.v2", "round": 1, "final": True, "judged": [_judged("checks_red", [eid], reason='"verdict": "pass"')], "conflicts": [], "overall": _overall("all_processes_judged", [eid])}, True),
        ("verdict.v2", "control", {"schema_version": "verdict.v2", "round": 1, "final": True, "judged": [_judged("checks_red", [eid])], "conflicts": [], "overall": _overall("all_processes_judged", [eid])}, True),
        ("verdict.v2", "control-unknown-empty", {"schema_version": "verdict.v2", "round": 1, "final": True, "judged": [_judged("unknown", [])], "conflicts": [], "overall": _overall("unknown", [], verdict="unknown")}, True),
        ("verdict.v2", "overall-zero-evidence", {"schema_version": "verdict.v2", "round": 1, "final": True, "judged": [_judged("checks_red", [eid])], "conflicts": [], "overall": _overall("blocked_missing_evidence", [])}, False),
        # plan-v2.v1 — the doc's own table P-1..P-4 (P-1/P-2 are
        # construction-rights / narrative verdicts and P-3's hanging ref is
        # rejected at the §3 reference-resolution layer, not by the JSON
        # Schema — all three are out of scope for a jsonschema run).
        ("plan-v2.v1", "P-4", {k: v for k, v in _plan_v2("wall_kill", [eid]).items() if k != "death_facts"}, False),
        ("plan-v2.v1", "enum-out", _plan_v2("F-1 检查拒绝", [eid]), False),
        ("plan-v2.v1", "cause-unknown-with-refs", _plan_v2("unknown", [eid]), False),
        ("plan-v2.v1", "control", _plan_v2("f1_rejected_machine_confirmed", [eid]), True),
        ("plan-v2.v1", "control-unknown-empty", _plan_v2("unknown", []), True),
        # handoff.v1 — the doc's own table H-1/H-2 + green control.
        ("handoff.v1", "H-1", {**_handoff(), "state": "完成"}, False),
        ("handoff.v1", "H-2", {**_handoff(), "checks": [{"command": "pytest", "result": "ran but failed"}]}, False),
        ("handoff.v1", "control", _handoff(), True),
    ]
    return [
        pytest.param(schema_id, case_id, instance, should_pass, id=f"{schema_id}:{case_id}")
        for schema_id, case_id, instance, should_pass in cases
    ]


class TestHandoffSchemaInstances:
    @pytest.fixture(scope="class", params=sorted(_extract_schema_samples().keys()))
    def schema_sample(self, request):
        schemas = _extract_schema_samples()
        sid = request.param
        assert sid in schemas, f"schema sample {sid} not extractable from handoff-schemas.md"
        return schemas[sid]

    def test_four_schema_samples_extractable(self):
        schemas = _extract_schema_samples()
        for sid in FIXTURE["schema_ids"]:
            assert sid in schemas, f"schema sample foreman/{sid} not extractable from handoff-schemas.md"

    @pytest.mark.parametrize("schema_id, case_id, instance, should_pass", _schema_instance_cases())
    def test_doc_negative_tables_as_instances(self, schema_id, case_id, instance, should_pass):
        schema = _extract_schema_samples()[schema_id]
        errors = sorted(
            Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.path)
        )
        if should_pass:
            assert not errors, f"{schema_id}:{case_id} must be VALID but got: {[e.message for e in errors]}"
        else:
            assert errors, f"{schema_id}:{case_id} must be REJECTED by the doc schema but validated"

    def test_conditional_keywords_present_in_all_four_schemas(self):
        # BLK-1 regression lock: every causal schema must carry the bidirectional
        # if/then pair (unknown → empty refs; non-unknown → non-empty refs) at
        # the level where the causal fields live: worker-delta/plan-v2 at top
        # level (delta) and death_facts items (plan), verdict.v2 at judged[]
        # items and overall.
        for sid, nodes in (
            ("worker-delta.v2", lambda s: [s]),
            ("verdict.v2", lambda s: [
                s["properties"]["judged"]["items"], s["properties"]["overall"]
            ]),
            ("plan-v2.v1", lambda s: [s["properties"]["death_facts"]["items"]]),
        ):
            schema = _extract_schema_samples()[sid]
            for sub in nodes(schema):
                assert sub.get("allOf"), f"{sid}: missing allOf conditional block"
                assert all("if" in c and "then" in c for c in sub["allOf"]), (
                    f"{sid}: allOf block lacks if/then pair"
                )
        # no unconditional minItems on judged[].evidence_refs (the round-1 defect)
        judged = _extract_schema_samples()["verdict.v2"]["properties"]["judged"]["items"]
        assert "minItems" not in judged["properties"]["evidence_refs"], (
            "verdict.v2: judged[].evidence_refs must not carry unconditional minItems"
        )


# ---------------------------------------------------------------------------
# Worker wrapper (VAL-GATES-004)
# ---------------------------------------------------------------------------


class TestWorkerWrapper:
    @pytest.mark.parametrize("marker", FIXTURE["wrapper_markers"])
    def test_wrapper_design_stated(self, doc_text: str, marker: str):
        assert marker in doc_text, f"wrapper design marker missing: {marker!r}"


# ---------------------------------------------------------------------------
# Out-of-graph clearance + key registry (VAL-OOGRAPH-001)
# ---------------------------------------------------------------------------


class TestOutOfGraphClearance:
    def _oog(self, doc_text: str) -> str:
        return _section(doc_text, FIXTURE["sections"]["out_of_graph"])

    @pytest.mark.parametrize("mark", FIXTURE["out_of_graph_marks"])
    def test_six_artifacts_listed(self, doc_text: str, mark: str):
        oog = self._oog(doc_text)
        assert f"| {mark} |" in oog, f"out-of-graph item {mark} not listed"

    def test_each_artifact_has_four_elements(self, doc_text: str):
        oog = self._oog(doc_text)
        for column in ("现位置锚", "图外性", "收编/禁绝", "责任席位"):
            assert column in oog, f"four-element column missing: {column}"

    @pytest.mark.parametrize("marker", FIXTURE["key_registry_markers"])
    def test_key_registry_design_stated(self, doc_text: str, marker: str):
        assert marker in doc_text, f"key registry marker missing: {marker!r}"


# ---------------------------------------------------------------------------
# Failure specs + absence-as-event (VAL-FSPEC-001)
# ---------------------------------------------------------------------------


class TestFailureSpecs:
    @pytest.mark.parametrize("field", FIXTURE["failure_spec_markers"]["fields"])
    def test_four_field_format_used_for_all_seats(self, doc_text: str, field: str):
        fspec = _section(doc_text, FIXTURE["sections"]["failure_specs"])
        assert field in fspec, f"failure-spec field {field!r} not stated in section"
        seat_rows = [
            ln for ln in fspec.splitlines()
            if re.match(r"^\| (" + "|".join(FIXTURE["seats"]) + r") \|", ln)
        ]
        assert len(seat_rows) >= len(FIXTURE["seats"]), (
            f"expected ≥{len(FIXTURE['seats'])} seat rows under the four-field table, got {len(seat_rows)}"
        )

    @pytest.mark.parametrize("marker", FIXTURE["failure_spec_markers"]["extra"])
    def test_cure_merge_and_layer3_noted(self, doc_text: str, marker: str):
        fspec = _section(doc_text, FIXTURE["sections"]["failure_specs"])
        assert marker in fspec, f"failure-spec extra marker missing: {marker!r}"

    @pytest.mark.parametrize("inv", FIXTURE["invariants"])
    def test_seven_absence_invariants_listed(self, doc_text: str, inv: str):
        assert inv in doc_text, f"invariant {inv} missing"


# ---------------------------------------------------------------------------
# Acceptance line: SL samples, latency, live evidence (VAL-FSPEC-002)
# ---------------------------------------------------------------------------


class TestMustDieSamples:
    @pytest.mark.parametrize("sample", FIXTURE["sla_samples"])
    def test_sl_family_indexed(self, doc_text: str, sample: str):
        assert sample in doc_text, f"must-die sample {sample} missing from acceptance line"


class TestEnforcementLatency:
    @pytest.mark.parametrize("marker", FIXTURE["latency_markers"])
    def test_latency_protocol_stated(self, doc_text: str, marker: str):
        acceptance = _section(doc_text, FIXTURE["sections"]["acceptance"])
        assert marker in acceptance, f"latency marker missing in acceptance section: {marker!r}"

    def test_upper_bound_per_run_discipline(self, doc_text: str):
        acceptance = _section(doc_text, FIXTURE["sections"]["acceptance"])
        assert "N≥5" in acceptance
        assert "实测" in acceptance


class TestSeatProbeExplicitMapping:
    """Round-2 discipline: every per-seat probe clause carries an explicit
    probe->SL mapping row (the blanket sentence was deleted). The five
    previously-unsampled probes must each name their SL carrier and the
    acceptance-line map must carry an explicit mapping table."""

    PROBE_CLAUSES = [
        # (seat-gates probe substring, SL carrier the clause must name)
        ("接线锁探针", "SL-13a"),
        ("候选分支越权写探针", "SL-13b"),
        ("D-2 封章粘滞负例", "SL-13c"),
        ("human_stop 消费探针", "SL-13d"),
        ("pick fail-closed 变体探针", "SL-13e"),
        ("droid 会话禁入探针", "SL-13"),
    ]

    def test_seat_gates_probe_clauses_name_sl_carrier(self):
        gates = (REPO_ROOT / "docs/wall-v3/seat-gates.md").read_text(encoding="utf-8")
        for clause, sl in self.PROBE_CLAUSES:
            region = next(
                (seg for seg in gates.split("probes = ")
                 if clause in seg.split("\n", 1)[0]),
                None,
            )
            assert region is not None, f"probe clause not found in seat-gates.md: {clause!r}"
            assert sl in region, f"probe clause {clause!r} does not name {sl}"

    def test_acceptance_map_has_explicit_probe_table(self):
        alm = (REPO_ROOT / "docs/wall-v3/acceptance-line-map.md").read_text(encoding="utf-8")
        assert "席位 probe→SL 显式映射表" in alm, "explicit probe mapping table missing"
        table = alm[alm.index("席位 probe→SL 显式映射表"):]
        # blanket folded sentence must be gone
        assert "不再另立族号" not in table, "blanket probe-coverage sentence survived"
        for _, sl in self.PROBE_CLAUSES:
            assert f"| {sl}" in table or f"| {sl} " in table, f"{sl} has no explicit mapping row"


class TestKeyLedgerFullTreeScan:
    """Round-2 orchestrator ruling: hard rule 9 covers the whole production
    workflow tree; criterion 1, the guard face, and the ledger site set must
    share one boundary (measured: 12 files / 6 secret names / 82 expansions)."""

    def test_workflow_tree_secret_scan_baseline(self):
        wf_dir = REPO_ROOT / ".github/workflows"
        files = sorted(wf_dir.glob("*.yml"))
        expansions = []
        names = set()
        for f in files:
            for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if "secrets." in ln:
                    expansions.append((f.name, i))
                    names.update(
                        part.split("}")[0].strip()
                        for part in ln.split("secrets.")[1:]
                    )
        with_secrets = [f for f in files if "secrets." in f.read_text(encoding="utf-8")]
        assert len(with_secrets) == 12, (
            f"expected 12 workflow files carrying secrets, got {len(with_secrets)}"
        )
        assert len(expansions) == 82, f"expected 82 expansion lines, got {len(expansions)}"
        assert len(names) == 6, f"expected 6 secret names, got {sorted(names)}"
        assert "I8_TEAM_TRIGGER_PAT" in names, "6th secret missing from scan"

    def test_ledger_design_states_full_tree_scope(self, doc_text: str):
        oog = (REPO_ROOT / "docs/wall-v3/out-of-graph-artifacts.md").read_text(encoding="utf-8")
        for marker in ("12 个 workflow 文件", "82 条展开行", "I8_TEAM_TRIGGER_PAT"):
            assert marker in oog, f"full-tree marker missing in ledger doc: {marker!r}"
        assert "三者同边界" in oog or "三者口径一致" in doc_text, (
            "criterion/guard/site-set boundary alignment not declared"
        )

    def test_sl7_scan_boundary_is_full_tree(self, doc_text: str):
        """Round-3 RC-7: SL-7's injection scan face is the full production
        workflow tree (12 files / 82 lines), not the legacy four-file set."""
        assert "四文件集" not in doc_text or "四文件集」旧表述废止" in doc_text or "四文件集」旧口径废止" in doc_text, (
            "stale four-file scan wording without deprecation note"
        )
        alm = (REPO_ROOT / "docs/wall-v3/acceptance-line-map.md").read_text(encoding="utf-8")
        sl7 = alm[alm.index("### 2.7 SL-7"):alm.index("### 2.8")]
        assert "12 文件全树边界" in sl7, "SL-7 scan face must name the full-tree boundary"

    def test_repo_secret_roster_single_statement(self):
        """Round-3 RC-3: the repo-secret roster is stated in one place
        (out-of-graph §3.3); measured 2026-11-28 via `gh secret list`:
        six names = in-service five + CI_KEY spare."""
        oog = (REPO_ROOT / "docs/wall-v3/out-of-graph-artifacts.md").read_text(encoding="utf-8")
        assert "repo-secret 名册六条一处陈述" in oog, "roster single-statement header missing"
        assert "CI_KEY（备用件" in oog, "spare CI_KEY roster row missing"

    def test_trigger_pat_nature_is_use(self):
        """Round-3 RC-2: I8_TEAM_TRIGGER_PAT is a trigger credential (use),
        not a capability-change key — aligned across ledger sample, §3.3
        table and §3.4 verdict sentence."""
        oog = (REPO_ROOT / "docs/wall-v3/out-of-graph-artifacts.md").read_text(encoding="utf-8")
        sample = oog[oog.index("name = \"I8_TEAM_TRIGGER_PAT\""):]
        assert 'nature = "use"' in sample, "ledger sample nature must be use"
        assert "触发凭证" in sample, "trigger-credential rationale missing"

    def test_ledger_sample_anchor_lines_resolve(self):
        """Round-3 RC-1: ledger [[key]] consumes anchor lines must resolve
        with matching content (env-check.yml:240 was a WORKER_CI_KEY line —
        wrong-anchor class)."""
        oog_text = (REPO_ROOT / "docs/wall-v3/out-of-graph-artifacts.md").read_text(encoding="utf-8")
        ledger = oog_text[oog_text.index("### 3.2 台账 schema"):oog_text.index("### 3.3")]
        forbidden = "env-check.yml:240"
        assert forbidden not in ledger, (
            "ledger carries env-check.yml:240 anchor — that line is wall-step "
            "S_WORKER_CI_KEY expansion, not a PROJECTS_STATE_PAT consumption"
        )
        envcheck = (REPO_ROOT / ".github/workflows/env-check.yml").read_text(encoding="utf-8").splitlines()
        assert "S_PROJECTS_STATE_PAT" in envcheck[194], "env-check.yml:195 anchor content mismatch"
        assert "S_WORKER_CI_KEY" in envcheck[238], "env-check.yml:239 is the WORKER_CI_KEY wall-step line"

    def test_ledger_anchor_roster_in_fixture(self):
        """Round-3 RC-1 companion: the ledger anchor roster is registered in
        the design-contract fixture (ledger_anchor_sources) so ledger anchors
        cannot drift unilaterally."""
        fixture = json.loads(
            (REPO_ROOT / "tests/fixtures/wall-v3/design-contract.json").read_text(encoding="utf-8")
        )
        assert "ledger_anchor_sources" in fixture, "fixture lacks ledger_anchor_sources"
        sources = fixture["ledger_anchor_sources"]
        files = [s.get("file") for s in sources if isinstance(s, dict) and "file" in s]
        assert "docs/wall-v3/out-of-graph-artifacts.md" in files, "ledger doc not registered"
        assert ".github/workflows/i8-zero-escape-live-orchestrator.yml" in files, "orchestrator anchor set not registered"


class TestLiveEvidenceGate:
    @pytest.mark.parametrize("marker", FIXTURE["live_evidence_markers"])
    def test_no_number_no_build_criteria(self, doc_text: str, marker: str):
        assert marker in doc_text, f"live-evidence marker missing: {marker!r}"


# ---------------------------------------------------------------------------
# Round-59 four problems regression (VAL-CROSS-001)
# ---------------------------------------------------------------------------


class TestFourProblemsPlaced:
    @pytest.mark.parametrize("problem", FIXTURE["four_problems"], ids=lambda p: p["id"])
    def test_problem_has_design_and_samples(self, doc_text: str, problem: dict):
        for marker in problem["markers"]:
            assert marker in doc_text, f"{problem['id']} marker missing: {marker!r}"

    @pytest.mark.parametrize("rs", FIXTURE["regression_samples"])
    def test_regression_samples_indexed(self, doc_text: str, rs: str):
        assert rs in doc_text, f"regression sample {rs} missing"


# ---------------------------------------------------------------------------
# Swap-in criteria (VAL-CROSS-003)
# ---------------------------------------------------------------------------


class TestSwapInCriteria:
    def test_three_criteria_sections_present(self, doc_text: str):
        for heading in ("### 7.1 判据一：门清单不变", "### 7.2 判据二：旧封印测试整套全过", "### 7.3 判据三：失败规范对位"):
            assert heading in doc_text, f"swap-in criterion heading missing: {heading!r}"

    @pytest.mark.parametrize("marker", FIXTURE["swap_in_markers"])
    def test_swap_in_markers_stated(self, doc_text: str, marker: str):
        assert marker in doc_text, f"swap-in marker missing: {marker!r}"


# ---------------------------------------------------------------------------
# Engine unclosed-item ban (VAL-MASTER-007)
# ---------------------------------------------------------------------------


class TestEngineBanDeclaration:
    @pytest.mark.parametrize("marker", FIXTURE["ban_markers"])
    def test_ban_declaration_stated(self, doc_text: str, marker: str):
        assert marker in doc_text, f"engine ban marker missing: {marker!r}"

    def test_two_gate_wording_only(self, doc_text: str):
        # R-29 evolution: citations must use the ruled two-gate wording, and
        # the ban section must name both forbidden citation forms explicitly.
        ban = _section(doc_text, "## §0b 引擎未闭合项禁抄声明")
        assert "两门" in ban
        assert "quality-gate" in ban and "substrate-gate-suite" in ban


# ---------------------------------------------------------------------------
# Ruling list (VAL-MASTER-001: 待大哥裁决清单)
# ---------------------------------------------------------------------------


class TestRulingList:
    def test_ruling_section_present_with_items(self, doc_text: str):
        rulings = _section(doc_text, FIXTURE["sections"]["rulings"])
        n_rows = len([ln for ln in rulings.splitlines() if re.match(r"^\| \d+ \|", ln)])
        assert n_rows >= 8, f"expected ≥8 ruling items, got {n_rows}"
        assert "呈大哥裁" in rulings or "大哥" in rulings

    @pytest.mark.parametrize("marker", FIXTURE["ruling_markers"])
    def test_known_ruling_topics_covered(self, doc_text: str, marker: str):
        assert marker in doc_text, f"ruling topic marker missing: {marker!r}"


# ---------------------------------------------------------------------------
# Anchor resolvability (VAL-MASTER-003)
# ---------------------------------------------------------------------------


def _anchor_params() -> list:
    return [
        pytest.param(a, id=f"{a['repo']}:{a['file']}:{a.get('line', 'exists')}")
        for a in FIXTURE["anchors"]
    ]


class TestAnchorResolvability:
    @staticmethod
    def _resolve(repo_root: Path, anchor: dict) -> str | None:
        path = repo_root / anchor["file"]
        if not path.is_file():
            return f"file not found: {path}"
        if anchor.get("exists"):
            return None
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        line = anchor["line"]
        if not (1 <= line <= len(lines)):
            return f"line {line} out of range ({len(lines)} lines) in {anchor['file']}"
        window = lines[line - 1 : line + anchor.get("window", 0)]
        needle = anchor["contains"]
        if not any(needle in ln for ln in window):
            preview = lines[line - 1][:120]
            return (
                f"anchor miss: {anchor['file']}:{line} expected {needle!r}; "
                f"got {preview!r}"
            )
        return None

    @pytest.mark.parametrize("anchor", _anchor_params())
    def test_anchor_resolves(self, anchor: dict):
        if anchor["repo"] == "engine" and not ENGINE_REPO_ROOT.is_dir():
            pytest.skip(f"engine repo not present at {ENGINE_REPO_ROOT}")
        root = REPO_ROOT if anchor["repo"] == "test" else ENGINE_REPO_ROOT
        error = self._resolve(root, anchor)
        assert error is None, error

    def test_engine_anchors_not_silently_skipped_locally(self):
        # VAL-MASTER-003 gate: when the engine repo is available (local dev,
        # validator runs), engine anchors must actually be exercised.
        if not ENGINE_REPO_ROOT.is_dir():
            pytest.skip(f"engine repo not present at {ENGINE_REPO_ROOT}")
        engine_anchors = [a for a in FIXTURE["anchors"] if a["repo"] == "engine"]
        assert engine_anchors, "fixture declares no engine anchors"
        failures = [msg for a in engine_anchors if (msg := self._resolve(ENGINE_REPO_ROOT, a))]
        assert not failures, "engine anchor failures:\n" + "\n".join(failures)

    def test_runtime_state_anchor_excluded(self):
        # memory/ is memory-core runtime state (untracked, off-contract):
        # it must stay out of the machine-checked anchor set.
        files = {a["file"] for a in FIXTURE["anchors"]}
        assert not any(f.startswith("memory/") for f in files)


# ---------------------------------------------------------------------------
# TOML fence machine-parseability (BLK-2 / VAL-GATES-001 regression)
# ---------------------------------------------------------------------------

# ```toml fences across all wall-v3 docs must parse with stdlib tomllib.
# Round-2 scrutiny caught a non-ASCII math operator (U+2248) breaking a
# key/value line in seat-gates.md; comments and prose may keep such symbols,
# key=value lines may not — this test is the regression gate for both modes.
TOML_FENCE_RE = re.compile(r"^```toml[ \t]*$(.*?)^```[ \t]*$", re.M | re.S)
MATH_SYMBOLS = "≈≤≥≠±×÷→←↔⇒"

WALL_V3_DOC_DIR = REPO_ROOT / "docs/wall-v3"
# The assembled master doc embeds seat-gate excerpts; its toml fence set must
# also parse (currently empty, kept for future embeds).
MASTER_DOC_PATH = REPO_ROOT / "docs/领班制-面墙API设计稿-v3.md"


def _wall_v3_toml_fences() -> list[tuple[str, int, str]]:
    docs = sorted(WALL_V3_DOC_DIR.glob("*.md")) + [MASTER_DOC_PATH]
    fences: list[tuple[str, int, str]] = []
    for path in docs:
        text = path.read_text(encoding="utf-8")
        for m in TOML_FENCE_RE.finditer(text):
            lineno = text[: m.start()].count("\n") + 1
            fences.append((str(path.relative_to(REPO_ROOT)), lineno, m.group(1)))
    return fences


def _math_symbol_hits(fence_body: str) -> list[str]:
    hits = []
    for lineno, line in enumerate(fence_body.split("\n"), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue  # comments and blank lines may keep math symbols
        hits.extend(
            f"U+{ord(ch):04X} {unicodedata.name(ch, '?')} on line {lineno}"
            for ch in stripped
            if ch in MATH_SYMBOLS
        )
    return hits


class TestWallV3TomlFencesParse:
    @pytest.mark.parametrize(
        "fence", _wall_v3_toml_fences(), ids=lambda f: f"{f[0]}:{f[1]}"
    )
    def test_fence_parses(self, fence: tuple[str, int, str]):
        doc_rel, lineno, body = fence
        try:
            tomllib.loads(body)
        except tomllib.TOMLDecodeError as exc:
            pytest.fail(f"{doc_rel}:{lineno} toml fence unparseable: {exc}")

    @pytest.mark.parametrize(
        "fence", _wall_v3_toml_fences(), ids=lambda f: f"{f[0]}:{f[1]}"
    )
    def test_fence_no_math_symbols_on_key_value_lines(
        self, fence: tuple[str, int, str]
    ):
        doc_rel, lineno, body = fence
        hits = _math_symbol_hits(body)
        assert not hits, (
            f"{doc_rel}:{lineno} math symbols inside key=value lines "
            f"(allowed only in comments/prose): {hits}"
        )

    def test_seat_gates_fences_present(self):
        # Guard against the scan silently degrading to zero fences.
        seat_fences = [f for f in _wall_v3_toml_fences() if "seat-gates" in f[0]]
        assert seat_fences, "seat-gates.md lost its toml fences — scan is vacuous"

