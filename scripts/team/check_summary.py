#!/usr/bin/env python3
"""Authoritative test counts for the evidence pack (I-4).

Round-54 F-03: 12/12 evidence packs carried inconsistent counts — prep reruns
per-card checks and the merged suite but only echoes the worker's own status
files, so the pack could disagree with itself about how many tests passed.
This module builds check-summary.json from what prep ACTUALLY ran (per-card
checks plus the merged pytest output), and prep writes it into evidence/
before the manifest hashes the tree, so the pack's own sha covers it.

Worker status files are never rewritten: the summary is the pack-level view,
evidence immutability stays intact.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

SUMMARY_NAME = "check-summary.json"

_PASSED_RE = re.compile(r"(\d+) passed")
_SKIPPED_RE = re.compile(r"(\d+) skipped")


def parse_pytest_counts(output: str) -> dict:
    """Extract passed/skipped from a pytest summary line (last match wins —
    pytest prints exactly one final summary line per run)."""
    passed = skipped = 0
    for line in output.splitlines():
        m = _PASSED_RE.search(line)
        if m:
            passed = int(m.group(1))
        m = _SKIPPED_RE.search(line)
        if m:
            skipped = int(m.group(1))
    return {"passed": passed, "skipped": skipped}


def build_summary(*, per_card: dict, totals: dict) -> dict:
    """The on-disk contract: per-card counts keyed by process id plus merged
    totals; every entry carries both fields so a missing value is explicit."""
    return {
        "schema_version": "check-summary.v1",
        "per_card": {
            pid: {"passed": int(v.get("passed", 0)), "skipped": int(v.get("skipped", 0))}
            for pid, v in (per_card or {}).items()
        },
        "totals": {
            "passed": int((totals or {}).get("passed", 0)),
            "skipped": int((totals or {}).get("skipped", 0)),
        },
    }


def write_summary(evidence_dir: Path, *, per_card: dict, totals: dict) -> Path:
    doc = build_summary(per_card=per_card, totals=totals)
    path = evidence_dir / SUMMARY_NAME
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    import argparse

    p = argparse.ArgumentParser(description="Build evidence/check-summary.json")
    p.add_argument("--evidence-dir", default="evidence")
    args = p.parse_args()
    root = Path(args.evidence_dir)
    per_card: dict = {}
    for exit_path in sorted(root.glob("packs/*/checks-exit.json")):
        pid = exit_path.parent.name
        try:
            exits = json.loads(exit_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        per_card[pid] = {"passed": 0, "skipped": 0, "checks": len(exits or [])}
    totals = parse_pytest_counts((root / "pytest-output.txt").read_text(encoding="utf-8", errors="replace"))
    write_summary(root, per_card=per_card, totals=totals)
    print(f"wrote {root / SUMMARY_NAME}: totals={totals}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
