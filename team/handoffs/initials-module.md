# Handoff: initials-module (sub-issue #33)

## What was requested
Implement `initials(name)` in `initials.py` (repo root) plus `tests/test_initials.py`, per work order #30 and process card `initials-module`:
- Split the name on spaces or hyphens, uppercase each word's first letter, join with dots, end with a trailing dot.
- Examples: `initials("ada lovelace")` -> `"A.L."`, `initials("jean-luc picard")` -> `"J.L.P."`.
- `initials("")` returns `""`.
- Standard library only; no CLI, no `__main__` block, no package directory, no imports of other project modules.
- Test file must only test `initials`.

## What I did
- Created `initials.py` with a single `initials(name: str) -> str` function: empty string short-circuits to `""`; otherwise replaces hyphens with spaces, splits on whitespace, and joins each word's first character uppercased plus a dot.
- Created `tests/test_initials.py` with three pytest tests: the `ada lovelace` example, the `jean-luc picard` example, and the empty-string case.

## What I did not do
- Did not touch `hexcodec.py`, `tally.py`, or any test file other than `tests/test_initials.py`.
- Did not add a CLI, package directory, or cross-module imports.
- Did not commit or push.

## Checks run and results
- `python -m pytest -q tests/test_initials.py` initially failed with "No module named pytest" (no pytest on the system interpreter).
- Installed pytest via `python3 -m pip install pytest`, then ran `python3 -m pytest -q tests/test_initials.py` -> **3 passed in 0.01s** (exit code 0).

## Notes for the validator
- The env check should use `python -m pytest -q` (or `python3`); pytest had to be pip-installed into this environment before any test could run, so a fresh environment may hit the same "No module named pytest" failure until it is installed.
- `initials` tolerates repeated/edge whitespace: empty tokens after splitting are skipped, so e.g. `initials("ada  lovelace")` also yields `"A.L."`. Spec examples and the empty-string case behave exactly as specified.
- The work order's `tally.py` verdict-line discrepancy (body says >= 60, acceptance says 70) belongs to the `tally-module` process, not this one.
