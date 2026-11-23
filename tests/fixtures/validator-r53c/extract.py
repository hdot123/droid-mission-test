#!/usr/bin/env python3
"""Extract 53C-type round-2 fixtures from archived round-53 artifacts (read-only source).

Produces tests/fixtures/validator-r53c/{plan.json,manifest.json}:
- both files come from the real run-C round-2 evidence pack verbatim;
- manifest.json is the load-bearing piece: every pack carries
  branch_present=false (F-1 rejected all 12 worker sessions before their
  branch push, so handoff/status/diff could never exist), which is the
  factual ground this feature's replan-context fix must speak from.

Run: python3 tests/fixtures/validator-r53c/extract.py [evidence_root]
Default evidence_root: /Users/busiji/droid-mission-test/adversarial/round53-verify
"""
from __future__ import annotations

import json
import sys
import tarfile
from pathlib import Path

RUN_ID = "45125143118"
PIDS = ["ascii85", "nthweekday", "substitution"]
EVIDENCE_MEMBER = f"team-evidence-issue-792-run-{RUN_ID}/evidence.tar.gz"
EVIDENCE2_MEMBER = f"team-evidence2-issue-792-run-{RUN_ID}/evidence.tar.gz"
OUT_DIR = Path(__file__).resolve().parent


def main() -> int:
    evidence_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "/Users/busiji/droid-mission-test/adversarial/round53-verify"
    )
    tar1_src = evidence_root / "runC" / EVIDENCE_MEMBER
    tar2_src = evidence_root / "runC" / EVIDENCE2_MEMBER
    for p in (tar1_src, tar2_src):
        if not p.is_file():
            print(f"missing source: {p}", file=sys.stderr)
            return 1

    # The replan job unpacks the ROUND-1 evidence tar (stage/manifest.json),
    # so the prompt-context extraction proves against the round-1 manifest.
    with tarfile.open(tar1_src, "r:gz") as tf:
        manifest1 = json.load(tf.extractfile("manifest.json"))
    with tarfile.open(tar2_src, "r:gz") as tf:
        plan = json.load(tf.extractfile("plan.json"))
        manifest2 = json.load(tf.extractfile("manifest.json"))

    assert manifest1["run_id"] == RUN_ID and manifest1["iteration"] == 1
    assert manifest2["run_id"] == RUN_ID and manifest2["iteration"] == 2
    for manifest in (manifest1, manifest2):
        assert sorted(manifest["packs"]) == PIDS
        for pid, info in manifest["packs"].items():
            assert info["branch_present"] is False, (pid, info)
            assert info["merged"] is False, (pid, info)
            assert info["complete"] is False, (pid, info)
    assert [p["id"] for p in plan["processes"]] == PIDS
    assert plan.get("plan_version") == 2

    (OUT_DIR / "manifest-r1.json").write_text(
        json.dumps(manifest1, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "plan.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "provenance.txt").write_text(
        "source: adversarial round53-verify evidence (read-only), "
        f"run C {RUN_ID}, issue #792\n"
        "manifest-r1.json: evidence (round-1 packs, the tar the replan job "
        "unpacks into stage/) verbatim\n"
        "plan.json: evidence2 (round-2 effective plan, plan_version=2) verbatim\n"
        "manifest.json: evidence2 (round-2 packs; all three branch_present=false "
        "— F-1 rejected before branch push) verbatim\n",
        encoding="utf-8",
    )
    print(f"fixtures written to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
