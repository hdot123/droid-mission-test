"""F1 worker-delta structured session outcome (death facts on the wall).

The delta step must classify the session outcome entirely from machine
evidence — the session step's exit code plus the tail shape of
worker-stream.jsonl — and the wall's workers slice must carry those facts
as optional, backward-compatible fields:

- job cancelled (25m wall)                          -> job_wall_cancelled
- exit 124 / exit 137 (GNU timeout TERM / --kill-after SIGKILL)
  or stream tail is the "Tool execution was interrupted"
  tool_error or (non-zero exit outside {0, 1} with no
  completion event anywhere in the stream)          -> wall_killed
- droid self-crash (exit 1 or negative, no completion) -> ok
- session self-ended (exit 0 or completion event)   -> ok

Three wall slices exercise the schema: legacy (no new fields) validates,
the new fields validate, an illegal outcome enum is rejected.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from foreman_run_lib import init_wall, save_wall, validate_with_jsonschema  # noqa: E402
from lint_workflow_wall_exits import job_spans, step_chunks  # noqa: E402
from merge_worker_deltas import apply_deltas  # noqa: E402
import write_worker_delta  # noqa: E402

FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "worker-r58d"
CONTROL_ROOT = FIXTURE_ROOT / "control-ok-missing"
INTERRUPT_MARKER = "Error: Tool execution was interrupted"
WORKFLOW = ROOT / ".github" / "workflows" / "team.yml"

INTERRUPT_TAIL_EVENT = json.dumps(
    {
        "type": "tool_result",
        "id": "call_x",
        "isError": True,
        "error": {"type": "tool_error", "message": INTERRUPT_MARKER},
    }
)
HEALTHY_TAIL_EVENT = json.dumps(
    {
        "type": "message",
        "role": "assistant",
        "text": "done",
    }
)
# Real corpus shape: healthy droid sessions end the stream with a
# completion event (54/97 real streams end with type "completion").
COMPLETION_TAIL_EVENT = json.dumps(
    {
        "type": "completion",
        "finalText": "Process card complete.",
        "numTurns": 14,
        "durationMs": 311439,
    }
)

WORKERS_REQUIRED = [
    "schema_version",
    "any_cancelled",
    "any_failed",
    "completed_pids",
    "cancelled_pids",
    "cancel_reason_by_pid",
]


def _job_step_chunk(job: str, step_name: str) -> str:
    text = WORKFLOW.read_text(encoding="utf-8")
    spans = job_spans(text)
    assert job in spans, f"job {job} not found in team.yml"
    start, end = spans[job]
    for chunk in step_chunks(text[start:end]):
        if f"name: {step_name}" in chunk:
            return chunk
    raise AssertionError(f"step {step_name!r} not found in job {job}")


def _run_delta_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    result: str,
    droid_exit_code: int | None,
    stream_text: str | None,
) -> dict:
    stream_path = tmp_path / "worker-stream.jsonl"
    stream_path.write_text(stream_text if stream_text is not None else "", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv(
        "DROID_EXIT_CODE", "" if droid_exit_code is None else str(droid_exit_code)
    )
    out = tmp_path / "worker-delta.json"
    monkeypatch.setattr(
        sys,
        "argv",
        ["write_worker_delta", "--pid", "hslconv", "--result", result, "--out", str(out)],
    )
    assert write_worker_delta.main() == 0
    return json.loads(out.read_text(encoding="utf-8"))


# --- classification: exit code + stream tail, zero model involvement -------


def test_classify_wall_killed_exit_124_interrupted_tail():
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=124,
        job_cancelled=False,
        stream_tail=json.dumps({"type": "message"}) + "\n" + INTERRUPT_TAIL_EVENT + "\n",
    )
    assert outcome == "wall_killed"
    assert marker is True


# --- scrutiny NC-2: explicit wall branches stay pinned over completion-present
#     streams (the catch-all clause would otherwise silently backstop them) ----


@pytest.mark.parametrize("exit_code", [124, 137])
def test_classify_wall_killed_explicit_branches_with_completion_present(exit_code):
    """A completion event anywhere in the stream proves a self-ended session
    in the abstract — but the explicit wall exits 124/137 outrank it: those
    codes are the GNU timeout kill verdicts, never a self-end. Deleting
    either explicit branch must go red (with a completion-present stream the
    catch-all would otherwise backstop the deletion silently)."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=exit_code,
        job_cancelled=False,
        stream_tail=HEALTHY_TAIL_EVENT + "\n" + COMPLETION_TAIL_EVENT + "\n",
    )
    assert outcome == "wall_killed"
    assert marker is False


