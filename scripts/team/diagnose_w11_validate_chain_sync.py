#!/usr/bin/env python3
"""W-11 诊断：复现 validate 尾步「derive 非零 → wall_sync 未跑 → chain.validate 滞留」."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEAM = ROOT / "scripts" / "team"
sys.path.insert(0, str(TEAM))

from adopt_verdict import adopt  # noqa: E402
from compute_validate_conclusion import derive  # noqa: E402
from foreman_run_lib import init_wall, save_wall  # noqa: E402

def _minimal_work(base: Path) -> Path:
    work = base / "work"
    work.mkdir()
    manifest = {
        "sha256": {},
        "packs": {},
        "pytest_exit": 0,
        "iteration": 1,
    }
    (work / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work / "plan.json").write_text(
        json.dumps({"processes": [{"id": "p1"}]}), encoding="utf-8"
    )
    (work / "judgeable.json").write_text('["p1"]', encoding="utf-8")
    return work


def _shell_derive_then_sync(wall_path: Path) -> tuple[int, str]:
    """模拟 team.yml validate 尾步：无 set +e，derive 失败即截断."""
    env = {**os.environ, "PYTHONPATH": str(TEAM)}
    script = f"""
set -eo pipefail
python3 {TEAM}/compute_validate_conclusion.py --wall {wall_path}
python3 {TEAM}/wall_sync_job.py --wall {wall_path} --job validate --result failure --produced false
"""
    proc = subprocess.run(
        ["bash", "-c", script],
        env=env,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out


def scenario_pre_session_death(tmp: Path) -> dict:
    base = tmp / "pre"
    base.mkdir(exist_ok=True)
    wall = init_wall(run_id="w11-pre", issue_number=901)
    wall_path = base / "foreman-run.json"
    save_wall(wall, wall_path)
    work = _minimal_work(base)
    adopt(work, wall_path, droid_exit=None, merge_step_ran=False)
    mid = json.loads(wall_path.read_text(encoding="utf-8"))
    derive_proc_rc = subprocess.run(
        [sys.executable, str(TEAM / "compute_validate_conclusion.py"), "--wall", str(wall_path)],
        env={**os.environ, "PYTHONPATH": str(TEAM)},
        capture_output=True,
        text=True,
    ).returncode
    merged_after_derive, conclusion = derive(mid)
    shell_rc, shell_log = _shell_derive_then_sync(wall_path)
    final = json.loads(wall_path.read_text(encoding="utf-8"))
    return {
        "scenario": "pre_session_death",
        "droid_exit": None,
        "session_outcome": final.get("budgets", {}).get("session_outcome"),
        "validation_adoption": final.get("validation", {}).get("adoption_status"),
        "job_conclusion_derived": final.get("validation", {}).get("job_conclusion_derived"),
        "derive_returncode_isolated": derive_proc_rc,
        "derive_conclusion_logic": conclusion,
        "shell_step_returncode": shell_rc,
        "chain_validate_result": final.get("chain", {}).get("validate", {}).get("result"),
        "chain_validate_started": final.get("chain", {}).get("validate", {}).get("started"),
        "wall_sync_ran": final.get("chain", {}).get("validate", {}).get("result") != "unknown",
        "shell_stderr_tail": shell_log[-400:],
    }


def scenario_session_timeout(tmp: Path) -> dict:
    base = tmp / "timeout"
    base.mkdir(exist_ok=True)
    wall = init_wall(run_id="w11-timeout", issue_number=902)
    wall_path = base / "foreman-run.json"
    save_wall(wall, wall_path)
    work = _minimal_work(base)
    adopt(work, wall_path, droid_exit=124, merge_step_ran=False)
    shell_rc, shell_log = _shell_derive_then_sync(wall_path)
    final = json.loads(wall_path.read_text(encoding="utf-8"))
    return {
        "scenario": "session_timeout",
        "droid_exit": 124,
        "session_outcome": final.get("budgets", {}).get("session_outcome"),
        "validation_adoption": final.get("validation", {}).get("adoption_status"),
        "adoption_error": final.get("validation", {}).get("adoption_error"),
        "job_conclusion_derived": final.get("validation", {}).get("job_conclusion_derived"),
        "shell_step_returncode": shell_rc,
        "chain_validate_result": final.get("chain", {}).get("validate", {}).get("result"),
        "wall_sync_ran": final.get("chain", {}).get("validate", {}).get("result") != "unknown",
        "shell_stderr_tail": shell_log[-400:],
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true", help="machine-readable only")
    args = p.parse_args()
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        reports = [scenario_pre_session_death(tmp), scenario_session_timeout(tmp)]
    if args.json:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
        return 0
    for r in reports:
        print("=" * 60)
        print(r["scenario"])
        print("\n".join([
            f"  adoption_status={r.get('validation_adoption')}",
            f"  job_conclusion_derived={r.get('job_conclusion_derived')}",
            f"  chain.validate.result={r.get('chain_validate_result')}",
            f"  wall_sync_ran={r.get('wall_sync_ran')}",
            f"  shell_step_rc={r.get('shell_step_returncode')}",
        ]))
    any_gap = any(not r["wall_sync_ran"] for r in reports)
    print("=" * 60)
    print("VERDICT:", "MECHANISM_CONFIRMED" if any_gap else "NO_GAP")
    return 1 if any_gap else 0


if __name__ == "__main__":
    raise SystemExit(main())