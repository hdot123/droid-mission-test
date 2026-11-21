#!/usr/bin/env python3
"""ForemanRun session wrapper: droid wall from budgets.roles[role] (batch-3 / P0-2)."""
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Callable

from budget_resolve import droid_wall_sec, session_completion_status
from foreman_run_lib import deep_merge, load_wall, save_wall

DROID_BIN = os.path.expanduser("~/.local/bin/droid")
FOREMAN_RUN_PATCH_ENV = "FOREMAN_RUN_PATCH"
KILL_AFTER_SEC = 30
# Lead segment hard gate: elapsed session time with zero segment files on disk.
LEAD_SEGMENT_GATE_EXIT = 125


class _StreamHeartbeat:
    """Auxiliary dual-threshold stall detector (warn-only unless FOREMAN_HEARTBEAT_KILL=1)."""

    def __init__(self, stream_path: Path, *, min_elapsed_sec: int, idle_sec: int):
        self.stream_path = stream_path
        self.min_elapsed_sec = min_elapsed_sec
        self.idle_sec = idle_sec
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._start = time.monotonic()
        self._last_size = 0
        self._last_growth = self._start

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self) -> None:
        kill_enabled = os.environ.get("FOREMAN_HEARTBEAT_KILL", "").lower() in (
            "1",
            "true",
            "yes",
        )
        while not self._stop.wait(5):
            if not self.stream_path.exists():
                continue
            size = self.stream_path.stat().st_size
            now = time.monotonic()
            if size > self._last_size:
                self._last_size = size
                self._last_growth = now
                continue
            elapsed = now - self._start
            idle = now - self._last_growth
            if elapsed < self.min_elapsed_sec or idle < self.idle_sec:
                continue
            msg = (
                f"heartbeat: dual threshold met (elapsed={elapsed:.0f}s>={self.min_elapsed_sec}, "
                f"idle={idle:.0f}s>={self.idle_sec}); stream stalled"
            )
            print(msg, file=sys.stderr)
            if kill_enabled:
                print(
                    "heartbeat: FOREMAN_HEARTBEAT_KILL ignored in batch-3 (warn-only)",
                    file=sys.stderr,
                )


class _LeadSegmentGate:
    """Fail-closed: no lead-plan segment files on disk after elapsed threshold."""

    def __init__(
        self,
        *,
        gate_sec: int,
        scan: Callable[[], object],
        proc_getter: Callable[[], subprocess.Popen[str] | None],
        on_trip: Callable[[], None],
    ):
        self.gate_sec = gate_sec
        self.scan = scan
        self.proc_getter = proc_getter
        self.on_trip = on_trip
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._start = time.monotonic()
        self.tripped = False

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self) -> None:
        from lead_plan_segments import SegmentScan

        while not self._stop.wait(5):
            elapsed = time.monotonic() - self._start
            if elapsed < self.gate_sec:
                continue
            result = self.scan()
            if not isinstance(result, SegmentScan):
                continue
            if result.segment_files:
                continue
            proc = self.proc_getter()
            if proc is None or proc.poll() is not None:
                continue
            self.tripped = True
            print(
                "lead segment gate: hard fail — "
                f"{elapsed:.0f}s elapsed with 0 segment files on disk "
                f"(threshold={self.gate_sec}s)",
                file=sys.stderr,
            )
            self.on_trip()
            try:
                proc.terminate()
            except OSError:
                pass
            break


def _patch_session_outcome(
    wall_path: Path,
    *,
    role: str,
    exit_code: int,
    plan_output_shape: str | None = None,
) -> None:
    wall = load_wall(wall_path)
    status = session_completion_status(exit_code)
    session_outcome: dict = {
        "role": role,
        "completion_status": status,
        "exit_code": exit_code,
    }
    if role == "lead":
        from lead_plan_segments import scan_segments

        session_outcome["plan_output_shape"] = plan_output_shape or scan_segments().shape
    patch = {"budgets": {"session_outcome": session_outcome}}
    save_wall(deep_merge(wall, patch), wall_path)


def build_droid_timeout_cmd(
    *,
    wall_path: Path | None,
    role: str,
    prompt_text: str,
    wall_override_sec: int | None = None,
    droid_bin: str = DROID_BIN,
) -> tuple[list[str], int]:
    wall = load_wall(wall_path) if wall_path and wall_path.is_file() else None
    wall_sec = droid_wall_sec(wall, role, override_sec=wall_override_sec)
    droid_cmd = [
        droid_bin,
        "exec",
        "--auto",
        "high",
        "-m",
        "custom:DeepSeek-V4.1-Flash-Go",
        "--output-format",
        "stream-json",
        prompt_text,
    ]
    timeout_cmd = [
        "timeout",
        "--signal=TERM",
        f"--kill-after={KILL_AFTER_SEC}s",
        f"{wall_sec}s",
        *droid_cmd,
    ]
    return timeout_cmd, wall_sec