@pytest.mark.parametrize("exit_code", [124, 137, 2])
def test_classify_job_wall_cancelled_priority_over_wall_codes(exit_code):
    """The job envelope (25m cancel) outranks every session-side kill verdict:
    cancelled wins over exit 124, 137 AND the catch-all wall codes."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=exit_code,
        job_cancelled=True,
        stream_tail=HEALTHY_TAIL_EVENT + "\n" + COMPLETION_TAIL_EVENT + "\n",
    )
    assert outcome == "job_wall_cancelled"
    assert marker is False


def test_classify_wall_killed_interrupted_tail_with_zero_exit():
    """The interrupted tail alone proves the kill: the OR rule (exit 124 or
    interrupted tail) must not be masked by a zero pipeline exit."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=0,
        job_cancelled=False,
        stream_tail=INTERRUPT_TAIL_EVENT + "\n",
    )
    assert outcome == "wall_killed"
    assert marker is True


def test_classify_wall_killed_exit_137_no_cancel(tmp_path=None):
    """GNU timeout --kill-after SIGKILL path: a process that ignores TERM
    exits 137, not 124. Same wall family, same verdict."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=137,
        job_cancelled=False,
        stream_tail=HEALTHY_TAIL_EVENT + "\n",
    )
    assert outcome == "wall_killed"
    assert marker is False


@pytest.mark.parametrize("exit_code", [2, 3, 15, 255])
def test_classify_wall_killed_nonzero_exit_without_completion_event(exit_code):
    """A non-zero session exit whose stream never carried a completion
    event is an abnormal termination of the same machine-provable family
    as a wall kill (a self-ended session always emits completion)."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=exit_code,
        job_cancelled=False,
        stream_tail=HEALTHY_TAIL_EVENT + "\n",
    )
    assert outcome == "wall_killed"
    assert marker is False


def test_classify_wall_killed_nonzero_exit_missing_stream():
    """Missing/unreadable stream cannot show a completion event, so a
    non-zero exit over it stays in the wall_killed family."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=2,
        job_cancelled=False,
        stream_tail=None,
    )
    assert outcome == "wall_killed"
    assert marker is False


def test_classify_exit_1_without_completion_is_droid_self_crash_ok():
    """Exit 1 with no completion is the droid self-crash death family, not
    a wall kill: the coarse enum keeps it ok and droid_exit_code carries
    the detail; the salvage guard reads the exit code directly."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=1,
        job_cancelled=False,
        stream_tail=HEALTHY_TAIL_EVENT + "\n",
    )
    assert outcome == "ok"
    assert marker is False


def test_classify_negative_exit_without_completion_is_droid_self_crash_ok():
    """Negative exit codes are not producible in production (bash $? is
    0-255; the 128+signal convention yields POSITIVE codes like 137/143),
    but a negative value arriving over the env face is a process death
    outside the GNU timeout wall family: same carve-out as exit 1, never
    wall_killed."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=-15,
        job_cancelled=False,
        stream_tail=None,
    )
    assert outcome == "ok"
    assert marker is False


def test_classify_exit_1_with_completion_event_is_ok():
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=1,
        job_cancelled=False,
        stream_tail=COMPLETION_TAIL_EVENT + "\n",
    )
    assert outcome == "ok"
    assert marker is False


def test_classify_ok_healthy_tail_zero_exit():
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=0,
        job_cancelled=False,
        stream_tail=HEALTHY_TAIL_EVENT + "\n",
    )
    assert outcome == "ok"
    assert marker is False


def test_classify_zero_exit_with_completion_event_is_ok():
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=0,
        job_cancelled=False,
        stream_tail=COMPLETION_TAIL_EVENT + "\n",
    )
    assert outcome == "ok"
    assert marker is False


def test_classify_job_wall_cancelled_wins_over_exit_124(tmp_path=None):
    """A 25m job-wall cancel is attributed to the job envelope even when the
    session inside it died to its own wall."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=124,
        job_cancelled=True,
        stream_tail=INTERRUPT_TAIL_EVENT + "\n",
    )
    assert outcome == "job_wall_cancelled"
    assert marker is True


