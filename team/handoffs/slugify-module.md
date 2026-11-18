# Handoff: slugify-module (sub-issue #327)

## What was requested
Process card "slugify-module": implement an ASCII URL slugifier per the work order #315 (round 38, concurrent batch D). Scope limited to two new files only:

- `slugify.py` — `slugify(text: str) -> str`
- `tests/test_slugify.py` — test cases covering every acceptance example

Spec (verbatim): 先转小写；只保留 ASCII 字母与数字，其余每个连续非字母数字段折为一个 `-`；去掉首尾 `-`；结果可为空串。非 ASCII 字母（如 é）按非字母数字处理（本轮口径，不做音译）。

## What I did
- Created `slugify.py` with a standard-library-only implementation: lowercase, then regex-substitute every run of non-`[a-z0-9]` characters with a single `-`, then strip leading/trailing `-`. Non-ASCII letters (e.g. `é` in "café") match the non-alphanumeric class and act as separators, so `slugify("café") == "caf"` per the round's ASCII-only rule (no transliteration).
- Created `tests/test_slugify.py` with 6 test cases covering all required acceptance points plus empty input:
  - `slugify("Hello, World!") == "hello-world"`
  - `slugify("  A  B  ") == "a-b"`
  - `slugify("!!!") == ""`
  - `slugify("café") == "caf"`
  - `slugify("already-slug") == "already-slug"`
  - `slugify("") == ""`

## What I did not do
- Did not touch any existing file (README.md, legacy_stringkit.py, roman.py, tests/*, worker files, etc.).
- Did not create or edit `wordwrap.py`, `csvfield.py`, or their tests (owned by other process cards).
- Did not import wordwrap or csvfield; implementation uses only the standard library (`re`).
- Did not commit or push.

## Checks run
From repository root:
1. `python3 -m pytest tests/test_slugify.py -q` → `6 passed in 0.01s`
2. `python3 -m pytest tests/ -q` → `17 passed in 0.02s` (all existing tests plus mine)

Note: `pytest` was not preinstalled in this environment; I installed it with `pip3 install pytest` (pytest 9.2.0). No project files were affected.

## For the validator
- Both owned files are new; `git status` should show only `slugify.py` and `tests/test_slugify.py` added by this process, alongside the two team files (`team/handoffs/slugify-module.md`, `team/status/slugify-module.json`).
- The `café` case intentionally yields `"caf"` (non-ASCII treated as separator, no transliteration) — this is the specified behavior for this round, not a bug.
- The regex collapses *every* run of non-alphanumerics into one `-`, then strips edge `-`, which satisfies both the multi-space and punctuation-only cases.
