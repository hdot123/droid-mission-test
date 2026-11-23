#!/usr/bin/env python3
"""Summarize an I8 live team run for docs/evidence archive."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_wall(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def job_snippet(jobs: list[dict]) -> str:
    lines = ["| Job | Conclusion |", "|---|---|"]
    for j in jobs:
        lines.append(f"| {j.get('name','')} | {j.get('conclusion','')} |")
    return "\n".join(lines)


def wall_excerpt(wall: dict) -> str:
    env = wall.get("env") or {}
    val = wall.get("validation") or {}
    close = (wall.get("closeout") or {}).get("comments") or {}
    arts = {
        k: v.get("complete")
        for k, v in (wall.get("artifacts") or {}).items()
        if "verdict" in k or k.startswith("foreman")
    }
    repl = (wall.get("replan_gate") or {}).get("should_replan")
    return json.dumps(
        {
            "env.ok": env.get("ok"),
            "env.hard_fail_count": env.get("hard_fail_count"),
            "env.secrets_required.PROJECTS_STATE_PAT": (env.get("secrets_required") or {}).get("PROJECTS_STATE_PAT"),
            "validation.adoption_status": val.get("adoption_status"),
            "validation.adoption_error": val.get("adoption_error"),
            "human_stop": wall.get("human_stop"),
            "artifacts_complete": arts,
            "closeout.comments": close,
            "replan_gate.should_replan": repl,
        },
        ensure_ascii=False,
        indent=2,
    )


def assess(scene: str, wall: dict | None, run_view: dict) -> tuple[str, list[str]]:
    notes: list[str] = []
    jobs = run_view.get("jobs") or []
    if scene == "B":
        lead = next((j for j in jobs if "lead" in j.get("name", "").lower()), None)
        ok_job = lead and lead.get("conclusion") == "failure"
        posted = False
        if wall:
            posted = (
                (wall.get("closeout") or {}).get("comments", {}).get("plan_dispatch", {}).get("posted") is False
            )
        pass_ = ok_job and run_view.get("conclusion") == "failure"
        if wall and not posted:
            notes.append(
                "wall closeout.comments.plan_dispatch.posted not false (artifact missing or patch absent)"
            )
        return ("PASS" if pass_ else "FAIL"), notes
    if scene in ("A", "D"):
        val_job = next(
            (j for j in jobs
             if "validator" in j.get("name", "").lower() and "round 2" not in j.get("name", "").lower()),
            None,
        )
        if scene == "A":
            adopt = (wall or {}).get("validation", {}).get("adoption_status") if wall else None
            hs = (wall or {}).get("human_stop") if wall else None
            repl = (wall or {}).get("replan_gate", {}).get("should_replan") if wall else None
            pass_ = (
                wall
                and adopt == "failed"
                and hs is True
                and repl is not True
                and val_job
                and val_job.get("conclusion") in ("failure", "cancelled")
            )
            if not wall:
                notes.append("no foreman-run artifact (cancel may have prevented wall upload)")
            return ("PASS" if pass_ else "INCONCLUSIVE"), notes
        # D
        complete_false = False
        if wall:
            for k, v in (wall.get("artifacts") or {}).items():
                if k.startswith("team-verdict") and v.get("complete") is False:
                    complete_false = True
        pass_ = complete_false and val_job and val_job.get("conclusion") in ("failure", "cancelled")
        return ("PASS" if pass_ else "INCONCLUSIVE"), notes
    if scene == "C-team":
        env = (wall or {}).get("env") or {}
        lead = next((j for j in jobs if j.get("name", "").startswith("lead")), None)
        pass_ = (
            env.get("hard_fail_count", 0) > 0
            and (lead is None or lead.get("conclusion") == "skipped")
            and run_view.get("conclusion") == "failure"
        )
        return ("PASS" if pass_ else "FAIL"), notes
    return ("UNKNOWN", notes)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--scene", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--issue", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--run-view", default="out/run-view.json")
    p.add_argument("--wall", default="out/foreman-run.json")
    args = p.parse_args()
    run_view = json.loads(Path(args.run_view).read_text(encoding="utf-8"))
    wall = load_wall(Path(args.wall))
    status, notes = assess(args.scene, wall, run_view)
    url = run_view.get("url") or f"https://github.com/{Path.cwd().name}/actions/runs/{args.run_id}"
    md = [
        f"# I8 scene {args.scene} — run `{args.run_id}`",
        "",
        f"- Issue: #{args.issue}",
        f"- Run: {url}",
        f"- Assessment: **{status}**",
        "",
        "## gh run view (jobs)",
        "",
        job_snippet(run_view.get("jobs") or []),
        "",
        "## foreman-run.json excerpt",
        "",
        "```json",
        wall_excerpt(wall) if wall else "(artifact not downloaded)",
        "```",
        "",
        "## Notes",
        "",
    ]
    if notes:
        md.extend(f"- {n}" for n in notes)
    else:
        md.append("- (none)")
    Path(args.out).write_text("\n".join(md) + "\n", encoding="utf-8")
    print(status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
