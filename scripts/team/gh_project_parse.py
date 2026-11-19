"""Shared unwrap + pagination for `gh project * --format json` envelopes (batch-1 / W-1, W-8).

Supported envelopes (recorded in tests/fixtures/gh_project/):
- item-list: list[...] | {"items": [...], "totalCount": N}
- field-list: list[...] | {"fields": [...], "totalCount": N}
- view: flat project object {"id", "number", "title", ...} (no list wrapper)

Explicitly **not** handled here (different `gh` subcommands / shapes):
- `gh run view`, `gh api` workflow run payloads, REST `runs` total_count — use their own parsers.
- `gh project list` (projects[] envelope) — no in-repo consumer yet.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Protocol


class GhRunner(Protocol):
    def __call__(self, args: list[str], token: str) -> Any: ...


@dataclass(frozen=True)
class ItemListEnvelope:
    items: list[dict[str, Any]]
    total_count: int | None


@dataclass(frozen=True)
class FieldListEnvelope:
    fields: list[dict[str, Any]]
    total_count: int | None


def loads_gh_stdout(stdout: str | None, *, default: Any) -> Any:
    """Parse JSON from gh stdout; empty output yields `default`."""
    raw = (stdout or "").strip()
    if not raw:
        return default
    return json.loads(raw)


def parse_project_item_list(payload: Any) -> list[dict[str, Any]]:
    """Normalize `gh project item-list` JSON into a list of items (W-1)."""
    return unwrap_item_list_envelope(payload).items


def unwrap_item_list_envelope(payload: Any) -> ItemListEnvelope:
    if isinstance(payload, list):
        return ItemListEnvelope(items=payload, total_count=len(payload))
    if isinstance(payload, dict):
        items = payload.get("items")
        if not isinstance(items, list):
            items = []
        total = payload.get("totalCount")
        if isinstance(total, int):
            return ItemListEnvelope(items=items, total_count=total)
        return ItemListEnvelope(items=items, total_count=None)
    return ItemListEnvelope(items=[], total_count=None)


def parse_project_field_list(payload: Any) -> list[dict[str, Any]]:
    """Normalize `gh project field-list` JSON into a list of fields (W-8)."""
    return unwrap_field_list_envelope(payload).fields


def unwrap_field_list_envelope(payload: Any) -> FieldListEnvelope:
    if isinstance(payload, list):
        return FieldListEnvelope(fields=payload, total_count=len(payload))
    if isinstance(payload, dict):
        fields = payload.get("fields")
        if not isinstance(fields, list):
            fields = []
        total = payload.get("totalCount")
        if isinstance(total, int):
            return FieldListEnvelope(fields=fields, total_count=total)
        return FieldListEnvelope(fields=fields, total_count=None)
    return FieldListEnvelope(fields=[], total_count=None)


def parse_project_view(payload: Any) -> dict[str, Any]:
    """Normalize `gh project view --format json` (flat object)."""
    if isinstance(payload, dict):
        return payload
    raise ValueError("gh project view JSON must be an object")


DEFAULT_ITEM_PAGE_SIZE = 100
MAX_ITEM_LIST_LIMIT = 10_000


def fetch_project_items(
    run_gh: GhRunner,
    *,
    owner: str,
    project_number: int,
    token: str,
    page_size: int = DEFAULT_ITEM_PAGE_SIZE,
) -> list[dict[str, Any]]:
    """Fetch all project items; refetch with a higher --limit when gh truncates (W-1 tail)."""
    if page_size < 1:
        raise ValueError("page_size must be >= 1")

    limit = min(page_size, MAX_ITEM_LIST_LIMIT)

    def call_item_list(request_limit: int) -> ItemListEnvelope:
        r = run_gh(
            [
                "project",
                "item-list",
                str(project_number),
                "--owner",
                owner,
                "--format",
                "json",
                "--limit",
                str(request_limit),
            ],
            token,
        )
        if r.returncode != 0:
            raise RuntimeError((r.stderr or r.stdout or "item-list failed").strip())
        data = loads_gh_stdout(r.stdout, default={})
        return unwrap_item_list_envelope(data)

    env = call_item_list(limit)
    total = env.total_count
    if total is not None and len(env.items) < total:
        need = min(total, MAX_ITEM_LIST_LIMIT)
        if need > limit:
            env = call_item_list(need)
            if len(env.items) < total and len(env.items) == need and need < total:
                raise RuntimeError(
                    f"item-list truncated at {len(env.items)} items "
                    f"(totalCount={total}, max_limit={MAX_ITEM_LIST_LIMIT})"
                )
    return env.items


def fetch_project_fields(
    run_gh: GhRunner,
    *,
    owner: str,
    project_number: int,
    token: str,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """Fetch project fields via field-list with envelope unwrap (W-8)."""
    r = run_gh(
        [
            "project",
            "field-list",
            str(project_number),
            "--owner",
            owner,
            "--format",
            "json",
            "--limit",
            str(limit),
        ],
        token,
    )
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "field-list failed").strip())
    data = loads_gh_stdout(r.stdout, default=[])
    env = unwrap_field_list_envelope(data)
    if env.total_count is not None and len(env.fields) < env.total_count and limit < env.total_count:
        r2 = run_gh(
            [
                "project",
                "field-list",
                str(project_number),
                "--owner",
                owner,
                "--format",
                "json",
                "--limit",
                str(min(env.total_count, MAX_ITEM_LIST_LIMIT)),
            ],
            token,
        )
        if r2.returncode != 0:
            raise RuntimeError((r2.stderr or r2.stdout or "field-list failed").strip())
        data = loads_gh_stdout(r2.stdout, default=[])
        env = unwrap_field_list_envelope(data)
    return env.fields


def fetch_project_id(
    run_gh: GhRunner,
    *,
    owner: str,
    project_number: int,
    token: str,
) -> str:
    r = run_gh(
        ["project", "view", str(project_number), "--owner", owner, "--format", "json"],
        token,
    )
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "project view failed").strip())
    view = parse_project_view(loads_gh_stdout(r.stdout, default={}))
    project_id = view.get("id")
    if not project_id:
        raise RuntimeError("project id missing from view")
    return str(project_id)