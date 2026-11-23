#!/usr/bin/env python3
"""Extract 52B-type validator fixtures from archived round-52 artifacts (read-only source).

Produces tests/fixtures/validator-r52b/{plan.json,manifest.json,analysis-dijkstra.md,...}:
- plan/manifest come from the real run's evidence pack;
- per-process analysis files are split out of the real validator stream's final
  reasoning turn (the turn that concluded pass x3 but died before writing files).

Run: python3 tests/fixtures/validator-r52b/extract.py [evidence_root]
Default evidence_root: /Users/busiji/droid-mission-test/adversarial/round52-verify/evidence
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RUN_ID = "45078468896"
PIDS = ["dijkstra", "nthprime", "windscale"]
# Char offsets of each process's analysis block inside the final reasoning turn.
SECTION_BOUNDS = {
    "dijkstra": (319, 7469),
    "nthprime": (7469, 8118),
    "windscale": (8118, 19353),
}
VERDICT_SENTENCE = (
    "Therefore:\n"
    "- verdicts: dijkstra pass, nthprime pass, windscale pass.\n"
    "- conflicts: []."
)
OUT_DIR = Path(__file__).resolve().parent


def main() -> int:
    evidence_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "/Users/busiji/droid-mission-test/adversarial/round52-verify/evidence"
    )
    plan_src = evidence_root / "bdeath" / "52B" / f"evidence-unpacked" / "plan.json"
    manifest_src = evidence_root / "bdeath" / "52B" / "evidence-unpacked" / "manifest.json"
    stream_src = (
        evidence_root
        / "bdeath"
        / "52B"
        / f"droid-stream-validator-run-{RUN_ID}"
        / "validator-stream.jsonl"
    )
    for p in (plan_src, manifest_src, stream_src):
        if not p.is_file():
            print(f"missing source: {p}", file=sys.stderr)
            return 1

    plan = json.loads(plan_src.read_text(encoding="utf-8"))
    assert [pr["id"] for pr in plan["processes"]] == PIDS
    manifest = json.loads(manifest_src.read_text(encoding="utf-8"))
    assert set(manifest["packs"]) == set(PIDS)

    events = [json.loads(line) for line in stream_src.read_text(encoding="utf-8").splitlines()]
    reasoning = [e for e in events if e.get("type") == "reasoning" and e.get("text")]
    final = reasoning[-1]["text"]
    assert VERDICT_SENTENCE in final, "verdict sentence not found in final reasoning turn"
    for pid, (start, end) in SECTION_BOUNDS.items():
        (OUT_DIR / f"analysis-{pid}.md").write_text(final[start:end], encoding="utf-8")
    (OUT_DIR / "plan.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "provenance.txt").write_text(
        "source: adversarial round52-verify evidence (read-only), run 45078468896\n"
        "validator stream final reasoning turn split at fixed char offsets\n"
        f"verdict sentence present: {VERDICT_SENTENCE.splitlines()[1]}\n",
        encoding="utf-8",
    )
    print(f"fixtures written to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
