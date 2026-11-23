"""ForemanRun wall: init, patch merge, schema validation (v2.7)."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "foreman-run.v1"
DEFAULT_FOREMAN_MODE = "test"
ARTIFACT_NAME_TEMPLATE = "foreman-run"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def schema_path() -> Path:
    return repo_root() / "schemas" / "foreman-run.v1.schema.json"


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    for key, val in patch.items():
        if key in out and isinstance(out[key], dict) and isinstance(val, dict):
            out[key] = deep_merge(out[key], val)
        else:
            out[key] = copy.deepcopy(val)
    return out


def default_budgets() -> dict[str, Any]:
    return {
        "schema_version": "budget-slice.v1",
        "roles": {
            "lead": {
                "droid_wall_sec": 600,
                "job_wall_min": 15,
                "output_contract": "plan_json",
            },
            "validator": {
                "droid_wall_sec": 480,
                "adopt_reserve_sec": 120,
                "job_wall_min": 12,
                "output_contract": "verdict_draft",
            },
            "replan": {
                "droid_wall_sec": 480,
                "job_wall_min": 15,
                "output_contract": "plan_v2_json",
            },
            "worker": {
                "droid_wall_sec": 900,
                "job_wall_min": 25,
                "output_contract": "handoff_bundle",
            },
        },
    }


def default_chain() -> dict[str, Any]:
    jobs = [
        "lead",
        "worker",
        "prep",
        "validate",
        "replan",
        "worker2",
        "prep2",
        "validate2",
        "assemble",
    ]
    chain: dict[str, Any] = {}
    for job in jobs:
        chain[job] = {
            "result": "unknown",
            "started": False,
            "produced_required_artifact": False,
            "downstream_blocker": None,
            "chain_facts": {
                "summary_code": "not_started",
                "detail": "",
                "forbidden_phrases": [],
            },
        }
    return chain


def default_artifacts(issue_number: int, run_id: str) -> dict[str, Any]:
    key = f"team-verdict-issue-{issue_number}-run-{run_id}"
    key2 = f"team-verdict2-issue-{issue_number}-run-{run_id}"
    verdict_art = {
        "complete": False,
        "missing": ["verdict.json", "verdict.md"],
        "required_members": ["verdict.json", "verdict.md"],
        "forbidden_partial": ["work/validator-stream.jsonl"],
    }
    return {
        key: dict(verdict_art),
        key2: dict(verdict_art),
        f"foreman-run-{run_id}": {
            "complete": False,
            "missing": ["foreman-run.json"],
            "required_members": ["foreman-run.json"],
        },
    }


def init_wall(
    *,
    run_id: str,
    issue_number: int,
    foreman_mode: str | None = None,
) -> dict[str, Any]:
    mode = foreman_mode or os.environ.get("FOREMAN_MODE", DEFAULT_FOREMAN_MODE)
    if mode not in ("test", "prod"):
        mode = DEFAULT_FOREMAN_MODE
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": str(run_id),
        "issue_number": int(issue_number),
        "plan_issue_number": None,
        "foreman_mode": mode,
        "env": {
            "schema_version": "env-slice.v1",
            "ok": True,
            "hard_fail_count": 0,
            "hard_fails": [],
            "soft_warns": [],
            "project_readable": True,
            "actions_can_create_pr": True,
            "secrets_required": {
                "FACTORY_API_KEY": False,
                "WORKER_CI_KEY": False,
                "PROJECTS_STATE_PAT": False,
            },
        },
        "budgets": default_budgets(),
        "chain": default_chain(),
        "artifacts": default_artifacts(issue_number, run_id),
        "human_stop": False,
    }


def normalize_chain_job_result(result: str) -> str:
    """Map GitHub job conclusions onto chain `result` vocabulary."""
    r = (result or "unknown").strip().lower()
    if r == "failed":
        return "failure"
    if r in ("success", "failure", "cancelled", "skipped", "unknown"):
        return r
    return "unknown"


def chain_summary_code_for_result(result: str) -> str:
    """Map chain job `result` to `chain_facts.summary_code` (wall vocabulary)."""
    normalized = normalize_chain_job_result(result)
    return {
        "success": "ok",
        "failure": "failed",
        "cancelled": "cancelled",
        "skipped": "not_started",
        "unknown": "not_started",
    }[normalized]


def parse_project_item_list(payload: Any) -> list[dict[str, Any]]:
    """Backward-compatible alias; implementation lives in gh_project_parse."""
    from gh_project_parse import parse_project_item_list as _parse

    return _parse(payload)


def patch_chain_job(
    wall: dict[str, Any],
    job: str,
    *,
    result: str,
    started: bool | None = None,
    produced_required_artifact: bool | None = None,
    chain_facts: dict[str, Any] | None = None,
    downstream_blocker: str | None = None,
) -> dict[str, Any]:
    result = normalize_chain_job_result(result)
    patch: dict[str, Any] = {
        "chain": {
            job: {
                "result": result,
                "started": started if started is not None else result != "skipped",
                "produced_required_artifact": bool(produced_required_artifact),
                "downstream_blocker": downstream_blocker,
            }
        }
    }
    if chain_facts:
        patch["chain"][job]["chain_facts"] = chain_facts
    return deep_merge(wall, patch)


def validate_schema(wall: dict[str, Any]) -> list[str]:
    """Lightweight validation without external deps (CI also uses jsonschema when available)."""
    errors: list[str] = []
    if wall.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    for req in (
        "run_id",
        "issue_number",
        "foreman_mode",
        "env",
        "budgets",
        "chain",
        "artifacts",
    ):
        if req not in wall:
            errors.append(f"missing required field: {req}")
    env = wall.get("env") or {}
    if env.get("hard_fail_count", 0) > 0 and env.get("ok") is True:
        errors.append("env.ok must be false when hard_fail_count > 0")
    if wall.get("foreman_mode") not in ("test", "prod"):
        errors.append("foreman_mode must be test|prod")
    for job, node in (wall.get("chain") or {}).items():
        if "chain_facts" not in node:
            errors.append(f"chain.{job} missing chain_facts (W5)")
    closeout = wall.get("closeout") or {}
    if closeout.get("comments", {}).get("fallback_card", {}).get("posted") and not closeout.get(
        "run_must_fail"
    ):
        errors.append("fallback_card.posted requires closeout.run_must_fail (B5)")
    val = wall.get("validation") or {}
    if val.get("adoption_status") == "failed" and not (
        wall.get("human_stop") or closeout.get("run_must_fail")
    ):
        errors.append("adoption_status=failed requires human_stop or closeout.run_must_fail (W6)")
    return errors


def validate_with_jsonschema(wall: dict[str, Any]) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        return validate_schema(wall)
    schema = json.loads(schema_path().read_text(encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema)
    return [f"{e.message} @ {list(e.path)}" for e in validator.iter_errors(wall)]


def load_wall(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_wall(wall: dict[str, Any], path: str | Path) -> None:
    errs = validate_with_jsonschema(wall)
    if errs:
        raise ValueError("wall failed schema validation:\n" + "\n".join(errs[:20]))
    Path(path).write_text(
        json.dumps(wall, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def artifact_wall_name(run_id: str) -> str:
    return f"{ARTIFACT_NAME_TEMPLATE}-{run_id}"


def merge_worker_slice(wall: dict[str, Any], pid: str, job_result: str) -> dict[str, Any]:
    workers = wall.get("workers") or {
        "schema_version": "worker-matrix.v1",
        "any_cancelled": False,
        "any_failed": False,
        "completed_pids": [],
        "cancelled_pids": [],
        "cancel_reason_by_pid": {},
    }
    completed = list(workers.get("completed_pids") or [])
    cancelled = list(workers.get("cancelled_pids") or [])
    reasons = dict(workers.get("cancel_reason_by_pid") or {})
    if job_result == "success":
        if pid not in completed:
            completed.append(pid)
    elif job_result == "cancelled":
        workers["any_cancelled"] = True
        if pid not in cancelled:
            cancelled.append(pid)
        reasons.setdefault(pid, "job_wall_25m")
    elif job_result == "failure":
        workers["any_failed"] = True
        if pid not in completed:
            completed.append(pid)
    workers["completed_pids"] = completed
    workers["cancelled_pids"] = cancelled
    workers["cancel_reason_by_pid"] = reasons
    wall = deep_merge(wall, {"workers": workers})
    return wall


def prep_should_run(wall: dict[str, Any]) -> bool:
    workers = wall.get("workers") or {}
    return len(workers.get("completed_pids") or []) > 0
