#!/usr/bin/env python3
"""Pick assemble verdict from ForemanRun wall (I2); incomplete artifacts fail-closed (no needs.*_RESULT)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from foreman_run_lib import load_wall


def find_in_dl(dl_dir: Path, dirname_prefix: str, filename: str) -> Path | None:
    if not dl_dir.is_dir():
        return None
    for d in sorted(dl_dir.iterdir()):
        if d.is_dir() and d.name.startswith(dirname_prefix):
            candidate = d / filename
            if candidate.is_file():
                return candidate
    return None


def read_candidate(tar_path: Path) -> str:
    import io
    import tarfile

    try:
        with tarfile.open(tar_path) as tf:
            member = None
            for member_name in ("./manifest.json", "manifest.json"):
                try:
                    member = tf.extractfile(member_name)
                except KeyError:
                    member = None
                if member is not None:
                    break
            if member is None:
                return ""
            manifest = json.load(io.TextIOWrapper(member, encoding="utf-8"))
            return manifest.get("candidate_branch", "") or ""
    except Exception:
        return ""


def pick(
    wall_path: Path,
    dl_dir: Path,
    *,
    issue_number: int,
    run_id: str,
    chain_results: dict[str, str] | None = None,
) -> tuple[dict, str, int, str]:
    """Returns verdict dict, candidate branch, picked_round, verdict_source."""
    if chain_results:
        raise SystemExit("chain_results forbidden when wall is enabled (fail-closed I2)")
    if not wall_path.is_file():
        raise SystemExit("foreman-run.json missing; cannot pick verdict (fail-closed)")

    wall = load_wall(wall_path)
    key1 = f"team-verdict-issue-{issue_number}-run-{run_id}"
    key2 = f"team-verdict2-issue-{issue_number}-run-{run_id}"
    arts = wall.get("artifacts") or {}
    r2_complete = bool(arts.get(key2, {}).get("complete"))
    r1_complete = bool(arts.get(key1, {}).get("complete"))

    picked_round = 1
    val: dict = wall.get("validation") or {}
    if r2_complete:
        picked_round = 2
        val = (wall.get("round2") or {}).get("validation") or val
    elif r1_complete:
        picked_round = 1
    else:
        picked_round = int(val.get("round") or 1)

    verdict_path: Path | None = None
    evidence_tar: Path | None = None
    wall_authoritative = r2_complete or r1_complete

    if wall_authoritative:
        prefix = "team-verdict2-" if picked_round == 2 else "team-verdict-"
        ev_prefix = "team-evidence2-" if picked_round == 2 else "team-evidence-"
        verdict_path = find_in_dl(dl_dir, prefix, "verdict.json")
        evidence_tar = find_in_dl(dl_dir, ev_prefix, "evidence.tar.gz")
        if verdict_path:
            verdict = json.loads(verdict_path.read_text(encoding="utf-8"))
        else:
            verdict = {
                "overall": val.get("overall", "fail"),
                "pytest_exit": val.get("pytest_exit"),
                "iteration": picked_round,
                "processes": [],
                "reason": val.get("adoption_error") or "墙已标记 verdict 完整但工件缺失",
                "unattributed_failure": bool(val.get("unattributed_failure")),
            }
        source = "wall+artifact"
    else:
        art_key = key2 if arts.get(key2) is not None else key1
        entry = arts.get(art_key) or {}
        missing = entry.get("missing") or ["verdict.json"]
        raise SystemExit(
            "wall verdict not authoritative "
            f"(artifacts[{art_key!r}].complete=false); fail-closed without needs.*_RESULT: "
            f"missing={missing}"
        )

    candidate = read_candidate(evidence_tar) if evidence_tar else ""
    if verdict.get("overall") == "pass" and not candidate:
        verdict["overall"] = "fail"
        verdict["reason"] = "判定 pass 但候选分支缺失（证据工件不完整）"

    return verdict, candidate, picked_round, source


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="wall-root/foreman-run.json")
    p.add_argument("--dl", default="dl")
    p.add_argument("--issue", type=int, required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--out", default="final-verdict.json")
    p.add_argument("--github-output", default="")
    args = p.parse_args()

    verdict, candidate, picked_round, source = pick(
        Path(args.wall),
        Path(args.dl),
        issue_number=args.issue,
        run_id=args.run_id,
    )
    Path(args.out).write_text(json.dumps(verdict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"picked round: {picked_round} | source: {source} | overall: {verdict.get('overall')}")
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as out:
            out.write(f"overall={verdict.get('overall')}\n")
            out.write(f"candidate={candidate}\n")
            out.write(f"picked_round={picked_round}\n")
            out.write(f"verdict_source={source}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
