#!/usr/bin/env python3
"""Turn-level budget metrics from droid session streams.

A turn is all assistant-side events sharing one message id. Stream events
are flushed when a turn completes, so a turn's latency runs from the
previous boundary (init / user message / tool_result / end of the previous
turn) to the turn's first event. The final in-flight turn of a killed
session never flushes; its pending span is reported as a right-censored
tail instead of a completed turn.

Char accounting: reasoning text and assistant message text count by their
``text`` length; tool calls count by the JSON length of ``parameters``.
Duplicate stream chunks (same event type, message id and payload length)
are counted once.

Inputs are either a stream artifact path (.jsonl or .log) or a run
directory; a directory input finds ``droid-stream-*-run-*`` artifact dirs
anywhere below it (a corpus root grouped by round works too). Unknown
files are skipped, so pointing the
tool at a mixed run directory never fails.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any

ART_DIR_RE = re.compile(r"^droid-stream-(?P<role>[a-z]+)-run-(?P<run>\w+)$")

_LOG_LINE = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)\.(\d+)Z (.*)$")
_MIN_LOG_LINE = len("1970-01-01T00:00:00.000Z ")


def _log_line_ts(m: re.Match[str]) -> float:
    base = datetime.datetime.strptime(
        m.group(1), "%Y-%m-%dT%H:%M:%S"
    ).replace(tzinfo=datetime.timezone.utc).timestamp()
    return base + float("0." + m.group(2))


def _read_events(path: Path) -> tuple[list[tuple[float, dict[str, Any]]], tuple[float, str] | None]:
    """Parse one stream artifact into (timestamped events, censored tail).

    .jsonl artifacts carry the timestamp inside each event; .log job logs
    echo the same events behind a UTC timestamp prefix, which wins because
    it is the only clock available there.
    """
    events: list[tuple[float, dict[str, Any]]] = []
    tail: tuple[float, str] | None = None
    last_ts: float | None = None
    is_jsonl = path.suffix == ".jsonl"
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        body = raw.strip()
        if not body:
            continue
        line_ts: float | None = None
        if not is_jsonl:
            m = _LOG_LINE.match(body)
            if m is None:
                continue
            line_ts = _log_line_ts(m)
            body = m.group(3)
        if not body.startswith('{"type"'):
            # First non-heartbeat log line after the events stopped is the
            # censored tail (e.g. the timeout error line of a killed job).
            if not is_jsonl and last_ts is not None and tail is None and "heartbeat" not in body:
                tail = (line_ts, body[:90])
            continue
        try:
            event = json.loads(body)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or "type" not in event:
            continue
        # .log echoes are clocked by their line prefix (the only reliable
        # clock there); .jsonl events carry their own ms timestamp and fall
        # back to the previous event's when missing.
        if is_jsonl:
            ts = event.get("timestamp")
            if isinstance(ts, (int, float)):
                last_ts = float(ts) / 1000.0
        else:
            last_ts = line_ts
        if last_ts is None:
            continue
        events.append((last_ts, event))
    return events, tail


def _assistant_content(event: dict[str, Any]) -> tuple[str | None, str]:
    """(turn key, counted text) for an assistant-side event, else (None, "")."""
    etype = event.get("type")
    if etype == "reasoning" or (etype == "message" and event.get("role") == "assistant"):
        return event.get("id"), event.get("text") or ""
    if etype == "tool_call":
        return event.get("messageId"), json.dumps(event.get("parameters"), ensure_ascii=False)
    return None, ""


def _turns(events: list[tuple[float, dict[str, Any]]]) -> list[dict[str, Any]]:
    turns: list[dict[str, Any]] = []
    boundary: float | None = None
    current: dict[str, Any] | None = None
    seen: set[tuple[Any, Any, Any, int]] = set()
    last_event_ts: float | None = None
    for ts, event in events:
        etype = event.get("type")
        if etype == "system" or (etype == "message" and event.get("role") == "user") or etype == "tool_result":
            boundary = ts
            continue
        turn_key, text = _assistant_content(event)
        if turn_key is None:
            continue
        dedup_key = (etype, turn_key, event.get("id"), len(text))
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        if current is None or current["turn_key"] != turn_key:
            anchors = [ts for ts in (boundary, last_event_ts) if ts is not None]
            start = max(anchors) if anchors else None
            current = {
                "turn_key": turn_key,
                "latency_s": (ts - start) if start is not None else None,
                "chars": 0,
                "tools": [],
            }
            turns.append(current)
        current["chars"] += len(text)
        last_event_ts = ts
        if etype == "tool_call":
            current["tools"].append(event.get("toolName"))
    for turn in turns:
        del turn["turn_key"]
    return turns


def measure_events(events: list[tuple[float, dict[str, Any]]], tail: tuple[float, str] | None) -> dict[str, Any]:
    turns = _turns(events)
    for i, turn in enumerate(turns):
        turn["index"] = i
        latency = turn["latency_s"]
        turn["latency_s"] = round(latency, 2) if latency is not None else None
        turn["chars_per_s"] = round(turn["chars"] / latency, 2) if latency and latency > 0 else None
    rates = [t["chars_per_s"] for t in turns if t["chars_per_s"] is not None and (t["latency_s"] or 0) >= 20]
    first = turns[0] if turns else None
    return {
        "n_turns": len(turns),
        "first_response_s": first["latency_s"] if first else None,
        "first_turn_chars": first["chars"] if first else None,
        "total_chars": sum(t["chars"] for t in turns),
        "rate_chars_per_s": {
            "median": round(statistics.median(rates), 2) if rates else None,
            "min": min(rates) if rates else None,
            "max": max(rates) if rates else None,
            "n": len(rates),
        },
        "latency_s": {
            "median": round(statistics.median([t["latency_s"] for t in turns]), 2) if turns else None,
            "max": max((t["latency_s"] for t in turns), default=None),
        },
        "censored_tail_s": round(tail[0] - events[-1][0], 2) if tail and events else None,
        "censored_tail_excerpt": tail[1] if tail else None,
        "turns": turns,
    }


def measure_path(path: Path) -> list[dict[str, Any]]:
    if path.is_dir():
        return measure_dir(path)
    events, tail = _read_events(path)
    role = "lead" if "lead-stream" in path.name else "worker" if "worker" in path.name else "validator" if "validator" in path.name else "unknown"
    run_id = path.parent.name
    m = ART_DIR_RE.match(path.parent.name)
    if m:
        role = m.group("role")
        run_id = m.group("run")
    return [{"source": path.name, "path": str(path), "role": role, "run_id": run_id, **measure_events(events, tail)}]


def _measure_art_dir(run_dir: Path) -> list[dict[str, Any]]:
    m = ART_DIR_RE.match(run_dir.name)
    sources: list[dict[str, Any]] = []
    for stream in sorted(run_dir.glob("*.jsonl")):
        events, tail = _read_events(stream)
        sources.append({
            "source": run_dir.name,
            "path": str(stream),
            "role": m.group("role"),
            "run_id": m.group("run"),
            **measure_events(events, tail),
        })
    return sources


def measure_dir(directory: Path) -> list[dict[str, Any]]:
    if ART_DIR_RE.match(directory.name):
        roots = [directory]
    else:
        # Not itself a run dir: find run dirs anywhere below (evidence
        # corpora group runs by round, e.g. art/50A/droid-stream-lead-run-*).
        roots = [p for p in sorted(directory.rglob("*")) if p.is_dir() and ART_DIR_RE.match(p.name)]
    sources: list[dict[str, Any]] = []
    for run_dir in roots:
        sources.extend(_measure_art_dir(run_dir))
    return sources


def _fmt(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value)


def _print_table(report: dict[str, Any]) -> None:
    header = (
        "source",
        "role",
        "run",
        "turns",
        "first_response",
        "first_chars",
        "total_chars",
        "rate_median",
        "rate_min",
        "rate_max",
        "censored_tail",
    )
    print("\t".join(header))
    for src in report["sources"]:
        row = (
            src["source"],
            src["role"],
            src["run_id"],
            src["n_turns"],
            src["first_response_s"],
            src["first_turn_chars"],
            src["total_chars"],
            src["rate_chars_per_s"]["median"],
            src["rate_chars_per_s"]["min"],
            src["rate_chars_per_s"]["max"],
            src["censored_tail_s"],
        )
        print("\t".join(_fmt(v) for v in row))
    for error in report["errors"]:
        print(f"error: {error}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("inputs", nargs="+", help="stream artifact path (.jsonl/.log) or run directory")
    parser.add_argument("--json", action="store_true", help="emit the full report as JSON")
    args = parser.parse_args(argv)

    sources: list[dict[str, Any]] = []
    errors: list[str] = []
    for raw in args.inputs:
        path = Path(raw)
        if not path.exists():
            errors.append(f"{raw}: no such file or directory")
            continue
        try:
            sources.extend(measure_path(path))
        except OSError as exc:
            errors.append(f"{raw}: {exc}")
    report = {"sources": sources, "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_table(report)
    return 0 if sources else 2


if __name__ == "__main__":
    sys.exit(main())
