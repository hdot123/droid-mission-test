"""Blocked-reason attribution for the validator merge steps (F1b).

The four merge verdict steps (validate / revalidate / validate2 /
revalidate2) used to hardcode one blame-shaped blocked-reason template
（缺件归该工序补齐）for every missing-evidence process. Since the
worker-delta outcome facts ride the wall (session_outcome_by_pid /
droid_exit_code_by_pid, see merge_worker_deltas), a wall-killed worker is
machine-visible: the template must branch on that fact instead of blaming
the worker for files it was killed before writing.

Contract (fail-closed): the neutral attribution is emitted only when the
wall records session_outcome=wall_killed for the pid. Every other shape —
no wall, no record for the pid, session_outcome=ok, legacy wall without
the outcome maps — keeps the current wording byte-for-byte.
"""
from __future__ import annotations

from typing import Any

# The single-point worker-blame suffix, kept only in the no-death branch.
BLAME_SUFFIX = "缺件归该工序补齐"

_LEGACY_PREFIX = "料不齐（没料不验收）：缺 "


def blocked_reason(pid: str, missing: list[str], wall: dict[str, Any] | None = None) -> str:
    """The verdict reason string for a blocked (missing-evidence) process.

    ``wall`` is the ForemanRun wall (its workers slice with the by-pid
    outcome maps, as the merge steps load it) — the single machine-recorded
    death-fact source, never a heuristic on the missing list.

    Wall-killed pid -> neutral attribution carrying the death facts.
    Any other shape  -> the current wording, unchanged (fail-closed).
    """
    base = _LEGACY_PREFIX + ", ".join(missing)
    workers = (wall or {}).get("workers") or {}
    outcome = (workers.get("session_outcome_by_pid") or {}).get(pid)
    if outcome == "wall_killed":
        exit_code = (workers.get("droid_exit_code_by_pid") or {}).get(pid)
        exit_part = f"，droid exit {exit_code}" if exit_code is not None else ""
        tail = (
            "（中性归因：worker 会话被 900s 墙杀、未能在被杀前写出这些证据文件"
            f"（session_outcome={outcome}{exit_part}），"
            "归因以墙上机器记录的死因事实为准，分型交由领班裁定）"
        )
        return f"{base}{tail}"
    return f"{base}（{BLAME_SUFFIX}）"


def blocked_report_line(pid: str, missing: list[str], wall: dict[str, Any] | None = None) -> str:
    """The verdict.md report-line twin of blocked_reason — same branch,
    same tail, so the human-readable report never contradicts the JSON."""
    reason = blocked_reason(pid, missing, wall=wall)
    missing_str = ", ".join(missing)
    prefix = _LEGACY_PREFIX + missing_str + "（"
    tail = reason[len(prefix):] if reason.startswith(prefix) else reason
    return f"- `{pid}`：blocked — 料不齐，缺 {missing_str}（{tail}"


def neutral_attribution(*, pid: str, missing: list[str] | None = None, exit_code: int | None = None) -> str:
    """One machine-fact line for the replan prompt's outcome panel: the
    death fact, what the kill prevented, and the neutral attribution
    instruction — no judge language, the redispatch/revise call stays
    with the foreman."""
    facts = ["session_outcome=wall_killed"]
    if exit_code is not None:
        facts.append(f"droid exit {exit_code}")
    missing_part = f" The pack is still missing: {', '.join(missing)}." if missing else ""
    return (
        f"process `{pid}`: {', '.join(facts)} — the worker session was killed by "
        "the 900s wall before it could write its evidence files." + missing_part +
        " Attribute this neutrally (machine-recorded death, not a worker-compliance failure)."
    )