# --- scrutiny NC-1: the classifier scans the WHOLE stream for completion ----


def test_classify_completion_followed_by_trailing_event_is_ok_at_nonzero_exit():
    """NC-1 pinning shape (red on the old last-line-only scan): a completion
    event followed by one more trailing event — the completion is NOT the
    last line, yet it proves the session ended on its own, so a non-wall,
    non-self exit (2) over such a stream is ok, not wall_killed. The delta
    CLI feeds the classifier the whole stream text; the last line is
    consulted only for the interrupt marker."""
    stream = (
        HEALTHY_TAIL_EVENT + "\n" + COMPLETION_TAIL_EVENT + "\n" + HEALTHY_TAIL_EVENT + "\n"
    )
    for exit_code in (2, 3):
        outcome, marker = write_worker_delta.classify_session_outcome(
            droid_exit_code=exit_code,
            job_cancelled=False,
            stream_tail=stream,
        )
        assert outcome == "ok", exit_code
        assert marker is False


def test_delta_cli_completion_midstream_is_ok_at_exit_2(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """CLI-level NC-1 pin: completion followed by a trailing event, exit 2 —
    the delta must record ok (the old implementation scanned only the last
    line and mis-reported wall_killed here)."""
    payload = _run_delta_cli(
        tmp_path,
        monkeypatch,
        result="failure",
        droid_exit_code=2,
        stream_text=HEALTHY_TAIL_EVENT + "\n" + COMPLETION_TAIL_EVENT + "\n"
        + HEALTHY_TAIL_EVENT + "\n",
    )
    assert payload["session_outcome"] == "ok"
    assert payload["droid_exit_code"] == 2
    assert payload["stream_tail_marker"] is False


def test_classify_wall_killed_exit_124_with_empty_stream():
    """Exit 124 is the wall-kill verdict on its own; a missing/unreadable
    stream must not downgrade it."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=124, job_cancelled=False, stream_tail=None
    )
    assert outcome == "wall_killed"
    assert marker is False


def test_classify_droid_self_exit_clean_tail_is_ok():
    """Exit 1 (droid self-crash) with a clean tail is not a wall death: the
    coarse enum keeps it ok and droid_exit_code carries the detail — the
    salvage guard reads the exit code directly for this family."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=1,
        job_cancelled=False,
        stream_tail=HEALTHY_TAIL_EVENT + "\n",
    )
    assert outcome == "ok"
    assert marker is False


@pytest.mark.parametrize(
    "tail_line",
    ["null", "42", "[1,2]", "true", '"text"'],
)
def test_classify_json_non_object_tail_returns_false_no_crash(tail_line):
    """A JSON-valid-but-non-object tail line (truncated stream, split
    write, junk) must be judged not-interrupted, never raise: the
    classifier runs inside the delta step under if: always(), and an
    exception there aborts the whole delta write — the pid then reaches
    the merge with no delta at all (legacy result fact lost too)."""
    outcome, marker = write_worker_delta.classify_session_outcome(
        droid_exit_code=124,
        job_cancelled=False,
        stream_tail=HEALTHY_TAIL_EVENT + "\n" + tail_line + "\n",
    )
    assert outcome == "wall_killed"  # exit 124 still proves the kill
    assert marker is False


# --- delta CLI end-to-end ---------------------------------------------------


def test_delta_cli_wall_killed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    payload = _run_delta_cli(
        tmp_path,
        monkeypatch,
        result="failure",
        droid_exit_code=124,
        stream_text=HEALTHY_TAIL_EVENT + "\n" + INTERRUPT_TAIL_EVENT + "\n",
    )
    assert payload["pid"] == "hslconv"
    assert payload["result"] == "failure"
    assert payload["session_outcome"] == "wall_killed"
    assert payload["droid_exit_code"] == 124
    assert payload["stream_tail_marker"] is True


