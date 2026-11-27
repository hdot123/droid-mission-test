#!/usr/bin/env python3
"""Merge matrix worker deltas into ForemanRun workers slice (W1, no last-write)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from foreman_run_lib import load_wall, merge_worker_slice, save_wall


def load_deltas(delta_dir: Path) -> list[dict]:
    deltas: list[dict] = []
    if not delta_dir.is_dir():
        return deltas
    for path in sorted(delta_dir.rglob("worker-delta.json")):
        try:
            deltas.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception as exc:
            print(f"skip bad delta {path}: {exc}", file=sys.stderr)
    for path in sorted(delta_dir.glob("*.json")):
        if path.name == "foreman-run.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if "pid" in data and "result" in data:
                deltas.append(data)
        except Exception:
            pass
    # Dedupe by pid (last delta wins per pid — same pid should not run twice)
    by_pid: dict[str, dict] = {}
    for d in deltas:
        pid = d.get("pid")
        if pid:
            by_pid[pid] = d
    return [by_pid[k] for k in sorted(by_pid)]


# F1 session-outcome delta fields -> workers-slice by-pid maps they ride on.
# Optional, backward-compatible: legacy deltas (pid+result only) leave all
# three maps untouched, so pre-F1 walls keep validating unchanged.
OUTCOME_FIELDS = (
    ("session_outcome", "session_outcome_by_pid"),
    ("droid_exit_code", "droid_exit_code_by_pid"),
    ("stream_tail_marker", "stream_tail_marker_by_pid"),
)


def apply_deltas(wall: dict, deltas: list[dict], *, round_tag: str = "") -> dict:
    delta_pids: list[str] = []
    for d in deltas:
        wall = merge_worker_slice(wall, d["pid"], d["result"])
        if d["pid"] not in delta_pids:
            delta_pids.append(d["pid"])
        reasons = (wall.get("workers") or {}).get("cancel_reason_by_pid") or {}
        if d.get("cancel_reason"):
            reasons[d["pid"]] = d["cancel_reason"]
            wall.setdefault("workers", {})["cancel_reason_by_pid"] = reasons
        workers = wall.setdefault("workers", {})
        for field, by_pid_key in OUTCOME_FIELDS:
            if field not in d:
                continue
            by_pid = dict(workers.get(by_pid_key) or {})
            by_pid[d["pid"]] = d[field]
            workers[by_pid_key] = by_pid
    if round_tag == "2":
        # The round-2 workers snapshot must be readable as "what round 2
        # itself observed": the top-level maps are cumulative last-write-wins
        # across rounds, so a round-1 wall_killed survives in them when a
        # worker2 dies before its delta step and would wrongly authorize a
        # round-2 salvage on stale facts (scrutiny NC-5). delta_pids records
        # which pids round 2 actually heard from.
        wall = {
            **wall,
            "round2": {
                **(wall.get("round2") or {}),
                "workers": wall.get("workers"),
                "delta_pids": delta_pids,
            },
        }
    return wall


def round2_salvage_wall(wall: dict | None) -> dict:
    """The workers slice the ROUND-2 salvage must judge on (fail-closed).

    Round 2 saw exactly the pids in round2.delta_pids; the snapshot is
    restricted to them. A pid with no round-2 delta falls out entirely —
    its round-1 death facts stay round-1 history and never authorize a
    round-2 salvage. No snapshot / no delta_pids at all (the round-2 merge
    never ran) -> an empty slice, never the round-1 top-level maps.
    """
    round2 = (wall or {}).get("round2") or {}
    workers = round2.get("workers")
    if not isinstance(workers, dict):
        return {}
    delta_pids = round2.get("delta_pids")
    if not isinstance(delta_pids, list) or not delta_pids:
        return {}
    slice_out = dict(workers)
    for key, value in list(slice_out.items()):
        if key.endswith("_by_pid") and isinstance(value, dict):
            slice_out[key] = {pid: v for pid, v in value.items() if pid in delta_pids}
    return slice_out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--delta-dir", default="deltas")
    p.add_argument("--round", type=int, default=1)
    args = p.parse_args()
    wall_path = Path(args.wall)
    if not wall_path.exists():
        print(f"missing wall: {wall_path}", file=sys.stderr)
        return 1
    wall = load_wall(wall_path)
    deltas = load_deltas(Path(args.delta_dir))
    if not deltas:
        print("no worker deltas found; workers slice unchanged")
        save_wall(wall, wall_path)
        return 0
    wall = apply_deltas(wall, deltas, round_tag=str(args.round) if args.round == 2 else "")
    save_wall(wall, wall_path)
    print(f"merged {len(deltas)} worker deltas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())