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
    rb = role_budget(wall, role)
    # Role defaults come from default_budgets() merge — no silent 600 for validator.
    if "droid_wall_sec" not in rb:
        raise ValueError(f"budgets.roles.{role}.droid_wall_sec missing after merge")
    return int(rb["droid_wall_sec"])


def adopt_reserve_sec(wall: dict[str, Any] | None, role: str = "validator") -> int:
    rb = role_budget(wall, role)
    if role == "validator":
        if "adopt_reserve_sec" not in rb:
            raise ValueError("budgets.roles.validator.adopt_reserve_sec missing after merge")
        return int(rb["adopt_reserve_sec"])
    return int(rb.get("adopt_reserve_sec", 0))


def validator_session_budget(wall: dict[str, Any] | None) -> tuple[int, int]:
    """Return (droid_wall_sec, adopt_reserve_sec) from wall config."""
    rb = role_budget(wall, "validator")
    return int(rb["droid_wall_sec"]), int(rb["adopt_reserve_sec"])


def job_wall_min(wall: dict[str, Any] | None, role: str) -> int:
    return int(role_budget(wall, role)["job_wall_min"])


# ForemanRun `budgets.roles.validator.job_wall_min` (12) is the contractual slice
# for droid+adopt budgeting. GitHub Actions `timeout-minutes: 15` is a wider
# platform job envelope (precheck/droid/merge/adopt/upload); do not conflate them.
GITHUB_VALIDATE_JOB_TIMEOUT_MIN = 15


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


def adopt_session_completion_status(droid_exit: int | None) -> str:
    """Adopt step: no recorded exit means the validator droid session never started."""
    if droid_exit is None:
        return "missing_output"
    return session_completion_status(droid_exit)