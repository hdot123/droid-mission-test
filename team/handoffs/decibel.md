# Handoff: decibel (sub-issue #919)

## What was requested

Process card #919 under work order #903 (round 57, C-unit: josephus / decibel / circle).
Implement the decibel conversion module and its tests, creating exactly two new files:

- `decibel.py` (repo root)
- `tests/test_decibel.py`

Spec (verbatim from the work order):

- `power_ratio_to_db(ratio)` = 10·log10(ratio); `db_to_power_ratio(db)` = 10^(db/10);
  `amplitude_ratio_to_db(ratio)` = 20·log10(ratio); `db_to_amplitude_ratio(db)` = 10^(db/20).
- Inputs: ratio ≤ 0 raises ValueError; non-numeric (including bool) raises TypeError
  (same for db inputs).
- Float acceptance relative tolerance 1e-9.
- Power quantities use 10·log10, amplitude quantities use 20·log10; constants must not be mixed.

## What I did

- Created `decibel.py` at the repo root: four conversion functions over `math`, with shared
  private validators. `_require_number` rejects bool and any non-int/float with TypeError
  (before any comparison, so `power_ratio_to_db("2")` and `db_to_power_ratio("3")` raise
  TypeError, not TypeError-from-comparison); `_require_positive` then raises ValueError for
  ratio ≤ 0. db inputs accept any numeric (negative db is valid).
- Created `tests/test_decibel.py` with a test case for every acceptance point, using
  `pytest.approx(..., rel=1e-9)` throughout: the 10 named value checks (3.0102999566398121,
  6.020599913279624, 10.0, 20.0, 0.0, -3.0102999566398121, round trips, etc.), parametrized
  round-trip identity properties for both power and amplitude, the
  `amplitude_ratio_to_db(x) ≈ 2 * power_ratio_to_db(x)` property, the three ValueError cases,
  and the required TypeError cases (string, bool for both ratio and db entry points).

## What I did not do

- Did not create or touch `josephus.py`, `circle.py`, or their tests (owned by sibling cards).
- Did not modify, move, or delete any existing file.
- Did not import josephus or circle; standard library only (`math`).
- Did not commit or push.
- No `verdict.json` / `verdict.md` by-products appeared; nothing to delete.

## Checks run (from repo root, verbatim)

- `python3 -m pytest tests/test_decibel.py -q` → **41 passed in 0.03s**
- `python3 -m pytest tests/ -q` → **383 passed, 2 skipped in 19.54s** (exit code 0)

## Notes for the validator

- Every acceptance bullet has a corresponding named test in `tests/test_decibel.py`; all
  float assertions use `rel=1e-9`.
- Bool is rejected with TypeError for ratio inputs (e.g. `power_ratio_to_db(True)`);
  negative db values are legal for `db_to_*` (only the ratio direction is constrained to > 0).
- The two skipped tests in the full run are pre-existing, unrelated to this card.
- Scope: only `decibel.py`, `tests/test_decibel.py`, and this card's two team files.
