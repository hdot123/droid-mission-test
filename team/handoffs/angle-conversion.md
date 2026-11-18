# Handoff: angle-conversion (sub-issue #398)

## What was requested
Process card "角度换算 angle.py" for work order #383 (第四十二轮 · 并发 D 单). Create only `angle.py` and `tests/test_angle.py` (new files), implementing:

- `deg2rad(d: float) -> float` — degrees to radians (`math.radians`).
- `rad2deg(r: float) -> float` — radians to degrees (`math.degrees`).
- `normalize_deg(d: float) -> float` — normalize into [0, 360) (`d % 360`, returns float).

All nine acceptance items must have corresponding test cases. Standard library only; no imports from `julian` or `bcd`. No existing files may be modified. No commits.

## What I did
- Created `angle.py` with the three functions (imports only `math` from the standard library).
- Created `tests/test_angle.py` with one test per acceptance item (9 tests):
  - tolerance assertions for `deg2rad(180)`, `deg2rad(90)`, `deg2rad(45)`, `rad2deg(pi)`; exact equality for `normalize_deg(370)`, `normalize_deg(-10)`, `normalize_deg(720)`, `normalize_deg(360)`, `normalize_deg(0)`.
- Wrote this handoff and `team/status/angle-conversion.json`.

## What I did not do
- Did not touch `julian.py`, `bcd.py`, `tests/test_julian.py`, `tests/test_bcd.py`, or any other existing file.
- Did not modify `roman.py`, `legacy_stringkit.py`, or existing tests.
- Did not import from `julian` or `bcd`; did not add third-party dependencies.
- Did not commit or push.

## Checks run and results
- `python3 -m pytest tests/test_angle.py -q` — PASSED (9 passed in 0.01s).
- `python3 -m pytest tests/ -q` — PASSED (20 passed in 0.02s; 9 new angle tests + 11 pre-existing `roman`/`legacy_stringkit` tests).

Note: pytest was not installed in the environment's system Python; I installed it via `pip3 install --user pytest` (pytest 9.2.0) to run the checks. No repository files were changed by that install.

## What the validator must pay attention to
- `normalize_deg` returns a `float` (wrapped in `float(...)`); `d % 360` on a float input already yields float, but on a float-typed annotation the result is always float. `normalize_deg(0) == 0.0` holds because `0.0 == 0` in Python.
- Tolerance assertions are `< 1e-12` exactly as specified.
- All nine acceptance items map 1:1 to named test functions; nothing else is tested (no extra scope).
- Files are new-only; git status should show them as untracked additions alongside the other D-unit files.
