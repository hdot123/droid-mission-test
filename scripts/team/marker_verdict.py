"""One marker verdict, shared by every consumer of checks-failed.marker.

The verify step (worker, both rounds) writes the marker whenever its
problems list is non-empty — and missing handoff/status alone makes that
list non-empty even when every card check exits 0 (v2.6.3 semantics). So
the marker's PRESENCE cannot mean "the worker's checks went red": for
exactly the death shape this pipeline exists to cure (machine-green work,
session killed before the two evidence files), the marker records green
checks plus missing-file problems.

Design ruling (M3 scrutiny round-1): the marker is the worker-side verify
record; prep's own checks-exit.json is the green authority. Every consumer
— the salvage guard, the adopt machine gate — classifies the marker by
CONTENT:

- red: any ``check exit <n>`` line with n != 0, any ``problem: status file
  is not valid JSON`` line, or marker bytes that cannot be parsed at all
  (fail-closed: content that cannot prove its entries green reads red);
- not red: problems are only missing-expected-file entries (checks-exit.json
  still gates those packs on its own, and all-0 exits stay green).

The job-level v2.6.3 accounting is unchanged: the trailing step fails the
job whenever the marker FILE exists (existence, not content), so red checks
and missing files alike still fail the worker job. Only the salvage/adopt
consumers read content.
"""
from __future__ import annotations

import re
from typing import Any

MARKER_NAME = "checks-failed.marker"

_PROCESS_RE = re.compile(r"^process: (.+)$")
_CHECK_EXIT_RE = re.compile(r"^check exit (-?\d+): (.*)$")
_MISSING_FILE_RE = re.compile(r"^problem: missing expected file: (.+)$")
_BAD_STATUS_RE = re.compile(r"^problem: status file is not valid JSON: (.*)$")
_PROBLEM_RE = re.compile(r"^problem: (.*)$")


def marker_problems(text: str | None) -> list[dict[str, Any]]:
    """Parse a marker body into typed problem records.

    Each record: ``kind`` (red_check | malformed_status | missing_file |
    unrecognized), plus ``exit``/``command`` for red_check lines and
    ``text`` for the others. Unrecognized ``problem:`` lines kind as
    unrecognized — a marker only exists when verify found problems, so an
    unknown problem is not provably benign.
    """
    problems: list[dict[str, Any]] = []
    if not text:
        return problems
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("process:"):
            continue
        m = _CHECK_EXIT_RE.match(line)
        if m:
            exit_code = int(m.group(1))
            if exit_code != 0:
                problems.append(
                    {"kind": "red_check", "exit": exit_code, "command": m.group(2)}
                )
            continue
        m = _BAD_STATUS_RE.match(line)
        if m:
            problems.append({"kind": "malformed_status", "text": m.group(1)})
            continue
        m = _MISSING_FILE_RE.match(line)
        if m:
            problems.append({"kind": "missing_file", "text": m.group(1)})
            continue
        m = _PROBLEM_RE.match(line)
        if m:
            problems.append({"kind": "unrecognized", "text": m.group(1)})
            continue
        # a non-empty line that is neither a check exit nor a problem line
        problems.append({"kind": "unrecognized", "text": line})
    return problems


def marker_verdict_red(text: str | None) -> bool:
    """True when the marker's content is red: a non-zero check exit, a
    malformed-status problem, any unrecognized problem, or bytes that do
    not parse as marker lines at all. Missing-file-only markers are not red
    (checks-exit.json is the green authority)."""
    if text is None:
        return True
    problems = marker_problems(text)
    if not problems:
        # empty/unparseable bytes prove nothing — red, never a pass-through
        return True
    return any(p["kind"] in ("red_check", "malformed_status", "unrecognized") for p in problems)


def marker_red_detail(text: str | None) -> str:
    """A short human-readable reason fragment naming the first red fact
    (empty when the marker reads green)."""
    if text is None:
        return "marker unreadable (absent bytes)"
    for p in marker_problems(text):
        if p["kind"] == "red_check":
            return f"check exit {p['exit']}: {p['command']}"
        if p["kind"] == "malformed_status":
            return f"status file is not valid JSON: {p['text']}"
        if p["kind"] == "unrecognized":
            return f"unrecognized problem: {p['text']}"
    return ""


def write_marker(process_id: str, check_results: list[tuple[str, int]], problems: list[str]) -> str:
    """The verify step's marker body, v2.6.3 format byte-for-byte:
    ``process:`` header, one ``check exit <n>: <cmd>`` per run check, then
    the ``problem:`` lines. Writer and readers live in this one module so
    the format cannot drift between the step and its consumers."""
    lines = [f"process: {process_id}"]
    for cmd, rc in check_results:
        lines.append(f"check exit {rc}: {cmd}")
    for problem in problems:
        lines.append(f"problem: {problem}")
    return "\n".join(lines) + "\n"
