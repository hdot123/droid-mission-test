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

from budget_resolve import droid_wall_sec, session_completion_status
from foreman_run_lib import deep_merge, load_wall, save_wall

DROID_BIN = os.path.expanduser("~/.local/bin/droid")
FOREMAN_RUN_PATCH_ENV = "FOREMAN_RUN_PATCH"
KILL_AFTER_SEC = 30


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


def _patch_session_outcome(
    wall_path: Path,
    *,
    role: str,
    exit_code: int,
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

        session_outcome["plan_output_shape"] = scan_segments().shape
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
    if enable_heartbeat:
        heartbeat = _StreamHeartbeat(
            stream_out,
            min_elapsed_sec=int(os.environ.get("FOREMAN_HEARTBEAT_MIN_ELAPSED_SEC", "180")),
            idle_sec=int(os.environ.get("FOREMAN_HEARTBEAT_IDLE_SEC", "120")),
        )
        heartbeat.start()
    try:
        with stream_out.open("w", encoding="utf-8") as stream_f:
            proc = subprocess.run(
                timeout_cmd,
                stdout=stream_f,
                stderr=subprocess.PIPE,
                text=True,
            )
    finally:
        if heartbeat:
            heartbeat.stop()
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    exit_code = proc.returncode
    exit_out.parent.mkdir(parents=True, exist_ok=True)
    exit_out.write_text(f"{exit_code}\n", encoding="utf-8")
    if wall_path.is_file():
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