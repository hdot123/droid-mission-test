#!/usr/bin/env python3
"""CI lint: ban legacy replan gates and half-upload patterns."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FORBIDDEN = [
    (re.compile(r"failed_processes\s*!=\s*['\"]\\?\\[\\]['\"]"), "string compare failed_processes != '[]'"),
    (re.compile(r"needs\.validate\.result\s*==\s*['\"]success['\"]"), "replan bound to validate.result success only"),
    (re.compile(r"fail_text\s*=\s*\{"), "static fail_text fallback in assemble"),
    (re.compile(r'备料未启动'), "forbidden static phrase 备料未启动 in workflow"),
]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--workflow", default=".github/workflows/team.yml")
    args = p.parse_args()
    text = Path(args.workflow).read_text(encoding="utf-8")
    errors: list[str] = []
    for rx, msg in FORBIDDEN:
        if rx.search(text):
            errors.append(msg)
    for m in re.finditer(r"- name: Upload verdict artifact", text):
        chunk = text[m.start() : m.start() + 400]
        if re.search(r"if:\s*always\(\)", chunk):
            errors.append("validate upload uses if: always() without wall gate")
    if errors:
        print("lint failures:", *errors, sep="\n", file=sys.stderr)
        return 1
    print("workflow foreman lint ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())