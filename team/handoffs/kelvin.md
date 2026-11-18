# Handoff: kelvin (sub-issue #426)

## What was requested

Implement the kelvin temperature-conversion component from work order #410 (round 43 · track D), owning exactly two new files:

- `kelvin.py` with four functions:
  - `c_to_k(c: float) -> float` = `c + 273.15`
  - `k_to_c(k: float) -> float` = `k - 273.15`, raising `ValueError` when `k < 0`
  - `c_to_f(c: float) -> float` = `c * 9/5 + 32`
  - `f_to_c(f: float) -> float` = `(f - 32) * 5/9`
- `tests/test_kelvin.py` with a test case for every acceptance item, all with floating-point tolerance `1e-9`:
  - `abs(c_to_k(0) - 273.15) < 1e-9`
  - `abs(c_to_k(100) - 373.15) < 1e-9`
  - `abs(k_to_c(273.15) - 0.0) < 1e-9`
  - `abs(c_to_f(0) - 32.0) < 1e-9`
  - `abs(c_to_f(100) - 212.0) < 1e-9`
  - `abs(f_to_c(32) - 0.0) < 1e-9`
  - `abs(f_to_c(212) - 100.0) < 1e-9`
  - `k_to_c(-1)` raises `ValueError`
  - `c_to_f` / `f_to_c` round-trip identity at 37.0 °C

Constraints: new files only, standard library only, no imports from `dms` or `bytefmt`, no modification of any existing file.

## What I did

- Created `kelvin.py` (new file): the four conversion functions per spec. `k_to_c` guards `k < 0` with a `ValueError` before subtraction.
- Created `tests/test_kelvin.py` (new file): 9 test functions, one per acceptance item above, each asserting with `1e-9` tolerance (or `pytest.raises(ValueError)` for the negative-Kelvin case). Imports only `pytest` and `kelvin`.

## What I did not do

- Did not touch `dms.py`, `bytefmt.py`, or their tests (owned by other processes).
- Did not modify any existing file (including `roman.py`, `legacy_stringkit.py`, existing tests, `README.md`).
- Did not add any dependencies beyond `pytest` (test runner only; implementation is pure standard library).
- Did not commit or push.

## Checks run and results

- `python3 -m pytest tests/test_kelvin.py -q` → **9 passed** (0.02s)
- `python3 -m pytest tests/ -q` → **20 passed** (0.03s) — full suite, includes pre-existing `roman` / `legacy_stringkit` tests, all green.

Note: `pytest` was not installed in the environment initially (`No module named pytest`); I installed it with `python3 -m pip install pytest` (pytest 9.2.0) to run the checks. This does not affect repository files.

## For the validator to pay attention to

- The full-suite result (20 passed) was measured before the other processes' files landed in this worktree; after merge, re-run `python3 -m pytest tests/ -q` against the combined tree as the acceptance criteria state.
- Round-trip at 37.0 °C is asserted both as `f_to_c(c_to_f(37.0)) ≈ 37.0` (tolerance 1e-9); all other assertions use the exact expressions from the work order.
- `k_to_c` rejects only `k < 0`; `k == 0` is valid (absolute zero → −273.15 °C) and is not covered by an explicit work-order item, but follows directly from the spec formula.
- Ownership boundary held: only `kelvin.py`, `tests/test_kelvin.py`, `team/handoffs/kelvin.md`, and `team/status/kelvin.json` were written.
