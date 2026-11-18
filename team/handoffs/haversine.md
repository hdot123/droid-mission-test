# Handoff: haversine (sub-issue #377)

## What was requested
Work order #373, process card `haversine`: implement `haversine.py` and `tests/test_haversine.py` only — spherical great-circle distance in km, haversine formula, Earth radius R = 6371.0 km, stdlib `math` only, no other dependencies, no imports of `adler32`/`soundex`. Latitude outside [-90, 90] or longitude outside [-180, 180] raises `ValueError`. Every acceptance item must have a corresponding test case.

## What I did
- Created NEW `haversine.py`:
  - `haversine(lat1, lon1, lat2, lon2) -> float` with range validation (raises `ValueError` on out-of-range latitude/longitude, checked on both endpoints of each coordinate), haversine formula using `math.radians`/`math.sin`/`math.cos`/`math.atan2`/`math.sqrt`, and clamping of the `a` term to [0, 1] against floating-point drift.
  - Only import is `math`; no cross-imports of other components.
- Created NEW `tests/test_haversine.py` with one test per acceptance item:
  - same point == 0.0; 1° lon and 1° lat == 111.1949266 ± 0.001; 180° along equator == 20015.0867960 ± 0.001; pole-to-equator == 10007.5433980 ± 0.001; antipodal diagonal (45,0 / -45,180) == 20015.0867960 ± 0.001; 90° along equator == 10007.5433980 ± 0.001; New York–London == 5570.2221797 ± 0.01; Sydney–Tokyo == 7825.8186165 ± 0.01; `haversine(91, 0, 0, 0)` and `haversine(0, 181, 0, 0)` each raise `ValueError` (plus mirror cases `-91` / `-181`).
- Installed `pytest` via `pip3 install --user pytest` (environment had no pytest module; this is outside the repo, no repo files touched).

## What I did NOT do
- Did not modify, create, or delete any existing repo file (only the two owned new files were added to the repo tree).
- Did not touch `adler32.py`, `soundex.py`, their tests, or any other process's files.
- Did not commit or push.
- Did not run or implement other process cards.

## Checks run (from repository root)
- `python3 -m pytest tests/test_haversine.py -q` → **11 passed** in 0.02s
- `python3 -m pytest tests/ -q` → **22 passed** in 0.03s (full suite, including existing roman/legacy_stringkit tests)

## Notes for the validator
- Expected tolerance-based values: all acceptance numbers match to within the stated tolerances (all comparisons passed exactly as written in the work order).
- The two ValueError acceptance items are covered in dedicated test functions; I additionally assert the `-91`/`-181` mirror cases (superset of the required checks, no relaxation of any required assertion).
- `haversine(0, 0, 0, 0) == 0.0` holds exactly (no epsilon needed).
- Tests import `from haversine import haversine`, consistent with how existing tests import `roman`/`legacy_stringkit` (root on `sys.path` via pytest rootdir behavior).
