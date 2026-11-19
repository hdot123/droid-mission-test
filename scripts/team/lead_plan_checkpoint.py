#!/usr/bin/env python3
"""Incrementally recover team-plan.json from lead stream-json checkpoints (batch-3)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CHECKPOINT_PATH = Path("team/lead-plan-checkpoint.json")
PLAN_PATH = Path("team-plan.json")


def _extract_json_objects(text: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(r"\{[\s\S]*?\}", text):
        chunk = m.group(0)
        try:
            obj = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and ("processes" in obj or "summary" in obj):
            out.append(obj)
    return out


def scan_stream(stream_path: Path) -> dict | None:
    if not stream_path.is_file():
        return None
    best: dict | None = None
    best_score = -1
    for line in stream_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            for obj in _extract_json_objects(line):
                score = len(obj.get("processes") or [])
                if score > best_score:
                    best, best_score = obj, score
            continue
        if isinstance(event, dict):
            for key in ("content", "text", "message", "delta"):
                val = event.get(key)
                if isinstance(val, str):
                    try:
                        inner = json.loads(val)
                        if isinstance(inner, dict) and (
                            "processes" in inner or "summary" in inner
                        ):
                            score = len(inner.get("processes") or [])
                            if score > best_score:
                                best, best_score = inner, score
                    except json.JSONDecodeError:
                        pass
        blob = json.dumps(event, ensure_ascii=False)
        for obj in _extract_json_objects(blob):
            score = len(obj.get("processes") or [])
            if score > best_score:
                best, best_score = obj, score
    return best


def write_checkpoint(plan: dict) -> None:
    CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "lead-plan-checkpoint.v1",
        "partial": True,
        "summary": plan.get("summary", ""),
        "processes": plan.get("processes") or [],
    }
    CHECKPOINT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def recover(*, stream_path: Path, promote: bool) -> int:
    plan = scan_stream(stream_path)
    if plan is None:
        print("lead checkpoint: no plan fragment in stream yet")
        return 0
    write_checkpoint(plan)
    print(
        "lead checkpoint:",
        f"processes={len(plan.get('processes') or [])}",
        f"path={CHECKPOINT_PATH}",
    )
    if promote and not PLAN_PATH.is_file():
        full = {
            "summary": plan.get("summary") or "（由检查点恢复）",
            "processes": plan.get("processes") or [],
        }
        if not full["processes"]:
            print("lead recover: checkpoint has no processes; not promoting")
            return 0
        PLAN_PATH.write_text(
            json.dumps(full, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print("lead recover: promoted checkpoint -> team-plan.json")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--stream", default="lead-stream.jsonl")
    p.add_argument("--promote", action="store_true")
    args = p.parse_args()
    return recover(stream_path=Path(args.stream), promote=args.promote)


if __name__ == "__main__":
    raise SystemExit(main())