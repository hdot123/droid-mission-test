# Handoff: hmsconv (sub-issue #295)

## What was requested
Process card `hmsconv` under work order #280 (round 35, group D): create two new files only —
- `hmsconv.py` — seconds ↔ (hours, minutes, seconds) conversion:
  - `split_seconds(total: int) -> tuple[int, int, int]`: non-negative integer seconds split into (h, m, s), both m and s < 60, hours uncapped; negative input raises `ValueError`.
  - `join_seconds(h: int, m: int, s: int) -> int`: inverse; raises `ValueError` if any component is negative or if m or s >= 60.
- `tests/test_hmsconv.py` — a test case for every acceptance point:
  `split_seconds(3661) == (1, 1, 1)`; `split_seconds(0) == (0, 0, 0)`; `split_seconds(86399) == (23, 59, 59)`; `split_seconds(90061) == (25, 1, 1)`; `join_seconds(1, 1, 1) == 3661`; `join_seconds(0, 60, 0)` raises `ValueError`; round-trip identity for 0, 59, 3600, 90061.

Constraints: only these two files (no edits to any pre-existing file), standard library only, no import of `baseconv`/`rangecompl`.

## What I did
- Created `hmsconv.py` with both functions. `split_seconds` uses `divmod(total, 3600)` then `divmod(rem, 60)`; `join_seconds` validates each component (rejects negatives and m/s >= 60) then computes `h * 3600 + m * 60 + s`. Both also reject non-`int` (including `bool`) inputs with `ValueError` as a defensive measure — the spec only requires ValueError for the listed cases, so this is a superset and cannot fail the stated checks.
- Created `tests/test_hmsconv.py` with one test per acceptance point (13 test items after parametrization), using `pytest.raises(ValueError)` for the error cases and `@pytest.mark.parametrize` for the four round-trip values.

## What I did not do
- Did not create or touch `baseconv.py`, `rangecompl.py`, `tests/test_baseconv.py`, `tests/test_rangecompl.py`, or any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing tests, README, etc.).
- Did not commit or push (workflow handles that).
- No imports beyond `pytest` in the test file and the standard library in the module.

## Checks run (from repository root)
1. `python3 -m pytest tests/test_hmsconv.py -q` → **13 passed**
2. `python3 -m pytest tests/ -q` → **24 passed** (my 13 + 11 pre-existing baseline tests, all green)

Note: `pytest` was not installed in this environment; I installed it via `python3 -m pip install --break-system-packages pytest` (pytest 9.2.0). This is an environment/tooling install only, no repository files were changed by it.

## What the validator must pay attention to
- Environment: pytest had to be installed manually; if the validator runs in a fresh container, pytest may again be missing before the checks can run.
- The full-suite check (`python3 -m pytest tests/ -q`) depends on `baseconv` and `rangecompl` tests passing too — those are other processes' deliverables, so full-suite green is only guaranteed post-merge.
- Behavior details beyond the literal acceptance points: hours are uncapped (e.g. `split_seconds(90061) == (25, 1, 1)`), m/s must be strictly < 60 on input to `join_seconds`, and negative inputs raise `ValueError`. Non-int inputs (including `bool`) also raise `ValueError` — a deliberate superset of the spec.
