# Handoff: versioncmp-module (sub-issue #167)

## What was requested
Implement `versioncmp.py` with a single function `compare(a, b)` that compares two
dot-separated numeric version strings and returns `-1` (a < b), `0` (equal), or
`1` (a > b):
- compare segment by segment as integers;
- pad the side with fewer segments with `0`;
- raise `ValueError` if any segment is non-numeric.

Required examples: `compare("1.10", "1.9") -> 1`, `compare("1.0", "1") -> 0`,
`compare("2.0.1", "2.0") -> 1`, `compare("0.9", "1.0") -> -1`.

Constraints: Python standard library only; no package directories; no CLI;
`tests/test_versioncmp.py` must test only this module's behavior.
Scope: this process owns only `versioncmp.py` and `tests/test_versioncmp.py`.

## What I did
- Created `versioncmp.py` implementing `compare(a, b)` per the spec:
  splits on `.`, parses each segment with `int` (non-numeric segments raise
  `ValueError`), pads the shorter side with `0`, then compares the integer
  lists (returns -1/0/1).
- Created `tests/test_versioncmp.py` with 7 tests covering: all four required
  worked examples, trailing-zero padding both directions, equal versions,
  numeric (not lexicographic) ordering (`1.2` < `1.11`, `10.0` > `9.9`), and
  `ValueError` on non-numeric or empty segments.
- Ran the process check verbatim (see below).

## What I did not do
- Did not touch `transpose.py`, `iban.py`, or any other process's files.
- Did not create package directories, `__init__.py`, or any CLI.
- Did not add imports beyond the standard library (tests use only `pytest`).
- Did not commit or push (left to the workflow).

## Checks run and results
1. `python -m pytest -q tests/test_versioncmp.py` — initially failed with
   `No module named pytest` (environment lacked pytest). Installed pytest via
   `python -m pip install -q pytest` (environment setup, no repo files changed),
   then re-ran the same command verbatim:
   `python -m pytest -q tests/test_versioncmp.py` → `7 passed in 0.01s` (exit 0).

## Notes for the validator
- The only environment-level action was installing `pytest`; it is not a repo
  change. The check command itself was run verbatim as required.
- `compare("")` raises `ValueError` (empty string yields one empty segment),
  which is consistent with the "non-numeric segment" rule.
- Files delivered: `versioncmp.py`, `tests/test_versioncmp.py`,
  `team/handoffs/versioncmp-module.md`, `team/status/versioncmp-module.json`.
