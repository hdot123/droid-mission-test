#!/usr/bin/env python3
"""Run adopt_verdict.py inside GNU timeout driven by wall adopt_reserve_sec."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from budget_resolve import adopt_reserve_sec
from foreman_run_lib import load_wall

ADOPT_KILL_AFTER_SEC = 10


def build_adopt_timeout_cmd(reserve_sec: int, argv: list[str]) -> list[str]:
    return [
        "timeout",
        "--signal=TERM",
        f"--kill-after={ADOPT_KILL_AFTER_SEC}s",
        f"{reserve_sec}s",
        *argv,
    ]


def run_adopt(
    *,
    wall_path: Path,
    work_dir: Path,
    droid_exit: int | None,
    merge_step_ran: bool,
    round_num: int,
    round1_verdict: Path | None,
    github_output: Path | None,
) -> int:
    if os.environ.get("FOREMAN_RUN_PATCH") != "1":
        print("FOREMAN_RUN_PATCH=1 required for adopt step", file=sys.stderr)
        return 2
    wall = load_wall(wall_path)
    reserve = adopt_reserve_sec(wall, "validator")
    if reserve <= 0:
        print("adopt_reserve_sec must be positive on wall", file=sys.stderr)
        return 2
    adopt_argv = [
        sys.executable,
        str(Path(__file__).resolve().parent / "adopt_verdict.py"),
        "--wall",
        str(wall_path),
        "--work-dir",
        str(work_dir),
    ]
    if droid_exit is not None and droid_exit >= 0:
        adopt_argv.extend(["--droid-exit", str(droid_exit)])
    if merge_step_ran:
        adopt_argv.append("--merge-step-ran")
    if round_num == 2:
        adopt_argv.extend(["--round", "2"])
        if round1_verdict and round1_verdict.is_file():
            adopt_argv.extend(["--round1-verdict", str(round1_verdict)])
    cmd = build_adopt_timeout_cmd(reserve, adopt_argv)
    print(f"adopt step: wall adopt_reserve_sec={reserve}, gnu_timeout={reserve}s")
    proc = subprocess.run(cmd, env={**os.environ, "PYTHONPATH": os.environ.get("PYTHONPATH", "scripts/team")})
    if proc.returncode != 0:
        return proc.returncode
    verdict_path = Path("verdict.json")
    if not verdict_path.is_file():
        return proc.returncode
    if github_output:
        import json

        v = json.loads(verdict_path.read_text(encoding="utf-8"))
        with github_output.open("a", encoding="utf-8") as out:
            out.write(f"overall={v.get('overall', 'fail')}\n")
            failed = [p["id"] for p in v.get("processes", []) if p.get("verdict") != "pass"]
            out.write("failed_processes=" + json.dumps(failed) + "\n")
            if round_num == 1:
                out.write(
                    f"unattributed_failure={'true' if v.get('unattributed_failure') else 'false'}\n"
                )
            if round_num == 2 or v.get("flips"):
                out.write("flips=" + json.dumps(v.get("flips") or [], ensure_ascii=False) + "\n")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--work-dir", default="work")
    p.add_argument("--droid-exit", type=int, default=-1)
    p.add_argument("--merge-step-ran", action="store_true")
    p.add_argument("--round", type=int, default=1)
    p.add_argument("--round1-verdict", default="")
    p.add_argument("--github-output", default="")
    args = p.parse_args()
    droid_exit = args.droid_exit if args.droid_exit >= 0 else None
    r1 = Path(args.round1_verdict) if args.round1_verdict else None
    gh_out = Path(args.github_output) if args.github_output else None
    if gh_out is None and os.environ.get("GITHUB_OUTPUT"):
        gh_out = Path(os.environ["GITHUB_OUTPUT"])
    return run_adopt(
        wall_path=Path(args.wall),
        work_dir=Path(args.work_dir),
        droid_exit=droid_exit,
        merge_step_ran=args.merge_step_ran,
        round_num=args.round,
        round1_verdict=r1,
        github_output=gh_out,
    )


if __name__ == "__main__":
    raise SystemExit(main())
