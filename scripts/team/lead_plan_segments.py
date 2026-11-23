#!/usr/bin/env python3
"""Lead plan segments are the single hand-written source of team-plan.json.

The lead writes only segments (00-header.json + one file per process card).
The machine stitches them into team-plan.json via ``stitch_plan_file`` /
``stitch`` — the lead never writes the plan, so there is no second artifact
to reconcile.
"""
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
# Process-card id rule (matches the lead prompt): derive the id from the
# module-name stem — lower-case it, turn underscores into hyphens; the result
# must fit ^[a-z0-9][a-z0-9-]*$, which is also the id==filename constraint.
SEGMENT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

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
    return bool(SEGMENT_ID_RE.fullmatch(pid))


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
        return SegmentScan("none", (), None, (), ())

    names = sorted(p.name for p in segments_dir.iterdir() if p.is_file() and p.suffix == ".json")
    if not names:
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
            errors.append(
                f"{name}: process.id must match filename ({pid}); "
                "rename the segment file to process-<id>.json where <id> is the card id "
                "derived from the module-name stem (lower-case, underscores -> hyphens)"
            )
            continue
        processes.append(proc)

    processes_sorted = tuple(sorted(processes, key=lambda p: str(p.get("id", ""))))
    # complete = every card scanned clean under a header with a usable summary;
    # partial = some segments on disk that did not yield a full card set.
    header_summary_ok = (
        header is not None
        and isinstance(header.get("summary"), str)
        and bool(str(header.get("summary")).strip())
    )
    if not errors and header_summary_ok and processes_sorted:
        shape: PlanOutputShape = "complete"
    else:
        shape = "partial"
    return SegmentScan(
        shape=shape,
        segment_files=tuple(names),
        header=header,
        processes=processes_sorted,
        errors=tuple(errors),
    )


def assemble_plan_dict(scan: SegmentScan) -> dict[str, Any] | None:
    """Single-direction stitch: segments -> plan dict (the machine writes it)."""
    if scan.header is None or not scan.processes:
        return None
    summary = scan.header.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        return None
    return {"summary": summary, "processes": [dict(p) for p in scan.processes]}


def write_stitched_plan(plan_path: Path, scan: SegmentScan) -> bool:
    """Overwrite plan_path with the segment assembly.

    Returns True when a plan was written (header + at least one card), False
    when the scan produced nothing stitchable. The path is replaced wholesale:
    a pre-existing file (stale hand-written plan or a previous shape) is never
    merged, it is overwritten from segments.
    """
    assembled = assemble_plan_dict(scan)
    if assembled is None:
        return False
    plan_path.write_text(
        json.dumps(assembled, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return True


def stitch_plan_file(
    plan_path: Path | None = None, *, scan: SegmentScan | None = None
) -> PlanOutputShape | None:
    """Stitch segments into team-plan.json; returns the resulting shape.

    Called in the lead job before any step reads team-plan.json. shape is
    complete (header + full segment set), partial (header + at least one
    card), or None when nothing stitchable exists (no team-plan.json written).
    """
    if scan is None:
        scan = scan_segments()
    if plan_path is None:
        plan_path = PLAN_PATH
    write_stitched_plan(plan_path, scan)
    if scan.header is None or not scan.processes:
        return None
    return "complete" if scan.shape == "complete" else "partial"


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


def cmd_stitch(wall_path: Path | None = None) -> int:
    scan = scan_segments()
    shape = stitch_plan_file(scan=scan)
    print("stitch:", f"shape={shape or 'none'}")
    if wall_path is not None and wall_path.is_file():
        patch_wall_plan_slice(wall_path, scan, role="lead")
    return 0


def cmd_assert_ready(wall_path: Path | None) -> int:
    scan = scan_segments()
    if wall_path and wall_path.is_file():
        patch_wall_plan_slice(wall_path, scan, role="lead")
    if scan.errors:
        for err in scan.errors:
            print(err, file=sys.stderr)
        return 1
    stitchable = scan.header is not None and bool(scan.processes)
    if not stitchable:
        print("team-plan.json missing: nothing stitchable on disk", file=sys.stderr)
        return 1
    if not write_stitched_plan(PLAN_PATH, scan):
        print("team-plan.json missing: nothing stitchable on disk", file=sys.stderr)
        return 1
    try:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("team-plan.json unreadable", file=sys.stderr)
        return 1
    if not isinstance(plan.get("summary"), str) or not str(plan.get("summary")).strip():
        print("team-plan.json missing summary", file=sys.stderr)
        return 1
    if not isinstance(plan.get("processes"), list) or not plan.get("processes"):
        print("team-plan.json missing processes", file=sys.stderr)
        return 1
    print("lead plan ready:", f"shape={scan.shape}", f"processes={len(plan.get('processes') or [])}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sync = sub.add_parser("sync-wall", help="Record segment scan on ForemanRun wall after lead session")
    sync.add_argument("--wall", default="foreman-run.json")
    sync.add_argument("--role", default="lead")
    gate = sub.add_parser("assert-ready", help="Stitch segments into team-plan.json, then verify schema")
    gate.add_argument("--wall", default=None)
    stitch = sub.add_parser("stitch", help="Stitch segments into team-plan.json (shape none|partial|complete)")
    stitch.add_argument("--plan", default=None)
    stitch.add_argument(
        "--wall",
        default=None,
        help="Record the stitch scan on this ForemanRun wall (the plan slice "
        "then carries the same shape the stitch log prints)",
    )
    args = p.parse_args()
    if args.cmd == "sync-wall":
        return cmd_sync_wall(Path(args.wall), args.role)
    if args.cmd == "assert-ready":
        wall = Path(args.wall) if args.wall else None
        return cmd_assert_ready(wall)
    if args.cmd == "stitch":
        wall = Path(args.wall) if args.wall else None
        return cmd_stitch(wall)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
