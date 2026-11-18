# Handoff: duration-parse (sub-issue #227)

## What was requested
Process card #227 (under work order #225): implement the standalone module `duration_parse.py`
(Python standard library only, no imports of other task modules, no package directory, no CLI)
exposing `parse_duration(s)` and `format_duration(seconds)` per the specification, plus
`tests/test_duration_parse.py` covering every worked example and every stated error case.
Scope was strictly limited to `duration_parse.py` and `tests/test_duration_parse.py`
(plus these two team files).

## What I did
- Created `duration_parse.py`:
  - `parse_duration(s)`: strips leading/trailing whitespace, validates the whole string against
    `d/h/m/s` segments (integer immediately followed by unit, optional single spaces between
    segments), rejects empty/whitespace-only strings, pure digits, unknown units, decimals,
    minus signs, and any other non-conforming input with `ValueError`; rejects repeated units
    with `ValueError`; sums segments using d=86400, h=3600, m=60, s=1.
  - `format_duration(seconds)`: raises `ValueError` for negative input, renders `0` as `"0s"`,
    otherwise greedily decomposes by d/h/m/s largest-to-smallest, omits zero units, joins with
    no spaces.
- Created `tests/test_duration_parse.py` with pytest tests covering:
  - all card examples: `1h30m`→5400, `45s`→45, `2d 3h`→183600, `1h2h` raises;
    `5400`→`1h30m`, `183600`→`2d3h`, `0`→`0s`, roundtrip `parse(format(183600))`;
  - additional valid inputs (single units, all units, leading/trailing spaces, zero units,
    multi-digit numbers, `90061`→`1d1h1m1s`);
  - every stated error case: empty string, whitespace-only, pure digits, repeated units
    (with and without space separator), unknown units, decimals, minus sign, missing unit,
    unit-before-number; negative input to `format_duration`.

## What I did NOT do
- Did not touch `bitflags.py`, `wrapwidth.py`, any other test file, `team/` paths other than
  my two handoff/status files, or any `.github` paths.
- Did not create a package directory, CLI, or any cross-module imports.
- Did not commit or push (workflow handles that).

## Checks run
- Environment note: `python -m pytest` initially failed with "No module named pytest"
  (environment gap, not a code failure); installed pytest 9.2.0 via `python3 -m pip install pytest`.
- `python -m pytest -q tests/test_duration_parse.py` → passed: 26 passed in 0.03s (exit 0).
  Result recorded in `team/status/duration-parse.json`.

## Notes for the validator
- The only check for this card is `python -m pytest -q tests/test_duration_parse.py`, run verbatim.
- Segment separator regex allows zero or more plain spaces between segments (so both `1h30m`
  and `2d 3h` parse; multi-space input like `2d  3h` also parses), which matches "segments may
  be separated by spaces" while keeping integer–unit adjacency strict.
- `format_duration` raises `ValueError` for negatives as specified; non-int input raises
  `TypeError` (not part of the stated error list).