def _lead_segment_gate_sec() -> int:
    raw = os.environ.get("FOREMAN_LEAD_SEGMENT_GATE_SEC", "120")
    try:
        return max(1, int(raw))
    except ValueError:
        return 120


def run_session(
    *,
    wall_path: Path,
    role: str,
    prompt_file: Path,
    stream_out: Path,
    exit_out: Path,
    wall_override_sec: int | None,
    enable_heartbeat: bool,
) -> int:
    if os.environ.get(FOREMAN_RUN_PATCH_ENV) != "1":
        print(f"{FOREMAN_RUN_PATCH_ENV}=1 required for foreman droid session", file=sys.stderr)
        return 2
    if not prompt_file.is_file():
        print(f"prompt file missing: {prompt_file}", file=sys.stderr)
        return 2
    prompt_text = prompt_file.read_text(encoding="utf-8")
    timeout_cmd, wall_sec = build_droid_timeout_cmd(
        wall_path=wall_path,
        role=role,
        prompt_text=prompt_text,
        wall_override_sec=wall_override_sec,
    )
    print(
        "foreman droid session:",
        f"role={role}",
        f"wall_droid_sec={wall_sec}",
        f"cmd={' '.join(shlex.quote(c) for c in timeout_cmd[:6])} …",
    )
    stream_out.parent.mkdir(parents=True, exist_ok=True)
    heartbeat: _StreamHeartbeat | None = None
    segment_gate: _LeadSegmentGate | None = None
    proc: subprocess.Popen[str] | None = None
    segment_gate_forced_exit: int | None = None
    use_popen = role == "lead" and enable_heartbeat

    if enable_heartbeat:
        heartbeat = _StreamHeartbeat(
            stream_out,
            min_elapsed_sec=int(os.environ.get("FOREMAN_HEARTBEAT_MIN_ELAPSED_SEC", "180")),
            idle_sec=int(os.environ.get("FOREMAN_HEARTBEAT_IDLE_SEC", "120")),
        )
        heartbeat.start()

    if use_popen:
        from lead_plan_segments import scan_segments

        gate_sec = _lead_segment_gate_sec()
        print(f"lead segment gate: armed (threshold={gate_sec}s elapsed, 0 files)", file=sys.stderr)

        def _trip_gate() -> None:
            nonlocal segment_gate_forced_exit
            segment_gate_forced_exit = LEAD_SEGMENT_GATE_EXIT
            if wall_path.is_file():
                _patch_session_outcome(
                    wall_path,
                    role=role,
                    exit_code=LEAD_SEGMENT_GATE_EXIT,
                    plan_output_shape="none",
                )

        segment_gate = _LeadSegmentGate(
            gate_sec=gate_sec,
            scan=scan_segments,
            proc_getter=lambda: proc,
            on_trip=_trip_gate,
        )
        segment_gate.start()

    completed: subprocess.CompletedProcess[str] | None = None
    stderr_text = ""
    try:
        with stream_out.open("w", encoding="utf-8") as stream_f:
            if use_popen:
                proc = subprocess.Popen(
                    timeout_cmd,
                    stdout=stream_f,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                _, stderr_text = proc.communicate()
            else:
                completed = subprocess.run(
                    timeout_cmd,
                    stdout=stream_f,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stderr_text = completed.stderr or ""
    finally:
        if segment_gate:
            segment_gate.stop()
        if heartbeat:
            heartbeat.stop()

    if use_popen:
        assert proc is not None
        exit_code = (
            segment_gate_forced_exit
            if segment_gate_forced_exit is not None
            else (proc.returncode if proc.returncode is not None else 0)
        )
    else:
        assert completed is not None
        exit_code = completed.returncode
    if stderr_text:
        print(stderr_text, file=sys.stderr)

    exit_out.parent.mkdir(parents=True, exist_ok=True)
    exit_out.write_text(f"{exit_code}\n", encoding="utf-8")
    if wall_path.is_file() and segment_gate_forced_exit is None:
        _patch_session_outcome(
            wall_path,
            role=role,
            exit_code=exit_code,
        )
    return exit_code


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--role", required=True, choices=["lead", "validator", "replan", "worker"])
    p.add_argument("--prompt-file", required=True)
    p.add_argument("--stream-out", required=True)
    p.add_argument("--exit-out", required=True)
    p.add_argument("--droid-wall-override-sec", type=int, default=None)
    p.add_argument("--heartbeat", action="store_true")
    args = p.parse_args()
    code = run_session(
        wall_path=Path(args.wall),
        role=args.role,
        prompt_file=Path(args.prompt_file),
        stream_out=Path(args.stream_out),
        exit_out=Path(args.exit_out),
        wall_override_sec=args.droid_wall_override_sec,
        enable_heartbeat=args.heartbeat,
    )
    return 0 if code in (0, 124) else code


if __name__ == "__main__":
    raise SystemExit(main())