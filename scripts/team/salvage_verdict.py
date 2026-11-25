#!/usr/bin/env python3
"""Incremental per-process verdict persistence (52B fix).

The round-52 B validator analyzed every process, concluded pass x3 inside its
reasoning, and was wall-killed before writing verdict-droid.json — all three
conclusions existed only in reasoning and were lost (the 20th validator
budget-kill death). This module is the write-side of the fix: after analyzing
each process, the validator persists that one conclusion immediately, so a
kill at any moment leaves the already-analyzed verdicts on disk.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PARTIAL_NAME = "verdict-partial.json"


def _valid_entry(entry: dict) -> bool:
    return (
        isinstance(entry, dict)
        and isinstance(entry.get("id"), str)
        and bool(entry["id"])
        and entry.get("verdict") in ("pass", "fail")
    )


def salvage_verdict(
    work_dir: Path,
    *,
    analyzed: dict[str, dict],
    conflicts: list[dict] | None = None,
    round_num: int = 1,
    final: bool = False,
) -> dict:
    """Build the persisted per-process verdict document (one write per analysis).

    `analyzed` maps process id -> {verdict, reason} for processes whose
    analysis has FINISHED. It never includes claims about processes that were
    not analyzed, and the pytest exit is intentionally absent: without the
    merged-suite evidence there is no basis for an overall pass.

    `final` is the D-2 seal: the validator asserts this partial file is its
    deliverable (analysis finished for the processes it covers). Only a
    sealed partial whose coverage equals the judgeable set is adoptable
    (see salvage_assemble.py / adopt_verdict.py).
    """
    entries = []
    for pid, entry in (analyzed or {}).items():
        if not _valid_entry({**entry, "id": pid}):
            raise ValueError(f"invalid verdict entry for {pid!r}: {entry!r}")
        entries.append({"id": pid, "verdict": entry["verdict"], "reason": entry.get("reason", "")})
    entries.sort(key=lambda e: e["id"])
    clean_conflicts = [
        c for c in (conflicts or []) if isinstance(c, dict) and c.get("process") and c.get("summary")
    ]
    return {
        "salvage_schema_version": "validator-partial.v1",
        "round": round_num,
        "final": bool(final),
        "analyzed_count": len(entries),
        "processes": entries,
        "conflicts": clean_conflicts,
    }


def _empty_doc(round_num: int) -> dict:
    return {
        "salvage_schema_version": "validator-partial.v1",
        "round": round_num,
        "final": False,
        "analyzed_count": 0,
        "processes": [],
        "conflicts": [],
    }


def record_verdict(
    work_dir: Path,
    *,
    pid: str,
    verdict: str,
    reason: str = "",
    conflicts: list[dict] | None = None,
    round_num: int = 1,
    final: bool = False,
) -> dict:
    """Persist one process's conclusion immediately after analyzing it (the
    per-process write discipline; idempotent per process within a round).

    `final=True` stamps the D-2 seal. The seal is sticky: a later unsealed
    write (a late recorder call) must not unseal an already-sealed partial.
    """
    doc = salvage_verdict(
        work_dir,
        analyzed={pid: {"verdict": verdict, "reason": reason}},
        conflicts=conflicts,
        round_num=round_num,
        final=final,
    )
    entry = doc["processes"][0]
    path = work_dir / PARTIAL_NAME
    current = _empty_doc(round_num)
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict) and loaded.get("round") == round_num:
                current = loaded
        except Exception:
            pass
    processes = [p for p in (current.get("processes") or []) if p.get("id") != pid]
    processes.append(entry)
    processes.sort(key=lambda e: e["id"])
    conflicts_merged: dict[str, dict] = {
        c.get("process"): c for c in (current.get("conflicts") or [])
    }
    for c in doc["conflicts"]:
        conflicts_merged[c["process"]] = c
    sealed = bool(current.get("final")) or bool(doc.get("final"))
    out = {
        "salvage_schema_version": "validator-partial.v1",
        "round": round_num,
        "final": sealed,
        "analyzed_count": len(processes),
        "processes": processes,
        "conflicts": list(conflicts_merged.values()),
    }
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def read_salvage(work_dir: Path, *, round_num: int = 1) -> dict | None:
    """Load the persisted per-process verdicts, if any survived the session."""
    path = work_dir / PARTIAL_NAME
    if not path.is_file():
        return None
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(doc, dict) or doc.get("salvage_schema_version") != "validator-partial.v1":
        return None
    if doc.get("round") != round_num:
        return None
    entries = [p for p in (doc.get("processes") or []) if _valid_entry(p)]
    if not entries:
        return None
    return {
        "salvage_schema_version": doc["salvage_schema_version"],
        "round": doc["round"],
        "final": bool(doc.get("final")),
        "analyzed_count": len(entries),
        "processes": entries,
        "conflicts": [
            c for c in (doc.get("conflicts") or []) if isinstance(c, dict) and c.get("process")
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Persist one per-process validator verdict")
    p.add_argument("--work-dir", default=".")
    p.add_argument("--process", required=True, help="process id")
    p.add_argument("--verdict", required=True, choices=("pass", "fail"))
    p.add_argument("--reason", default="")
    p.add_argument(
        "--conflict",
        action="append",
        default=[],
        metavar="PROCESS|SUMMARY|EVIDENCE",
        help="escalate one work-order conflict (repeatable); fields separated by |",
    )
    p.add_argument(
        "--final",
        action="store_true",
        help="D-2 seal: this partial is the validator's deliverable "
        "(adoptable only with full judgeable coverage)",
    )
    p.add_argument("--round", type=int, default=1)
    args = p.parse_args()
    conflicts = []
    for raw in args.conflict:
        parts = raw.split("|")
        if len(parts) != 3 or not all(part.strip() for part in parts):
            print(
                f"invalid --conflict {raw!r}: expected PROCESS|SUMMARY|EVIDENCE",
                file=sys.stderr,
            )
            return 2
        conflicts.append(
            {"process": parts[0].strip(), "summary": parts[1].strip(), "evidence": parts[2].strip()}
        )
    out = record_verdict(
        Path(args.work_dir),
        pid=args.process,
        verdict=args.verdict,
        reason=args.reason,
        conflicts=conflicts,
        round_num=args.round,
        final=args.final,
    )
    print(f"recorded {args.process}={args.verdict} (analyzed {out['analyzed_count']} so far)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
