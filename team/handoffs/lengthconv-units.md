# Handoff: lengthconv-units (sub-issue #441)

## What was requested

Process card `lengthconv-units` under work order #431 (Round 44 · batch B): implement
`lengthconv.py` at the repository root and `tests/test_lengthconv.py`, owning exactly
those two files. Implement `convert(value, from_unit, to_unit) -> float` converting via
meters as the pivot. Unit table: mm, cm, m, km, in, ft, yd, mi with exact meter
definitions in = 0.0254, ft = 0.3048, yd = 0.9144, mi = 1609.344, mm = 0.001,
cm = 0.01, km = 1000. `value` must be numeric with bool excluded (True/False raise
TypeError, strings raise TypeError). Unknown units raise ValueError. All 15 acceptance
items must each have a corresponding test case. Standard library only; no imports of
columnar/primepi. No pre-existing file may be modified.

## What I did

- Created `lengthconv.py`: `convert()` validates the value type (rejecting bool and
  non-numbers with TypeError) and both units (ValueError if absent), converts through
  meters, returns a float.
- Conversion arithmetic uses `fractions.Fraction` with the exact meter factors (e.g.
  in = 254/1000), so mathematically exact results (12 in -> 1.0 ft, 2.54 cm -> 1.0 in,
  3 ft -> 36.0 in, 5280 ft -> 1.0 mi, 1760 yd -> 1.0 mi, identity and zero cases) come
  out bit-exact rather than off by ~1e-16 from naive float chaining. Float inputs are
  converted via `Fraction(str(value))` to preserve their decimal value.
- Created `tests/test_lengthconv.py` with one test per acceptance item: 12 value
  checks (km->m, m->mm, cm->m, in->ft, mi->km approx, ft->mi, yd->m approx, cm->in,
  m->m, 0 km->mi, ft->in, yd->mi), 2 unknown-unit ValueError cases (parsec target,
  furlong source), 1 TypeError case ("1" string), plus a bool-rejection test for the
  card's explicit bool-exclusion requirement (16 tests total).

## What I did not do

- Did not create `columnar.py`, `primepi.py`, or their tests (other processes own them).
- Did not modify any pre-existing file (`README.md`, `roman.py`, `legacy_stringkit.py`,
  existing tests, `team/` or `.github/` paths owned by others).
- Did not import the other two modules; implementation is standard library only.
- Did not commit or push.

## Checks run

- `python3 -m pytest tests/test_lengthconv.py -q` -> 16 passed (exit 0).
- `python3 -m pytest tests/ -q` -> 27 passed (exit 0), which includes the 11 baseline
  tests from `test_roman.py` and `test_legacy_stringkit.py` plus 16 new ones.
- Note: pytest was not installed in the environment; I installed it with pip
  (`pip3 install pytest`, pytest 9.2.0) to run the required checks. No repo files were
  affected by that.

## Notes for the validator

- Exact-equality acceptance items (`== 1.0`, `== 36.0`, etc.) pass because conversion
  is done in exact rationals; a naive float implementation fails three of them
  (12 in -> ft, 2.54 cm -> in, 3 ft -> in) with 1e-16-level error. The approx items
  (mi -> km, yd -> m) pass well within the 1e-9 tolerance.
- Bool rejection (`convert(True, ...)`) raises TypeError as required; it has its own
  test in addition to the 15 verbatim acceptance items.
- Only the two deliverable files plus the two team files listed in the card were added.
