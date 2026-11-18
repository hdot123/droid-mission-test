# Handoff: euclid-tools (sub-issue #368)

## What was requested
Process card #368 under work order #348 (round 40 · concurrent E unit): implement `euclid.py` as a new file with three functions, plus a new `tests/test_euclid.py`, creating **only** those two files and not modifying any existing file.

Spec (verbatim requirements):
- `gcd(a: int, b: int) -> int` — greatest common divisor, always non-negative (negative inputs counted by absolute value); `gcd(0, 0)` is `0`.
- `lcm(a: int, b: int) -> int` — least common multiple, always non-negative; returns `0` if either input is `0`.
- `is_coprime(a: int, b: int) -> bool` — `True` when the two numbers' gcd is 1.
- Standard library only; must not import `caesar` or `vigenere`.
- Each of the ten acceptance points must have a corresponding test case in `tests/test_euclid.py`.

## What I did
- Created `euclid.py`:
  - `gcd` uses the iterative Euclidean algorithm on `abs(a), abs(b)`, so negatives are treated by magnitude and `gcd(0, 0)` naturally returns `0`.
  - `lcm` takes absolute values, returns `0` when either input is `0`, otherwise computes `a // gcd(a, b) * b` (division first to avoid overflow and keep the result exact and non-negative).
  - `is_coprime` returns `gcd(a, b) == 1`.
- Created `tests/test_euclid.py` with ten tests, one per acceptance point:
  - `test_gcd_basic` → `gcd(48, 36) == 12`
  - `test_gcd_negative_input` → `gcd(-48, 36) == 12`
  - `test_gcd_with_zero` → `gcd(0, 5) == 5`
  - `test_gcd_zero_zero` → `gcd(0, 0) == 0`
  - `test_gcd_coprime` → `gcd(17, 5) == 1`
  - `test_lcm_basic` → `lcm(4, 6) == 12`
  - `test_lcm_zero` → `lcm(0, 7) == 0`
  - `test_lcm_negative_input` → `lcm(-4, 6) == 12`
  - `test_is_coprime_true` → `is_coprime(8, 9) is True`
  - `test_is_coprime_false` → `is_coprime(8, 12) is False`

## What I did NOT do
- Did not modify, move, or delete any pre-existing file (including `roman.py`, `legacy_stringkit.py`, `tests/test_roman.py`, README, or anything under `.github/`).
- Did not implement `caesar.py`, `vigenere.py`, or their tests (owned by other process cards).
- Did not import `caesar` or `vigenere` from `euclid.py` (no cross-module imports at all; standard library only, in fact no imports beyond the module docstring).
- Did not commit or push anything.

## Checks run and results
From the repository root `/home/runner/work/droid-mission-test/droid-mission-test`:

1. `python3 -m pytest tests/test_euclid.py -q` → **10 passed** (`..........  [100%]  10 passed in 0.02s`)
2. `python3 -m pytest tests/ -q` → **21 passed** (`.....................  [100%]  21 passed in 0.04s`) — full suite including the pre-existing `tests/test_roman.py` (11 tests).

Note: `pytest` was not initially installed in the environment (`No module named pytest`); I installed it with `python3 -m pip install pytest` (pytest 9.2.0) to run the required checks. This installed a tool only, no repository files were touched by the install.

## What the validator must pay attention to
- The environment's default `python3` initially lacked pytest; if the validator re-runs checks in a fresh environment, pytest must be available (installed via pip).
- Full-suite count is 21 tests (11 pre-existing roman + 10 new euclid); any drop in that count means a file was lost or modified.
- `git status` after this card should show exactly three new untracked paths relative to base: `euclid.py`, `tests/test_euclid.py`, plus the two team files `team/handoffs/euclid-tools.md` and `team/status/euclid-tools.json`. No tracked file should show as modified.
