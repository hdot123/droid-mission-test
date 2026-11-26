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
    for d in deltas:
        wall = merge_worker_slice(wall, d["pid"], d["result"])
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
        wall = {**wall, "round2": {**(wall.get("round2") or {}), "workers": wall.get("workers")}}
    return wall


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