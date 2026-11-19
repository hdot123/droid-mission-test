"""Resolve ForemanRun budget slice for workflow sessions (batch-3 / P0-2)."""
from __future__ import annotations

from typing import Any

from foreman_run_lib import default_budgets

VALID_ROLES = ("lead", "validator", "replan", "worker")
KILL_AFTER_SEC = 30


def role_budget(wall: dict[str, Any] | None, role: str) -> dict[str, Any]:
    if role not in VALID_ROLES:
        raise ValueError(f"unknown role: {role}")
    budgets = (wall or {}).get("budgets") or default_budgets()
    roles = budgets.get("roles") or {}
    base = default_budgets()["roles"][role]
    merged = dict(base)
    merged.update(roles.get(role) or {})
    return merged


def droid_wall_sec(
    wall: dict[str, Any] | None,
    role: str,
    *,
    override_sec: int | None = None,
) -> int:
    if override_sec is not None:
        return int(override_sec)
    return int(role_budget(wall, role).get("droid_wall_sec", 600))


def adopt_reserve_sec(wall: dict[str, Any] | None, role: str = "validator") -> int:
    return int(role_budget(wall, role).get("adopt_reserve_sec", 0))


def validator_session_budget(wall: dict[str, Any] | None) -> tuple[int, int]:
    """Return (droid_wall_sec, adopt_reserve_sec) from wall config."""
    rb = role_budget(wall, "validator")
    return int(rb.get("droid_wall_sec", 480)), int(rb.get("adopt_reserve_sec", 120))


def job_wall_min(wall: dict[str, Any] | None, role: str) -> int:
    return int(role_budget(wall, role).get("job_wall_min", 15))


def assert_validator_job_budget(wall: dict[str, Any] | None, *, job_timeout_min: int) -> list[str]:
    """Fail-closed check: job wall must cover droid + adopt reserve."""
    droid, adopt = validator_session_budget(wall)
    job_sec = int(job_timeout_min) * 60
    errs: list[str] = []
    if droid + adopt + KILL_AFTER_SEC > job_sec:
        errs.append(
            f"validator job {job_timeout_min}m too small for "
            f"droid_wall={droid}s + adopt_reserve={adopt}s + kill_after={KILL_AFTER_SEC}s"
        )
    if droid != 480:
        errs.append(f"validator droid_wall_sec expected 480 in config, got {droid}")
    if adopt != 120:
        errs.append(f"validator adopt_reserve_sec expected 120 in config, got {adopt}")
    return errs


def session_completion_status(exit_code: int | None) -> str:
    if exit_code == 124:
        return "timeout"
    if exit_code not in (None, 0):
        return "droid_failed"
    return "ok"