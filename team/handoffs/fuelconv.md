# Handoff: fuelconv（sub-issue #889）

## What was requested

Process card #889 under work order #879 (第56轮 D 单). Own exactly two new files:

- `fuelconv.py` — `convert_fuel(value, from_unit, to_unit) -> float` for the unit set `{L/100km, mpgUS, mpgImp, km/L}` with reciprocal (倒数式) relations pinned: `mpgUS = 235.214583…/(L/100km)`, `mpgImp = 282.480936…/(L/100km)`, `km/L = 100/(L/100km)`, factors derived from US gallon = 3.785411784 L, imperial gallon = 4.54609 L, mile = 1.609344 km.
- `tests/test_fuelconv.py` — a test case for every acceptance item in the work order.

Input contract: `value <= 0` → `TypeError`-free `ValueError`; non-numeric value (including `bool`) → `TypeError`; unknown unit → `ValueError`. Float acceptance relative error 1e-9.

Constraints: add-only (no existing file modified), standard library only, no imports from jaro/multiset or any other work-order module.

## What I did

- Created `fuelconv.py`:
  - Factors computed from the three defining constants: `_MPG_US = 100.0 * 3.785411784 / 1.609344` (235.214583…), `_MPG_IMP = 100.0 * 4.54609 / 1.609344` (282.480936…), `_KM_PER_L = 100.0`.
  - Conversion is two-step reciprocal: value → canonical `L/100km` (`_to_canonical`) → target unit (`_from_canonical`). Each direction divides by the factor for reciprocal units, so `L/100km → mpgUS` and `mpgUS → L/100km` are true reciprocals, not linear scaling.
  - Validation: `bool` and non-`Real` values raise `TypeError`; `value <= 0` raises `ValueError`; unknown units raise `ValueError` (validated on the `from_unit` side inside `_to_canonical`, which runs after value checks).
  - Returns a plain `float`.
- Created `tests/test_fuelconv.py` with 16 test cases covering every acceptance item:
  - Each named numeric point (`10 → mpgUS ≈ 23.5215`, `30 mpgUS → 7.8405`, `40 mpgImp → 7.0620`, `10 → km/L = 10.0`, `15 km/L → 6.666666666666667`, `1 mpgUS → 235.2145833`) at the specified tolerances (5e-5 where given, else rel 1e-9).
  - Factors derived from the defining constants (rel 1e-9), plus an explicit mpgUS ≠ mpgImp factor test.
  - Reciprocal-direction test (油耗 doubled → mpg halved, proving not linear scaling).
  - Round-trip over all 4×4 unit pairs at 8.4 (rel 1e-9) and identity `convert_fuel(8.4, u, u)`.
  - Error contract: `0`, `-3` → `ValueError`; `"mpg"` → `ValueError`; `"5"` → `TypeError`; `True` → `TypeError` (bool explicitly covered).

## What I did not do

- Did not touch any existing file (verified via `git status --short`: only `fuelconv.py` and `tests/test_fuelconv.py` added by me).
- Did not implement `jaro` or `multiset` (other cards own those).
- Did not import anything outside the standard library (`numbers.Real`) and nothing from other work-order modules.
- Did not commit or push.
- No `verdict.json` / `verdict.md` by-products were produced by the test run (verified absent).

## Checks run and results

1. `python3 -m pytest tests/test_fuelconv.py -q` → `16 passed in 0.03s`
2. `python3 -m pytest tests/ -q` → `358 passed, 2 skipped in 22.28s` (the 2 skips are pre-existing suite skips, unrelated to fuelconv)

Both checks from the card passed.

## Notes for the validator

- The card's headline trap (reciprocal, not linear) is covered by `test_reciprocal_direction_not_linear_scaling`; the factor-not-mixed trap by `test_mpgus_and_mpgimp_factors_differ`.
- `bool` is rejected as `TypeError` per "非数值（含 bool）" — a plain `isinstance(value, Real)` check would let `True` through, so an explicit `isinstance(value, bool)` guard is in place.
- Unknown-unit `ValueError` is raised from the canonical-conversion helpers; it is only reachable when `value` passes the value checks first, so `convert_fuel(0, "bogus", "x")` raises `ValueError` for the zero value (still `ValueError`, matching the contract).
- Relative-error acceptance (1e-9) is asserted with `pytest.approx(..., rel=1e-9)`; the five work-order points that quote absolute tolerances use `abs=5e-5` as specified.
