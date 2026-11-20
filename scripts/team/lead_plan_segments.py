#!/usr/bin/env python3
"""Lead plan segmented persistence (batch-B / B2): one file per segment, no stream salvage."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from foreman_run_lib import deep_merge, load_wall, save_wall

SEGMENTS_DIR = Path("team/lead-plan-segments")
PLAN_PATH = Path("team-plan.json")
HEADER_BASENAME = "00-header.json"
PROCESS_PREFIX = "process-"
SEGMENT_SCHEMA = "lead-plan-segment.v1"
PLAN_SLICE_SCHEMA = "lead-plan-slice.v1"

PlanOutputShape = Literal["none", "partial", "complete"]


@dataclass(frozen=True)
class SegmentScan:
    shape: PlanOutputShape
    segment_files: tuple[str, ...]
    header: dict[str, Any] | None
    processes: tuple[dict[str, Any], ...]
    errors: tuple[str, ...]


def _is_process_filename(name: str) -> bool:
    if not name.startswith(PROCESS_PREFIX) or not name.endswith(".json"):
        return False
    pid = name[len(PROCESS_PREFIX) : -len(".json")]
    return bool(re.fullmatch(r"^[a-z0-9][a-z0-9-]*$", pid))


def _read_segment(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"{path.name}: invalid json ({exc})"
    if not isinstance(raw, dict):
        return None, f"{path.name}: segment must be a JSON object"
    if raw.get("schema_version") != SEGMENT_SCHEMA:
        return None, f"{path.name}: schema_version must be {SEGMENT_SCHEMA}"
    kind = raw.get("kind")
    if kind not in ("header", "process"):
        return None, f"{path.name}: kind must be header|process"
    return raw, None


def scan_segments(*, segments_dir: Path = SEGMENTS_DIR) -> SegmentScan:
    errors: list[str] = []
    if not segments_dir.is_dir():
        if PLAN_PATH.is_file():
            return SegmentScan("complete", (), None, (), ())
        return SegmentScan("none", (), None, (), ())

    names = sorted(p.name for p in segments_dir.iterdir() if p.is_file() and p.suffix == ".json")
    if not names:
        if PLAN_PATH.is_file():
            return SegmentScan("complete", (), None, (), ())
        return SegmentScan("none", (), None, (), ())

    header: dict[str, Any] | None = None
    processes: list[dict[str, Any]] = []
    for name in names:
        if name == HEADER_BASENAME:
            if header is not None:
                errors.append(f"duplicate {HEADER_BASENAME}")
            obj, err = _read_segment(segments_dir / name)
            if err:
                errors.append(err)
            elif (obj or {}).get("kind") != "header":
                errors.append(f"{name}: expected kind header")
            else:
                header = obj
            continue
        if not _is_process_filename(name):
            errors.append(f"{name}: unsupported segment filename")
            continue
        obj, err = _read_segment(segments_dir / name)
        if err:
            errors.append(err)
            continue
        if obj is None or obj.get("kind") != "process":
            errors.append(f"{name}: expected kind process")
            continue
        proc = obj.get("process")
        if not isinstance(proc, dict):
            errors.append(f"{name}: missing process object")
            continue
        pid = name[len(PROCESS_PREFIX) : -len(".json")]
        if str(proc.get("id", "")) != pid:
            errors.append(f"{name}: process.id must match filename ({pid})")
            continue
        processes.append(proc)

    processes_sorted = tuple(sorted(processes, key=lambda p: str(p.get("id", ""))))
    if PLAN_PATH.is_file():
        shape: PlanOutputShape = "complete"
    else:
        shape = "partial" if names else "none"
    return SegmentScan(
        shape=shape,
        segment_files=tuple(names),
        header=header,
        processes=processes_sorted,
        errors=tuple(errors),
    )


def assemble_plan_dict(scan: SegmentScan) -> dict[str, Any] | None:
    """Read-only merge for equivalence checks — never used to create team-plan.json in CI."""
    if scan.header is None or not scan.processes:
        return None
    summary = scan.header.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        return None
    return {"summary": summary, "processes": [dict(p) for p in scan.processes]}


def plan_core_fields(plan: dict[str, Any]) -> dict[str, Any]:
    processes = []
    for proc in plan.get("processes") or []:
        if not isinstance(proc, dict):
            continue
        processes.append(
            {
                "id": proc.get("id"),
                "title": proc.get("title"),
                "scope": proc.get("scope"),
                "files": list(proc.get("files") or []),
                "task": proc.get("task"),
                "checks": list(proc.get("checks") or []),
            }
        )
    processes.sort(key=lambda p: str(p.get("id", "")))
    return {"summary": plan.get("summary", ""), "processes": processes}


def plans_core_equivalent(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return plan_core_fields(left) == plan_core_fields(right)


def plan_slice_payload(scan: SegmentScan) -> dict[str, Any]:
    return {
        "schema_version": PLAN_SLICE_SCHEMA,
        "output_shape": scan.shape,
        "segment_files": list(scan.segment_files),
        "process_segment_count": len(scan.processes),
        "has_header_segment": scan.header is not None,
        "segment_errors": list(scan.errors),
    }


def patch_wall_plan_slice(wall_path: Path, scan: SegmentScan, *, role: str | None = None) -> None:
    wall = load_wall(wall_path)
    patch: dict[str, Any] = {"plan": plan_slice_payload(scan)}
    if role:
        patch["budgets"] = {"session_outcome": {"role": role, "plan_output_shape": scan.shape}}
    save_wall(deep_merge(wall, patch), wall_path)


def cmd_sync_wall(wall_path: Path, role: str) -> int:
    scan = scan_segments()
    patch_wall_plan_slice(wall_path, scan, role=role)
    print(
        "lead plan segments:",
        f"shape={scan.shape}",
        f"files={len(scan.segment_files)}",
        f"processes={len(scan.processes)}",
    )
    for err in scan.errors:
        print("segment warning:", err, file=sys.stderr)
    return 0


def cmd_assert_ready(wall_path: Path | None) -> int:
    scan = scan_segments()
    if wall_path and wall_path.is_file():
        patch_wall_plan_slice(wall_path, scan, role="lead")
    if scan.errors:
        for err in scan.errors:
            print(err, file=sys.stderr)
        return 1
    if PLAN_PATH.is_file():
        try:
            plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            print("team-plan.json unreadable", file=sys.stderr)
            return 1
        assembled = assemble_plan_dict(scan)
        if assembled is not None and not plans_core_equivalent(plan, assembled):
            print(
                "team-plan.json core fields differ from segment assembly (equivalence)",
                file=sys.stderr,
            )
            return 1
        print("lead plan ready:", f"shape={scan.shape}", f"processes={len(plan.get('processes') or [])}")
        return 0
    if scan.shape == "none":
        print("lead plan missing: no team-plan.json and no segments on disk", file=sys.stderr)
        return 1
    print(
        "lead plan partial:",
        f"{len(scan.segment_files)} segment file(s); refusing to stitch into team-plan.json",
        file=sys.stderr,
    )
    return 1


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sync = sub.add_parser("sync-wall", help="Record segment scan on ForemanRun wall after lead session")
    sync.add_argument("--wall", default="foreman-run.json")
    sync.add_argument("--role", default="lead")
    gate = sub.add_parser("assert-ready", help="Fail unless team-plan.json exists; record partial|none on wall")
    gate.add_argument("--wall", default=None)
    args = p.parse_args()
    if args.cmd == "sync-wall":
        return cmd_sync_wall(Path(args.wall), args.role)
    if args.cmd == "assert-ready":
        wall = Path(args.wall) if args.wall else None
        return cmd_assert_ready(wall)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())