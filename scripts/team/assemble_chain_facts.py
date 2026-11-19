#!/usr/bin/env python3
"""Render assemble stop reason from chain topology (P1-3 / W5)."""
from __future__ import annotations

import argparse
import json
import os
import sys

from foreman_run_lib import chain_summary_code_for_result, load_wall, patch_chain_job, save_wall

CHAIN_ORDER = [
    "lead",
    "worker",
    "prep",
    "validate",
    "replan",
    "worker2",
    "prep2",
    "validate2",
]

FACT_TEMPLATES = {
    ("worker", "failure"): (
        "worker_failed_with_evidence",
        "工人 job 失败，但已产出交接证据；不得以「备料未启动」概括。",
        ["备料未启动"],
    ),
    ("prep", "success"): (
        "prep_completed",
        "备料已完成并产出 evidence artifact。",
        [],
    ),
    ("validate", "failure"): (
        "validation_structural",
        "验收 job 结构性失败或采认未完成。",
        [],
    ),
}


def derive_downstream_blocker(wall: dict) -> str | None:
    for job in CHAIN_ORDER:
        node = (wall.get("chain") or {}).get(job) or {}
        if node.get("started") and not node.get("produced_required_artifact"):
            if node.get("result") in ("failure", "cancelled"):
                return job
    return None


def build_facts(wall: dict, env_results: dict[str, str]) -> dict:
    for job in CHAIN_ORDER:
        env_result = env_results.get(job, "skipped")
        node = (wall.get("chain") or {}).get(job) or {}
        result = node.get("result")
        if result in (None, "unknown"):
            mapping = {
                "success": "success",
                "failure": "failure",
                "cancelled": "cancelled",
                "skipped": "skipped",
            }
            result = mapping.get(env_result, "unknown")
        workers = wall.get("workers") or {}
        prep = wall.get("chain", {}).get("prep") or {}
        if job == "worker" and result == "failure" and workers.get("completed_pids"):
            code, detail, forbidden = FACT_TEMPLATES["worker", "failure"]
        elif job == "prep" and prep.get("produced_required_artifact"):
            code, detail, forbidden = FACT_TEMPLATES["prep", "success"]
        elif job == "validate" and (wall.get("validation") or {}).get("adoption_status") == "failed":
            code, detail, forbidden = (
                "adoption_failed",
                f"采认失败：{(wall.get('validation') or {}).get('adoption_error')}",
                ["备料未启动"],
            )
        elif result == "failure":
            code, detail, forbidden = "failed", f"{job} job 失败", []
        elif result == "cancelled":
            code, detail, forbidden = "cancelled", f"{job} job 被取消/超时", []
        elif result == "skipped":
            code, detail, forbidden = "not_started", f"{job} 未启动", []
        else:
            code, detail, forbidden = "ok", f"{job} 正常", []
        wall.setdefault("chain", {})[job] = {
            **node,
            "result": result,
            "started": result not in ("skipped", "unknown"),
            "chain_facts": {
                "summary_code": code,
                "detail": detail,
                "forbidden_phrases": forbidden,
            },
        }
    blocker = derive_downstream_blocker(wall)
    if blocker:
        wall["chain"][blocker]["downstream_blocker"] = blocker
    return wall


def sync_assemble_exit(
    wall: dict,
    *,
    job_result: str,
    produced_required_artifact: bool,
) -> dict:
    """Patch only chain.assemble; never backfill other seats from needs.*."""
    summary = chain_summary_code_for_result(job_result)
    if job_result == "success":
        detail = "assemble 收口完成"
        forbidden: list[str] = []
    else:
        detail = pick_fallback_reason(wall)
        forbidden = []
    return patch_chain_job(
        wall,
        "assemble",
        result=job_result,
        produced_required_artifact=produced_required_artifact,
        chain_facts={
            "summary_code": summary,
            "detail": detail,
            "forbidden_phrases": forbidden,
        },
    )


def pick_fallback_reason(wall: dict) -> str:
    for job in CHAIN_ORDER:
        node = (wall.get("chain") or {}).get(job) or {}
        facts = node.get("chain_facts") or {}
        if node.get("result") in ("failure", "cancelled"):
            detail = facts.get("detail") or f"{job} 异常"
            forbidden = facts.get("forbidden_phrases") or []
            if job == "worker" and (wall.get("workers") or {}).get("completed_pids"):
                if "备料未启动" in detail:
                    return "工人 job 失败，但备料链路已部分启动（见 workers.completed_pids）"
            if not any(p in detail for p in forbidden):
                return detail
            return facts.get("detail") or detail
    val = wall.get("validation") or {}
    if val.get("adoption_error"):
        return f"采认失败：{val['adoption_error']}（人类停单）"
    return "验收未产出判定（chain_facts 兜底）"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wall", default="foreman-run.json")
    p.add_argument("--github-output", default="")
    p.add_argument(
        "--assemble-exit",
        action="store_true",
        help="Only record chain.assemble exit; do not merge needs.* into chain",
    )
    p.add_argument("--result", default="")
    p.add_argument("--produced", choices=["true", "false"], default="false")
    args = p.parse_args()
    wall = load_wall(args.wall)
    if args.assemble_exit:
        job_result = args.result or os.environ.get("JOB_STATUS", "success")
        produced = args.produced == "true"
        merged = sync_assemble_exit(
            wall, job_result=job_result, produced_required_artifact=produced
        )
        save_wall(merged, args.wall)
        reason = pick_fallback_reason(merged)
        print("assemble_exit:", job_result, "fallback_reason:", reason)
        if args.github_output:
            with open(args.github_output, "a", encoding="utf-8") as out:
                out.write(f"fallback_reason={reason}\n")
        return 0
    env_results = {
        job.upper(): os.environ.get(f"{job.upper()}_RESULT", "")
        for job in CHAIN_ORDER
    }
    merged = build_facts(wall, {k.lower(): v for k, v in env_results.items() if v})
    save_wall(merged, args.wall)
    reason = pick_fallback_reason(merged)
    print("fallback_reason:", reason)
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as out:
            out.write(f"fallback_reason={reason}\n")
    for job in CHAIN_ORDER:
        facts = merged["chain"][job]["chain_facts"]
        for phrase in facts.get("forbidden_phrases") or []:
            if phrase in reason:
                print(f"forbidden phrase in reason: {phrase}", file=sys.stderr)
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())