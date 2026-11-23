#!/usr/bin/env python3
"""Build env slice + foreman-run.json from env-check-results.tsv (L0 / W3)."""
from __future__ import annotations

import argparse
import json
import os
import sys

from foreman_run_lib import init_wall, save_wall


def parse_tsv(path: str) -> list[tuple[str, str, str]]:
    rows = []
    for line in open(path, encoding="utf-8"):
        parts = line.rstrip("\n").split("\t")
        if len(parts) == 3:
            rows.append((parts[0], parts[1], parts[2]))
    return rows


def build_env_slice(rows: list[tuple[str, str, str]], secrets: dict[str, bool]) -> dict:
    hard_fails: list[str] = []
    soft_warns: list[str] = []
    for status, item, detail in rows:
        if status == "FAIL":
            hard_fails.append(f"{item}: {detail}")
        elif status == "WARN":
            soft_warns.append(f"{item}: {detail}")
    for name, present in secrets.items():
        if not present:
            hard_fails.append(f"Secret 缺失: {name}")
    project_readable = not any("板面配置" in f and "FAIL" in str(r) for r in rows for f in [r[0]])
    for status, item, detail in rows:
        if item == "板面配置" and status == "FAIL":
            project_readable = False
    hard_fail_count = len(hard_fails)
    ok = hard_fail_count == 0
    return {
        "schema_version": "env-slice.v1",
        "ok": ok,
        "hard_fail_count": hard_fail_count,
        "hard_fails": hard_fails,
        "soft_warns": soft_warns,
        "project_readable": project_readable,
        "actions_can_create_pr": not any("创建 PR" in d and s == "FAIL" for s, _i, d in rows),
        "secrets_required": {
            "FACTORY_API_KEY": secrets.get("FACTORY_API_KEY", False),
            "WORKER_CI_KEY": secrets.get("WORKER_CI_KEY", False),
            "PROJECTS_STATE_PAT": secrets.get("PROJECTS_STATE_PAT", False),
        },
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--results-tsv", default="env-check-results.tsv")
    p.add_argument("--issue", type=int, required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--foreman-mode", default=os.environ.get("FOREMAN_MODE", "test"))
    p.add_argument("--out", default="foreman-run.json")
    p.add_argument("--github-output", default="")
    args = p.parse_args()
    secrets = {
        "FACTORY_API_KEY": bool(os.environ.get("S_FACTORY_API_KEY")),
        "WORKER_CI_KEY": bool(os.environ.get("S_WORKER_CI_KEY")),
        "PROJECTS_STATE_PAT": bool(os.environ.get("S_PROJECTS_STATE_PAT")),
    }
    if not secrets["PROJECTS_STATE_PAT"]:
        extra_row = ("FAIL", "Secret 名单", "PROJECTS_STATE_PAT 缺失")
        rows = parse_tsv(args.results_tsv)
        rows.append(extra_row)
    else:
        rows = parse_tsv(args.results_tsv)
    env_slice = build_env_slice(rows, secrets)
    wall = init_wall(
        run_id=args.run_id,
        issue_number=args.issue,
        foreman_mode=args.foreman_mode,
    )
    wall["env"] = env_slice
    wall["artifacts"][f"foreman-run-{args.run_id}"]["complete"] = bool(env_slice["ok"])
    wall["artifacts"][f"foreman-run-{args.run_id}"]["missing"] = []
    save_wall(wall, args.out)
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as out:
            out.write(f"foreman_ok={'true' if env_slice['ok'] else 'false'}\n")
            out.write(f"hard_fail_count={env_slice['hard_fail_count']}\n")
    print("env.ok:", env_slice["ok"], "hard_fail_count:", env_slice["hard_fail_count"])
    return 0 if env_slice["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())