def test_delta_cli_ok(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    payload = _run_delta_cli(
        tmp_path,
        monkeypatch,
        result="success",
        droid_exit_code=0,
        stream_text=HEALTHY_TAIL_EVENT + "\n",
    )
    assert payload["session_outcome"] == "ok"
    assert payload["droid_exit_code"] == 0
    assert payload["stream_tail_marker"] is False
    assert "cancel_reason" not in payload


def test_delta_cli_job_wall_cancelled(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    payload = _run_delta_cli(
        tmp_path,
        monkeypatch,
        result="cancelled",
        droid_exit_code=124,
        stream_text=HEALTHY_TAIL_EVENT + "\n",
    )
    assert payload["session_outcome"] == "job_wall_cancelled"
    assert payload["droid_exit_code"] == 124
    assert payload["stream_tail_marker"] is False
    assert payload["cancel_reason"] == "job_wall_25m"


def test_delta_cli_skipped_session_records_null_exit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """prep_should_run=false cancels the matrix before any session ran: the
    delta must not fabricate an exit code."""
    payload = _run_delta_cli(
        tmp_path,
        monkeypatch,
        result="cancelled",
        droid_exit_code=None,
        stream_text=None,
    )
    assert payload["session_outcome"] == "job_wall_cancelled"
    assert payload["droid_exit_code"] is None
    assert payload["stream_tail_marker"] is False


def test_delta_cli_replays_r58_wall_killed_stream(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The vendored r58 stream (52 events, interrupted tail, no completion)
    must classify as wall_killed when replayed with the recorded exit 124."""
    stream = (FIXTURE_ROOT / "worker-stream.jsonl").read_text(encoding="utf-8")
    payload = _run_delta_cli(
        tmp_path,
        monkeypatch,
        result="failure",
        droid_exit_code=124,
        stream_text=stream,
    )
    assert payload["session_outcome"] == "wall_killed"
    assert payload["droid_exit_code"] == 124
    assert payload["stream_tail_marker"] is True
    assert payload == json.loads(
        (FIXTURE_ROOT / "worker-delta-wall-killed.json").read_text(encoding="utf-8")
    )


def test_delta_cli_replays_control_ok_tail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The control shape (self-ended session, healthy tail) must classify as
    ok — session_outcome keys on session evidence, never on result alone."""
    tail = (CONTROL_ROOT / "worker-stream-tail.jsonl").read_text(encoding="utf-8")
    payload = _run_delta_cli(
        tmp_path,
        monkeypatch,
        result="failure",
        droid_exit_code=0,
        stream_text=tail,
    )
    assert payload["session_outcome"] == "ok"
    assert payload["droid_exit_code"] == 0
    assert payload["stream_tail_marker"] is False
    assert payload["result"] == "failure"


def test_delta_cli_r58_stream_with_completion_end_is_ok_at_any_self_exit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The same r58 stream with a completion event appended at the end
    models a session that finished on its own: ok at exit 0 and at a
    self-exit exit 1 — the completion event clears the abnormal-termination
    clause for every exit outside the wall family."""
    stream = (FIXTURE_ROOT / "worker-stream.jsonl").read_text(encoding="utf-8")
    for exit_code in (0, 1):
        payload = _run_delta_cli(
            tmp_path,
            monkeypatch,
            result="failure",
            droid_exit_code=exit_code,
            stream_text=stream + COMPLETION_TAIL_EVENT + "\n",
        )
        assert payload["session_outcome"] == "ok", exit_code
        assert payload["droid_exit_code"] == exit_code
        assert payload["stream_tail_marker"] is False


def test_delta_cli_r58_stream_nonzero_exit_without_completion_is_wall_killed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The r58 stream ends interrupted with no completion event anywhere:
    replayed at a non-wall-family non-zero exit it is still an abnormal
    termination -> wall_killed (the completion-absence clause)."""
    stream = (FIXTURE_ROOT / "worker-stream.jsonl").read_text(encoding="utf-8")
    payload = _run_delta_cli(
        tmp_path,
        monkeypatch,
        result="failure",
        droid_exit_code=2,
        stream_text=stream,
    )
    assert payload["session_outcome"] == "wall_killed"
    assert payload["droid_exit_code"] == 2
    assert payload["stream_tail_marker"] is True


# --- delta merge into the wall slice ----------------------------------------


def test_apply_deltas_carries_session_outcome_fields():
    wall = init_wall(run_id="f1", issue_number=9)
    wall = apply_deltas(
        wall,
        [
            {
                "pid": "hslconv",
                "result": "failure",
                "session_outcome": "wall_killed",
                "droid_exit_code": 124,
                "stream_tail_marker": True,
            }
        ],
    )
    w = wall["workers"]
    assert w["session_outcome_by_pid"] == {"hslconv": "wall_killed"}
    assert w["droid_exit_code_by_pid"] == {"hslconv": 124}
    assert w["stream_tail_marker_by_pid"] == {"hslconv": True}
    # r58 was a job failure, not a cancel: cancel_reason semantics untouched
    assert w["cancel_reason_by_pid"] == {}
    assert not validate_with_jsonschema(wall), validate_with_jsonschema(wall)


def test_apply_deltas_cancelled_keeps_cancel_reason_semantics():
    wall = init_wall(run_id="f1c", issue_number=9)
    wall = apply_deltas(
        wall,
        [
            {
                "pid": "cancelme",
                "result": "cancelled",
                "cancel_reason": "job_wall_25m",
                "session_outcome": "job_wall_cancelled",
                "droid_exit_code": None,
                "stream_tail_marker": False,
            }
        ],
    )
    w = wall["workers"]
    assert w["cancelled_pids"] == ["cancelme"]
    assert w["cancel_reason_by_pid"] == {"cancelme": "job_wall_25m"}
    assert w["session_outcome_by_pid"] == {"cancelme": "job_wall_cancelled"}
    assert w["droid_exit_code_by_pid"] == {"cancelme": None}
    assert not validate_with_jsonschema(wall), validate_with_jsonschema(wall)


def test_apply_deltas_legacy_delta_shape_stays_byte_identical():
    """A legacy delta (pid + result only — the r58 CI-recorded shape) must
    produce exactly the pre-F1 workers slice: no new keys appear."""
    wall = apply_deltas(
        init_wall(run_id="f1l", issue_number=9),
        [{"pid": "hslconv", "result": "failure"}],
    )
    w = wall["workers"]
    assert "session_outcome_by_pid" not in w
    assert "droid_exit_code_by_pid" not in w
    assert "stream_tail_marker_by_pid" not in w
    assert w["completed_pids"] == ["hslconv"]
    assert w["any_failed"] is True
    assert not validate_with_jsonschema(wall), validate_with_jsonschema(wall)


# --- schema: backward-compatible extension ----------------------------------


def _workers_slice_schema() -> dict:
    schema = json.loads(
        (ROOT / "schemas" / "foreman-run.v1.schema.json").read_text(encoding="utf-8")
    )
    return schema["$defs"]["workers_slice"]


def test_workers_slice_required_fields_unchanged():
    assert sorted(_workers_slice_schema()["required"]) == sorted(WORKERS_REQUIRED)


def test_workers_slice_declares_optional_outcome_fields():
    props = _workers_slice_schema()["properties"]
    outcome = props["session_outcome_by_pid"]
    assert outcome["type"] == "object"
    assert outcome["additionalProperties"]["enum"] == [
        "ok",
        "wall_killed",
        "job_wall_cancelled",
    ]
    assert props["droid_exit_code_by_pid"]["additionalProperties"]["type"] == [
        "integer",
        "null",
    ]
    assert props["stream_tail_marker_by_pid"]["additionalProperties"]["type"] == "boolean"


def test_legacy_wall_without_new_fields_validates(tmp_path: Path):
    wall = init_wall(run_id="f1s1", issue_number=9)
    wall = merge_legacy(wall)
    errs = save_and_validate(wall, tmp_path)
    assert not errs, errs


def merge_legacy(wall: dict) -> dict:
    return apply_deltas(wall, [{"pid": "old", "result": "success"}])


def save_and_validate(wall: dict, tmp_path: Path) -> list[str]:
    path = tmp_path / "foreman-run.json"
    save_wall(wall, path)
    return validate_with_jsonschema(json.loads(path.read_text(encoding="utf-8")))


def test_wall_with_new_outcome_fields_validates(tmp_path: Path):
    wall = init_wall(run_id="f1s2", issue_number=9)
    wall = apply_deltas(
        wall,
        [
            {
                "pid": "hslconv",
                "result": "failure",
                "session_outcome": "wall_killed",
                "droid_exit_code": 124,
                "stream_tail_marker": True,
            }
        ],
    )
    errs = save_and_validate(wall, tmp_path)
    assert not errs, errs


def test_illegal_session_outcome_enum_rejected(tmp_path: Path):
    wall = init_wall(run_id="f1s3", issue_number=9)
    wall["workers"] = {
        **(wall.get("workers") or {}),
        "session_outcome_by_pid": {"hslconv": "timeout"},
    }
    errs = validate_with_jsonschema(wall)
    assert errs, "illegal session_outcome enum value must be rejected"


def test_illegal_droid_exit_code_type_rejected():
    wall = init_wall(run_id="f1s4", issue_number=9)
    wall["workers"] = {
        **(wall.get("workers") or {}),
        "droid_exit_code_by_pid": {"hslconv": "124"},
    }
    assert validate_with_jsonschema(wall), "string exit code must be rejected"


def test_illegal_stream_tail_marker_type_rejected():
    wall = init_wall(run_id="f1s5", issue_number=9)
    wall["workers"] = {
        **(wall.get("workers") or {}),
        "stream_tail_marker_by_pid": {"hslconv": "yes"},
    }
    assert validate_with_jsonschema(wall), "string tail marker must be rejected"


# --- workflow wiring: the delta step must chain session evidence ------------


def test_record_worker_delta_step_stays_always_with_session_inputs():
    chunk = _job_step_chunk("worker", "Record worker delta for ForemanRun (W1 matrix)")
    assert "if: always()" in chunk
    assert "DROID_EXIT_CODE: ${{ steps.session.outputs.exit_code }}" in chunk
    assert "--stream worker-stream.jsonl" in chunk


def test_record_worker_delta_step_cancel_branch_stamps_outcome_not_reason():
    chunk = _job_step_chunk("worker", "Record worker delta for ForemanRun (W1 matrix)")
    # the cancel one-liner now stamps the structured outcome alongside the
    # legacy cancel_reason=job_wall_25m (semantics preserved, outcome added)
    legacy = "d['cancel_reason']='job_wall_25m'"
    assert legacy in chunk
    assert "d['session_outcome']='job_wall_cancelled'" in chunk


def test_worker_session_step_captures_exit_code_as_output():
    chunk = _job_step_chunk("worker", "Worker executes exactly one process card")
    assert "id: session" in chunk
    assert 'echo "exit_code=${DROID_EXIT:-0}" >> "$GITHUB_OUTPUT"' in chunk
    # the session step must keep re-exiting with the session code so the
    # job-level failure conclusion on a wall kill is unchanged
    assert 'exit "${DROID_EXIT:-0}"' in chunk
    assert "set -o pipefail" in chunk
    assert "timeout --signal=TERM --kill-after=30s 900s" in chunk


def test_worker2_session_step_captures_exit_code_as_output():
    chunk = _job_step_chunk("worker2", "Worker executes exactly one process card (round 2)")
    assert "id: session" in chunk
    assert 'echo "exit_code=${DROID_EXIT:-0}" >> "$GITHUB_OUTPUT"' in chunk
    assert 'exit "${DROID_EXIT:-0}"' in chunk


def test_worker2_delta_step_chains_session_inputs():
    chunk = _job_step_chunk("worker2", "Record worker2 delta for ForemanRun")
    assert "if: always()" in chunk
    assert "DROID_EXIT_CODE: ${{ steps.session.outputs.exit_code }}" in chunk
    assert "--stream worker-stream.jsonl" in chunk
