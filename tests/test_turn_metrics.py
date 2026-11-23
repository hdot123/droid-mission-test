"""Tests for scripts/team/turn_metrics.py (turn-level budget metrics).

Synthetic fixtures pin the reconstruction numbers (chars / latency / rate);
the 50A calibration case replays the real archived lead stream and is
env-gated (TURN_METRICS_50A_STREAM) because CI has no local evidence copy.

Reconstruction caliber (shared with the adversarial-review reference): a
turn is all assistant-side events sharing one message id; latency runs from
the previous boundary (init / user message / tool_result / end of the
previous turn) to the turn's first event; reasoning text and tool-call JSON
both count toward turn characters.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "team"))

import turn_metrics as tm  # noqa: E402


def _jsonl(tmp_path: Path, name: str, events: list[dict]) -> Path:
    path = tmp_path / name
    path.write_text(
        "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in events),
        encoding="utf-8",
    )
    return path


def _sample_events() -> list[dict]:
    """Two turns with known char counts and a tool_result boundary.

    turn 1 (message id m1): latency 10.0s from the user-message boundary,
    chars = 50 reasoning + 20 assistant text + 13 tool-call JSON
    ('{"path": "x"}') = 83.
    turn 2 (message id m2): latency 10.5s from the tool_result boundary
    (1012.0 -> 1022.5), chars = 40.
    """
    return [
        {"type": "system", "subtype": "init"},
        {"type": "message", "role": "user", "id": "u1", "text": "work order", "timestamp": 1_000_000},
        {"type": "reasoning", "id": "m1", "text": "r" * 50, "timestamp": 1_010_000},
        {"type": "message", "role": "assistant", "id": "m1", "text": "a" * 20, "timestamp": 1_010_000},
        {
            "type": "tool_call",
            "id": "c1",
            "messageId": "m1",
            "toolName": "Read",
            "parameters": {"path": "x"},
            "timestamp": 1_010_000,
        },
        {"type": "tool_result", "id": "c1", "messageId": "m2", "value": "ok", "timestamp": 1_012_000},
        {"type": "reasoning", "id": "m2", "text": "s" * 30, "timestamp": 1_022_500},
        {"type": "message", "role": "assistant", "id": "m2", "text": "t" * 10, "timestamp": 1_022_500},
    ]


def test_synthetic_stream_known_metrics(tmp_path: Path):
    path = _jsonl(tmp_path, "lead-stream.jsonl", _sample_events())
    src = tm.measure_path(path)[0]
    assert src["n_turns"] == 2
    assert src["first_response_s"] == pytest.approx(10.0)
    assert src["first_turn_chars"] == 83
    assert src["total_chars"] == 123
    assert [t["latency_s"] for t in src["turns"]] == [10.0, 10.5]
    assert [t["chars"] for t in src["turns"]] == [83, 40]
    assert [t["chars_per_s"] for t in src["turns"]] == [8.3, 3.81]
    assert src["turns"][0]["tools"] == ["Read"]
    assert src["censored_tail_s"] is None


def test_duplicate_events_counted_once(tmp_path: Path):
    # Streamed chunks can land twice (same message id, same payload length):
    # the dedup key must keep chars stable.
    events = _sample_events()
    events.insert(3, {"type": "reasoning", "id": "m1", "text": "r" * 50, "timestamp": 1_010_000})
    path = _jsonl(tmp_path, "lead-stream.jsonl", events)
    src = tm.measure_path(path)[0]
    assert src["first_turn_chars"] == 83
    assert src["n_turns"] == 2


def test_tool_call_chars_are_json_parameters(tmp_path: Path):
    params = {"路径": "卡片"}
    events = [
        {"type": "message", "role": "user", "id": "u1", "text": "wo", "timestamp": 5_000_000},
        {
            "type": "tool_call",
            "id": "c1",
            "messageId": "m1",
            "toolName": "Create",
            "parameters": params,
            "timestamp": 5_005_000,
        },
    ]
    path = _jsonl(tmp_path, "lead-stream.jsonl", events)
    src = tm.measure_path(path)[0]
    assert src["first_turn_chars"] == len(json.dumps(params, ensure_ascii=False))
    assert src["first_response_s"] == pytest.approx(5.0)


def test_boundaries_reset_latency_clock(tmp_path: Path):
    # user message and tool_result both set the boundary; a turn's latency
    # runs from the latest anchor (boundary or previous turn's last event).
    events = [
        {"type": "system", "subtype": "init"},
        {"type": "message", "role": "user", "id": "u1", "text": "wo", "timestamp": 1_000_000},
        {"type": "reasoning", "id": "m1", "text": "x" * 10, "timestamp": 1_004_000},
        {
            "type": "tool_call",
            "id": "c1",
            "messageId": "m1",
            "toolName": "Read",
            "parameters": {},
            "timestamp": 1_004_000,
        },
        {"type": "tool_result", "id": "c1", "value": "ok", "timestamp": 1_050_000},
        {"type": "reasoning", "id": "m2", "text": "y" * 10, "timestamp": 1_060_000},
    ]
    path = _jsonl(tmp_path, "lead-stream.jsonl", events)
    src = tm.measure_path(path)[0]
    assert [t["latency_s"] for t in src["turns"]] == [4.0, 10.0]
    assert [t["chars"] for t in src["turns"]] == [12, 10]


def test_job_log_format_with_censored_tail(tmp_path: Path):
    # Job logs echo stream events behind a timestamp prefix; the in-flight
    # turn of a killed session never flushes and shows up as a tail.
    lines = [
        "2026-11-22T10:00:00.000Z preamble before any event is ignored",
        "2026-11-22T10:00:00.000Z " + json.dumps({"type": "message", "role": "user", "id": "u1", "text": "wo", "timestamp": 1_000}),
        "2026-11-22T10:00:10.000Z " + json.dumps({"type": "reasoning", "id": "m1", "text": "r" * 50, "timestamp": 1_010}),
        "2026-11-22T10:00:10.000Z " + json.dumps({"type": "message", "role": "assistant", "id": "m1", "text": "a" * 20, "timestamp": 1_010}),
        "2026-11-22T10:00:11.000Z heartbeat: still alive",
        "2026-11-22T10:00:22.500Z " + json.dumps({"type": "reasoning", "id": "m2", "text": "s" * 30, "timestamp": 1_022}),
        "2026-11-22T10:00:22.500Z " + json.dumps({"type": "message", "role": "assistant", "id": "m2", "text": "t" * 10, "timestamp": 1_022}),
        "2026-11-22T10:00:30.000Z ##[error]Process completed with exit code 124.",
    ]
    path = tmp_path / "45X-lead-1.log"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    src = tm.measure_path(path)[0]
    assert src["n_turns"] == 2
    assert [t["latency_s"] for t in src["turns"]] == [10.0, 12.5]
    assert [t["chars"] for t in src["turns"]] == [70, 40]
    assert src["censored_tail_s"] == pytest.approx(7.5)
    assert src["censored_tail_excerpt"] == "##[error]Process completed with exit code 124."


def test_run_directory_discovery(tmp_path: Path):
    lead_dir = tmp_path / "droid-stream-lead-run-111"
    lead_dir.mkdir()
    _jsonl(lead_dir, "lead-stream.jsonl", _sample_events())
    val_dir = tmp_path / "droid-stream-validator-run-222"
    val_dir.mkdir()
    _jsonl(val_dir, "validator-stream.jsonl", _sample_events())
    foreman_dir = tmp_path / "foreman-run-111"
    foreman_dir.mkdir()
    (foreman_dir / "foreman-run.json").write_text("{}", encoding="utf-8")

    sources = tm.measure_dir(tmp_path)
    assert [s["source"] for s in sources] == [
        "droid-stream-lead-run-111",
        "droid-stream-validator-run-222",
    ]
    assert sources[0]["role"] == "lead"
    assert sources[0]["run_id"] == "111"
    assert sources[1]["role"] == "validator"
    assert sources[1]["run_id"] == "222"

    assert tm.measure_dir(tmp_path / "foreman-run-111") == []


def test_measure_dir_corpus_root(tmp_path: Path):
    # A corpus root (one folder per round) measures every run dir under it.
    round_a = tmp_path / "50A"
    round_a.mkdir()
    lead_dir = round_a / "droid-stream-lead-run-111"
    lead_dir.mkdir()
    _jsonl(lead_dir, "lead-stream.jsonl", _sample_events())
    round_b = tmp_path / "50B"
    round_b.mkdir()
    val_dir = round_b / "droid-stream-validator-run-222"
    val_dir.mkdir()
    _jsonl(val_dir, "validator-stream.jsonl", _sample_events())

    sources = tm.measure_dir(tmp_path)
    assert [s["source"] for s in sources] == [
        "droid-stream-lead-run-111",
        "droid-stream-validator-run-222",
    ]


def test_log_file_named_as_artifact(tmp_path: Path):
    # Job logs staged under a round folder carry the artifact naming on the
    # file itself; role and run id must come from the file name, not the dir.
    round_dir = tmp_path / "48A"
    round_dir.mkdir()
    log = round_dir / "droid-stream-lead-run-44555700638.log"
    line = lambda ts: f"2025-01-01T00:00:{ts:02d}.000Z " + json.dumps(_sample_events()[0])
    log.write_text("\n".join(line(i) for i in range(4)), encoding="utf-8")
    src = tm.measure_path(log)[0]
    assert src["role"] == "lead"
    assert src["run_id"] == "44555700638"


def test_worker2_role_token(tmp_path: Path):
    # Second-round worker seats are worker2/worker3: the role token in the
    # artifact name is alphanumeric, not purely alphabetic.
    round_dir = tmp_path / "45A"
    round_dir.mkdir()
    log = round_dir / "droid-stream-worker2-run-44428440695.log"
    line = lambda ts: f"2025-01-01T00:00:{ts:02d}.000Z " + json.dumps(_sample_events()[0])
    log.write_text("\n".join(line(i) for i in range(4)), encoding="utf-8")
    src = tm.measure_path(log)[0]
    assert src["role"] == "worker2"
    assert src["run_id"] == "44428440695"


def test_worker_role_with_module_name(tmp_path: Path):
    # Worker artifact dirs embed the card module in the role token
    # (droid-stream-worker-eliasgamma-run-N); run id stays the numeric tail.
    round_dir = tmp_path / "50B"
    round_dir.mkdir()
    (round_dir / "droid-stream-worker-eliasgamma-run-44692482847").mkdir()
    _jsonl(round_dir / "droid-stream-worker-eliasgamma-run-44692482847",
           "worker-stream.jsonl", _sample_events())
    src = tm.measure_dir(tmp_path)[0]
    assert src["role"] == "worker-eliasgamma"
    assert src["run_id"] == "44692482847"


def test_cli_json_output(tmp_path: Path, capsys):
    path = _jsonl(tmp_path, "lead-stream.jsonl", _sample_events())
    assert tm.main([str(path), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["errors"] == []
    assert out["sources"][0]["first_turn_chars"] == 83


def test_cli_table_output_and_missing_input(tmp_path: Path, capsys):
    path = _jsonl(tmp_path, "lead-stream.jsonl", _sample_events())
    assert tm.main([str(path)]) == 0
    assert "first_response" in capsys.readouterr().out
    assert tm.main([str(tmp_path / "nope.jsonl")]) == 2


def test_jsonl_stream_with_job_log_aligned_tail(tmp_path: Path):
    # A .jsonl stream artifact never carries the censored tail itself (the
    # in-flight turn never flushes); paired with the seat's job log, the
    # session-end echo ("foreman droid session:", printed by the wrapper
    # after the session dies) minus the stream's last event timestamp
    # recovers the pending span (52B calibration shape).
    def ts(stamp: str) -> int:
        import datetime

        dt = datetime.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
            tzinfo=datetime.timezone.utc
        )
        return int(dt.timestamp() * 1000)

    events = [
        {"type": "system", "subtype": "init", "timestamp": ts("2026-11-22T10:00:01.000Z")},
        {"type": "message", "role": "user", "id": "u1", "text": "wo", "timestamp": ts("2026-11-22T10:00:02.000Z")},
        {"type": "reasoning", "id": "m1", "text": "r" * 50, "timestamp": ts("2026-11-22T10:00:10.000Z")},
        {
            "type": "tool_call",
            "id": "c1",
            "messageId": "m1",
            "toolName": "Execute",
            "parameters": {"cmd": "x"},
            "timestamp": ts("2026-11-22T10:00:10.000Z"),
        },
        {"type": "tool_result", "id": "c1", "timestamp": ts("2026-11-22T10:00:10.500Z")},
    ]
    stream = _jsonl(tmp_path, "validator-stream.jsonl", events)
    log = tmp_path / "2X-validator-job.log"
    log.write_text(
        "\n".join(
            [
                "2026-11-22T10:00:01.000Z validator session budget (wall): droid=480s adopt_reserve=120s (I8-A/D may override droid wall only)",
                "2026-11-22T10:00:25.000Z foreman droid session: role=validator wall_droid_sec=480 cmd=timeout --signal=TERM --kill-after=30s 480s …",
                "2026-11-22T10:00:25.100Z ##[error]Process completed with exit code 124.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    src = tm.measure_path(stream, job_logs=[log])[0]
    # stream last event 10:00:10.500 -> session end echo 10:00:25.000
    assert src["censored_tail_s"] == pytest.approx(14.5)
    assert src["censored_tail_method"] == "session_log_alignment"
    assert src["censored_tail_excerpt"].startswith("foreman droid session:")
    assert src["censored_tail_source"] == "2X-validator-job.log"


def test_log_alignment_requires_budget_anchor(tmp_path: Path):
    # Guard against pairing with an unrelated log: the session-end echo only
    # counts when the same log shows the session budget echo EARLIER (the
    # session actually started there) and ends after the stream's last event.
    def ts(stamp: str) -> int:
        import datetime

        dt = datetime.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
            tzinfo=datetime.timezone.utc
        )
        return int(dt.timestamp() * 1000)

    events = [
        {"type": "message", "role": "user", "id": "u1", "text": "wo", "timestamp": ts("2026-11-22T10:00:02.000Z")},
        {"type": "reasoning", "id": "m1", "text": "r" * 50, "timestamp": ts("2026-11-22T10:00:20.000Z")},
    ]
    stream = _jsonl(tmp_path, "validator-stream.jsonl", events)
    # no budget echo line at all -> not this seat's job log
    log = tmp_path / "other-job.log"
    log.write_text(
        "2026-11-22T10:01:00.000Z foreman droid session: role=lead wall_droid_sec=600 cmd=timeout …\n",
        encoding="utf-8",
    )
    src = tm.measure_path(stream, job_logs=[log])[0]
    assert src["censored_tail_s"] is None
    assert src["censored_tail_method"] is None
    # budget echo AFTER the session echo -> nonsense ordering, rejected
    log2 = tmp_path / "inverted-job.log"
    log2.write_text(
        "\n".join(
            [
                "2026-11-22T10:01:00.000Z foreman droid session: role=validator wall_droid_sec=480 cmd=timeout …",
                "2026-11-22T10:02:00.000Z validator session budget (wall): droid=480s adopt_reserve=120s (I8-A/D may override droid wall only)",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    src2 = tm.measure_path(stream, job_logs=[log2])[0]
    assert src2["censored_tail_s"] is None


def test_52b_censored_tail_calibration():
    """VAL-M3-006: the killed 52B validator session's censored tail must be
    measurable from the artifact stream paired with its job log; the
    calibrated value is 143-144s (event alignment, verify-b-death)."""
    root = os.environ.get("TURN_METRICS_52B_EVIDENCE", "")
    if not root:
        pytest.skip("set TURN_METRICS_52B_EVIDENCE to the round52-verify bdeath evidence root to run calibration")
    root = Path(root)
    stream = root / "52B" / "droid-stream-validator-run-45078468896" / "validator-stream.jsonl"
    log = root / "logs" / "52B-validator-job.log"
    if not stream.exists() or not log.exists():
        pytest.skip("TURN_METRICS_52B_EVIDENCE is missing the 52B stream or validator job log")
    src = tm.measure_path(stream, job_logs=[log])[0]
    assert src["role"] == "validator"
    assert src["censored_tail_s"] == pytest.approx(144.05, abs=2.0)
    assert src["censored_tail_method"] == "session_log_alignment"


@pytest.mark.skipif(
    not os.environ.get("TURN_METRICS_50A_STREAM"),
    reason="set TURN_METRICS_50A_STREAM to the archived 50A lead stream to run calibration",
)
def test_50a_calibration():
    stream = Path(os.environ["TURN_METRICS_50A_STREAM"])
    if not stream.exists():
        pytest.skip("TURN_METRICS_50A_STREAM points at a missing file")
    src = tm.measure_path(stream)[0]
    # Adversarial-review reference values for the 50A lead stream:
    # first response 539.8s; first turn ~59,686 reasoning chars (60,265
    # total once assistant text and tool-call JSON are included, +0.97%).
    assert src["n_turns"] == 3
    assert src["first_response_s"] == pytest.approx(539.8, abs=0.5)
    assert src["first_turn_chars"] == pytest.approx(59_686, rel=0.05)
    assert src["rate_chars_per_s"]["median"] == pytest.approx(111.7, abs=1.0)
    assert src["role"] == "lead"
