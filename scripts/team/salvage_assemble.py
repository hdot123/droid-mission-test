#!/usr/bin/env python3
"""Machine-assemble the validator draft from the persisted partial (I-6).

The one helper both adoption surfaces share — adopt_verdict.py and the inline
merge steps in team.yml. A verdict-partial.json is adoptable only when ALL of:
  - the D-2 seal is present (``final: true``, stamped by the validator with
    the recorder's --final flag);
  - its entries cover EXACTLY the judgeable set (no more, no fewer);
  - every entry's verdict is pass|fail with a string id.
Any other shape returns None and the caller falls back to the revalidate
path (VAL-P1-002) — never a guessy adoption.

This replaces the M3-era contract ("recovery never upgrades the verdict",
overturned by U-3): artifact completeness on disk now outranks the session
exit code, while the pytest_exit / conflicts machine gates stay exactly where
they were — the assembled draft enters the SAME gate path a live draft would.
"""
from __future__ import annotations

import json
from pathlib import Path

PARTIAL_NAME = "verdict-partial.json"


def _valid_entry(entry: dict) -> bool:
    return (
        isinstance(entry, dict)
        and isinstance(entry.get("id"), str)
        and bool(entry["id"])
        and entry.get("verdict") in ("pass", "fail")
    )


def assemble_assembled_draft(work_dir: Path, judgeable: list[str]) -> dict | None:
    """Return a verdict-droid.json-shaped draft assembled from the partial,
    or None when the partial does not meet the adoptable bar."""
    path = work_dir / PARTIAL_NAME
    if not judgeable or not path.is_file():
        return None
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(doc, dict) or doc.get("salvage_schema_version") != "validator-partial.v1":
        return None
    if not doc.get("final"):
        return None
    entries = [p for p in (doc.get("processes") or []) if _valid_entry(p)]
    if sorted(e["id"] for e in entries) != sorted(judgeable):
        return None
    conflicts = [
        c
        for c in (doc.get("conflicts") or [])
        if isinstance(c, dict) and c.get("process") and c.get("summary")
    ]
    return {
        "processes": [
            {"id": e["id"], "verdict": e["verdict"], "reason": e.get("reason", "")}
            for e in entries
        ],
        "conflicts": conflicts,
    }
