# Handoff: implement-volconv (sub-issue #492)

## What was requested
Process card `implement-volconv` under work order #480 (round 46, unit C): implement
`volconv.py` with `convert(value, from_unit, to_unit) -> float`, using liters as the
pivot unit and exactly the pinned unit-to-liter factors, plus `tests/test_volconv.py`
covering every acceptance item. Scope limited to those two files (plus this handoff and
the status JSON); standard library only; no import of `crt` or `xorcipher`.

## What I did
- Created `volconv.py`:
  - `_FACTORS` dict with exactly the pinned factors: L=1, mL=0.001, m3=1000,
    cm3=0.001, gal=3.785411784, qt=0.946352946, pt=0.473176473,
    floz=0.0295735295625, cup=0.2365882365, tbsp=0.01478676478125,
    tsp=0.00492892159375.
  - `convert(value, from_unit, to_unit)`:
    - `value`: rejects `bool` (checked before `int`, since `bool` subclasses `int`),
      accepts only `int`/`float`, else `TypeError`.
    - unknown/non-string units (either argument) raise `ValueError`.
    - returns `value * (factor[from] / factor[to])`, a float.
- Created `tests/test_volconv.py`: one test per acceptance item (13 acceptance groups),
  with `TOL = 1e-9` used for the tolerance-based assertions.

## What I did not do
- Did not create or modify `crt.py`, `xorcipher.py`, `tests/test_crt.py`,
  `tests/test_xorcipher.py`, or any pre-existing file.
- Did not add conftest/pytest config (none exists; bare module import works when
  pytest is invoked from the repo root, matching how `tests/test_roman.py` imports
  `roman`).
- Did not commit or push.

## Environment note
The checkout had no pytest (`python3 -m pytest` reported "No module named pytest").
I installed it non-root into the user site with `python3 -m pip install --user pytest`
(pytest 9.2.0). This does not touch the repository; if the validation runner has its own
pytest, this install is irrelevant.

## Checks run (from repository root)
- `python3 -m pytest tests/test_volconv.py -q` → passed (13 passed).
- `python3 -m pytest tests/ -q` → passed (existing roman + stringkit tests plus
  these; all green).

## Notes for the validator
- Tolerance items use `abs(actual - expected) <= 1e-9`; exact-equality items
  (`gal→L`, `m3→L`, `qt→pt`, `cm3→mL`, `L→L`) use `==` as specified.
- `convert(1, "qt", "pt")` relies on the pinned ratio 0.946352946/0.473176473;
  verified to equal exactly 2.0 in binary float.
- `bool` rejection is explicit; `convert(True, "L", "mL")` raises `TypeError`.
- Full-suite result reflects this checkout only; sibling processes (crt, xorcipher)
  merge separately.
