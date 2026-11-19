# Handoff: pressureconv (sub-issue #495)

## What was requested

Process card #495 under work order #481 (Round 46 · D): implement `pressureconv.py` with
`convert(value, from_unit: str, to_unit: str) -> float` that converts pressure units using
pascals (Pa) as the intermediary, plus `tests/test_pressureconv.py`. Owns only those two
files. Standard library only; no imports from other deliverables; no modification of any
existing file.

Pinned conversion factors (to Pa): Pa=1, kPa=1000, bar=100000, atm=101325,
psi=6894.757293168, mmHg=133.322387415, torr=133.322387415, inHg=3386.389.

Validation rules: non-numeric `value` (str, None, etc.) raises TypeError; `bool` raises
TypeError (checked first, since `bool` is an `int` subclass); a unit not in the table
raises ValueError.

## What I did

- Created `pressureconv.py`: module-level `_FACTORS` dict of the eight pinned factors;
  `convert()` rejects bool/non-numeric values with TypeError, unknown `from_unit` or
  `to_unit` with ValueError, then computes `value * factor[from] / factor[to]`.
- Created `tests/test_pressureconv.py`: 15 tests covering every acceptance criterion —
  the ten numeric conversions (with `abs=1e-9` tolerance, and `abs=1e-6` for the
  760 mmHg → atm case), both ValueError cases (unknown units), both TypeError cases
  (str, None), plus an extra bool-rejection case.
- Ran the process checks (pytest had to be installed first; see below).

## What I did not do

- Did not touch `ringbuffer.py`, `century.py`, or any other existing file (those belong
  to other process cards).
- Did not modify `roman.py`, `legacy_stringkit.py`, `tests/` pre-existing tests, or any
  file outside my two deliverables plus the two required team files.
- Did not commit or push.
- Did not import anything outside the standard library (none was needed).

## Checks run and results

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_pressureconv.py -q` | 15 passed in 0.02s |
| `python3 -m pytest tests/ -q` | 26 passed in 0.04s (exit 0) |

Note: the environment had no pytest (`No module named pytest`), so I installed it with
`pip3 install pytest` (pytest 9.2.0) to run the required checks. This changed no
repository file.

## Notes for the validator

- Tolerance handling: all numeric assertions use `pytest.approx(..., abs=1e-9)` except
  `convert(760, "mmHg", "atm")`, which uses `abs=1e-6` as specified. Exact-equality
  assertions are used only where the spec demands `==` (atm→Pa, bar→kPa, torr→mmHg,
  Pa→atm, kPa→kPa).
- `bool` rejection: `isinstance(value, bool)` is checked before the int/float check,
  otherwise `True` would silently convert as `1`.
- Unit names are matched exactly (case-sensitive) against the pinned table; `"lb"` and
  `"kg"` are not in it, so they raise ValueError as required.
- Full suite passes alongside the other round-46 deliverables already present in
  `tests/`.
