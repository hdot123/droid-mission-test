#!/usr/bin/env python3
"""Write Projects board status via PROJECTS_STATE_PAT (P1-1)."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from foreman_run_lib import deep_merge, load_wall, save_wall

STATUS_BY_OVERALL = {"pass": "已验收", "fail": "阻塞"}
STATE_FIELD_NAMES = ("Status", "状态", "state")


def _gh(args: list[str], token: str) -> subprocess.CompletedProcess:
    env = {**os.environ, "GH_TOKEN": token}
    return subprocess.run(["gh", *args], capture_output=True, text=True, env=env)


def find_item_and_project(owner: str, project_number: int, issue_number: int, token: str) -> tuple[str, str]:
    r = _gh(
        [
            "project",
            "item-list",
            str(project_number),
            "--owner",
            owner,
            "--format",
            "json",
            "--limit",
            "200",
        ],
        token,
    )
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "item-list failed").strip())
    data = json.loads(r.stdout or "{}")
    items = data.get("items") or data if isinstance(data, list) else []
    item_id = None
    for it in items:
        content = it.get("content") or {}
        if content.get("number") == issue_number:
            item_id = it.get("id")
            break
    if not item_id:
        raise RuntimeError(f"issue #{issue_number} not linked to project #{project_number}")
    pr = _gh(["project", "view", str(project_number), "--owner", owner, "--format", "json"], token)
    if pr.returncode != 0:
        raise RuntimeError((pr.stderr or pr.stdout or "project view failed").strip())
    project_id = json.loads(pr.stdout).get("id")
    if not project_id:
        raise RuntimeError("project id missing from view")
    return item_id, project_id


def pick_status_option(fields_json: list, status_text: str) -> tuple[str, str]:
    for f in fields_json:
        if f.get("name") not in STATE_FIELD_NAMES:
            continue
        for opt in f.get("options") or []:
            if opt.get("name") == status_text:
                return f["id"], opt["id"]
    raise RuntimeError(f"no board option {status_text!r} in fields {STATE_FIELD_NAMES}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--overall", required=True)
    p.add_argument("--issue", type=int, required=True)
    p.add_argument("--project", type=int, default=int(os.environ.get("PROJECT_NUMBER", "33")))
    args = p.parse_args()
    pat = os.environ.get("PROJECTS_STATE_PAT", "")
    if not pat:
        print("PROJECTS_STATE_PAT missing", file=sys.stderr)
        return 1
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    owner = repo.split("/")[0] if "/" in repo else os.environ.get("GITHUB_REPOSITORY_OWNER", "")
    status = STATUS_BY_OVERALL.get(args.overall, "阻塞")
    ok = False
    err = None
    try:
        item_id, project_id = find_item_and_project(owner, args.project, args.issue, pat)
        fr = _gh(["project", "field-list", str(args.project), "--owner", owner, "--format", "json"], pat)
        if fr.returncode != 0:
            raise RuntimeError((fr.stderr or fr.stdout).strip())
        fields = json.loads(fr.stdout or "[]")
        field_id, option_id = pick_status_option(fields, status)
        er = _gh(
            [
                "project",
                "item-edit",
                "--project-id",
                project_id,
                "--id",
                item_id,
                "--field-id",
                field_id,
                "--single-select-option-id",
                option_id,
            ],
            pat,
        )
        if er.returncode != 0:
            raise RuntimeError((er.stderr or er.stdout or "item-edit failed").strip())
        ok = True
        print(f"project state -> {status}")
    except Exception as exc:
        err = str(exc)
        print(f"project state write failed: {err}", file=sys.stderr)
    wall_path = Path(args.wall)
    if wall_path.exists():
        patch: dict = {
            "closeout": {
                "schema_version": "closeout-slice.v1",
                "project_state_written": ok,
                "project_state_enum": status if ok else None,
            }
        }
        if err:
            patch["closeout"]["project_state_error"] = err
        if not ok:
            patch["closeout"]["run_must_fail"] = True
        save_wall(deep_merge(load_wall(wall_path), patch), wall_path)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())