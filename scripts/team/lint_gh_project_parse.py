#!/usr/bin/env python3
"""CI lint: `gh project` JSON must go through gh_project_parse (batch-1 gate)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TEAM = Path(__file__).resolve().parent
ALLOWLIST = {
    "gh_project_parse.py",
    "lint_gh_project_parse.py",
}

# Subcommand token after literal "project" in gh argv lists / comments.
PROJECT_SUBCMD = re.compile(
    r'["\']project["\']\s*,\s*["\'](item-list|field-list|view)["\']'
    r'|gh\s+project\s+(item-list|field-list|view)\b'
)

BARE_JSON_LOADS = re.compile(r"\bjson\.loads\s*\(")

PARSE_LAYER_SYM = re.compile(
    r"\b(?:"
    r"gh_project_parse|"
    r"loads_gh_stdout|"
    r"parse_project_item_list|"
    r"parse_project_field_list|"
    r"parse_project_view|"
    r"unwrap_item_list_envelope|"
    r"unwrap_field_list_envelope|"
    r"fetch_project_items|"
    r"fetch_project_fields|"
    r"fetch_project_id"
    r")\b"
)


def scan_file(path: Path) -> list[str]:
    if path.name in ALLOWLIST:
        return []
    text = path.read_text(encoding="utf-8")
    early = "item-list" in text or "field-list" in text or "gh project view" in text
    if not early and not PROJECT_SUBCMD.search(text):
        return []
    errs: list[str] = []
    if (
        PROJECT_SUBCMD.search(text)
        and BARE_JSON_LOADS.search(text)
        and not PARSE_LAYER_SYM.search(text)
    ):
        errs.append(
            f"{path.relative_to(path.parents[2])}: "
            f"gh project * JSON must use gh_project_parse (found bare json.loads)"
        )
    return errs


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--team-dir", default=str(TEAM))
    args = p.parse_args()
    team = Path(args.team_dir)
    errors: list[str] = []
    for py in sorted(team.glob("*.py")):
        errors.extend(scan_file(py))
    if errors:
        print("lint gh_project_parse failures:", *errors, sep="\n", file=sys.stderr)
        return 1
    print("lint gh_project_parse ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
