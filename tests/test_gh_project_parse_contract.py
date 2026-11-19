"""Contract tests for gh_project_parse (batch-1: W-1, W-8, pagination)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures" / "gh_project"
sys.path.insert(0, str(ROOT / "scripts" / "team"))

from gh_project_parse import (  # noqa: E402
    fetch_project_fields,
    fetch_project_id,
    fetch_project_items,
    parse_project_field_list,
    parse_project_item_list,
    parse_project_view,
    unwrap_field_list_envelope,
    unwrap_item_list_envelope,
)
import project_state_write  # noqa: E402


def _load(name: str):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


REGISTERED_FIXTURES = (
    "item_list_envelope.json",
    "item_list_legacy_array.json",
    "field_list_envelope.json",
    "project_view.json",
    "item_list_truncated_page.json",
)


@pytest.mark.parametrize("fixture_name", REGISTERED_FIXTURES)
def test_fixture_files_exist(fixture_name: str):
    assert (FIX / fixture_name).is_file()


def test_w1_item_list_envelope_fixture():
    items = parse_project_item_list(_load("item_list_envelope.json"))
    assert len(items) == 1
    assert items[0]["content"]["number"] == 661


def test_w8_field_list_envelope_fixture():
    fields = parse_project_field_list(_load("field_list_envelope.json"))
    assert len(fields) == 1
    assert fields[0]["name"] == "Status"


def test_w8_bare_dict_breaks_pick_status_without_parse():
    """Reproduces round-48 C/D: field-list envelope passed as list consumer."""
    envelope = _load("field_list_envelope.json")
    with pytest.raises(AttributeError):
        project_state_write.pick_status_option(envelope, "已验收")


def test_w8_pick_status_after_parse():
    fields = parse_project_field_list(_load("field_list_envelope.json"))
    fid, oid = project_state_write.pick_status_option(fields, "已验收")
    assert fid == "PVTF_lACO"
    assert oid == "OPTION_pass"


def test_project_view_parse():
    view = parse_project_view(_load("project_view.json"))
    assert view["number"] == 33
    assert view["id"].startswith("PVT_")


def test_item_list_pagination_refetch():
    calls: list[int] = []

    def fake_gh(args, token):
        assert token == "tok"
        limit_idx = args.index("--limit")
        req_limit = int(args[limit_idx + 1])
        calls.append(req_limit)
        if req_limit < 250:
            body = json.dumps(_load("item_list_truncated_page.json"))
        else:
            body = json.dumps(
                {
                    "items": [{"id": f"PVTI_{i}", "content": {"number": i}} for i in range(1, 251)],
                    "totalCount": 250,
                }
            )
        return subprocess.CompletedProcess(args, 0, body, "")

    items = fetch_project_items(fake_gh, owner="hdot123", project_number=33, token="tok", page_size=100)
    assert len(items) == 250
    assert calls == [100, 250]


def test_field_list_envelope_metadata():
    env = unwrap_field_list_envelope(_load("field_list_envelope.json"))
    assert env.total_count == 1
    assert len(env.fields) == 1


def test_item_list_envelope_metadata():
    env = unwrap_item_list_envelope(_load("item_list_truncated_page.json"))
    assert env.total_count == 250
    assert len(env.items) == 1


def test_lint_gh_project_parse_gate():
    lint = ROOT / "scripts" / "team" / "lint_gh_project_parse.py"
    r = subprocess.run([sys.executable, str(lint)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr + r.stdout


def test_w1_find_item_reads_items_from_dict():
    calls = {"n": 0}

    def fake_gh(args, token):
        calls["n"] += 1
        if "item-list" in args:
            body = json.dumps(_load("item_list_envelope.json"))
            return subprocess.CompletedProcess(args, 0, body, "")
        body = json.dumps(_load("project_view.json"))
        return subprocess.CompletedProcess(args, 0, body, "")

    with patch.object(project_state_write, "_gh", fake_gh):
        item_id, project_id = project_state_write.find_item_and_project(
            "hdot123", 33, 661, "token"
        )
    assert item_id == "PVTI_lACOAA"
    assert project_id == "PVT_kwDOVwPK-s4BDIxx"


def test_fetch_project_fields_uses_envelope():
    def fake_gh(args, token):
        return subprocess.CompletedProcess(
            args, 0, json.dumps(_load("field_list_envelope.json")), ""
        )

    fields = fetch_project_fields(fake_gh, owner="hdot123", project_number=33, token="t")
    assert fields[0]["options"][0]["name"] == "已验收"


def test_fetch_project_id():
    def fake_gh(args, token):
        return subprocess.CompletedProcess(args, 0, json.dumps(_load("project_view.json")), "")

    assert (
        fetch_project_id(fake_gh, owner="hdot123", project_number=33, token="t")
        == "PVT_kwDOVwPK-s4BDIxx"
    )