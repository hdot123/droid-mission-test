# Handoff: duration (sub-issue #330)

## What was requested
Process card "duration" from work order #314 (第三十八轮 · 并发 C 单). Own exactly two deliverables:

- `duration.py` — duration string conversion in h/m/s units:
  - `parse(text: str) -> int`: convert `"1h30m"`, `"45s"`, `"2h"`, `"1h1m1s"` etc. to total seconds. Only units `h`, `m`, `s`; each at most once; must appear in `h → m → s` order. Raise `ValueError` on empty string, digits with no unit, unknown unit, reversed order, or duplicate unit.
  - `format(seconds: int) -> str`: inverse; canonical output with zero components omitted; total 0 formats as `"0s"`; negative input raises `ValueError`.
- `tests/test_duration.py` — one test case per acceptance criterion.

All acceptance criteria from the work order are covered as tests:
`parse("1h30m") == 5400`, `parse("45s") == 45`, `parse("1h1m1s") == 3661`,
`format(5400) == "1h30m"`, `format(3661) == "1h1m1s"`, `format(0) == "0s"`,
`format(3600) == "1h"`, `parse("30m1h")` raises `ValueError`, `parse("1x")` raises
`ValueError`, `parse("")` raises `ValueError`, and round-trip identity for 7325
(`parse(format(7325)) == 7325`, expected `format(7325) == "2h2m5s"`).

## What I did
- Created `duration.py` using only the standard library (`re`). Parsing uses a
  fullmatch of `(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?`, which rejects empty strings
  (no groups matched), bare digits (trailing text fails fullmatch), unknown
  units, out-of-order units and duplicate units (they fail the pattern as well
  as the h→m→s positional structure). Formatting uses `divmod` and omits zero
  components, appending `0s` only when everything is zero.
- Created `tests/test_duration.py` with pytest cases for every acceptance
  criterion plus extras: single units, zero forms, duplicate units, digits with
  no unit, embedded/trailing spaces, and a multi-value round-trip loop.
- Ran both process checks; both pass (see below).
- Also wrote `team/handoffs/duration.md` and `team/status/duration.json`.

## What I did NOT do
- Did not touch `ipv4kit.py`, `macaddr.py`, their tests, or any pre-existing
  file (only added the two deliverables and the two team files).
- Did not commit or push.
- Did not import from other deliverables (standard library only).

## Checks run and results
- `python3 -m pytest tests/test_duration.py -q` → `12 passed in 0.02s`
- `python3 -m pytest tests/ -q` → `23 passed in 0.03s`

Note: `pytest` was not preinstalled in this environment; I installed it with
`python3 -m pip install -q pytest` (environment setup only, no repo files
changed).

## Notes for the validator
- `duration.py` shadows the builtin `format` within its own module namespace
  (required by the spec: the work order explicitly names the function
  `format`). The test file imports `from duration import format, parse`, which
  is intentional and matches the spec. No other file imports `format` from
  `duration`, so builtins elsewhere are unaffected.
- The parse pattern intentionally accepts forms like `"0s"` and `"0h0m0s"`
  (all zero, in order) and rejects anything not matching the exact h/m/s
  grammar, including whitespace, trailing garbage and `h` alone.
- Expected canonical outputs verified: `format(7325) == "2h2m5s"`,
  `format(45) == "45s"`, `format(1800) == "30m"`.
