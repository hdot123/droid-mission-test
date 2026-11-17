# Handoff: duration-module (sub-issue #27)

## What was requested

Implement `duration.py` in the repository root with two public functions, plus `tests/test_duration.py`:

- `parse(s)` — parse duration strings like `"1h30m"`, `"45s"`, `"2d 3h"` into total seconds. Units are d (86400), h (3600), m (60), s (1). Whitespace between segments is allowed; segments may appear in any order; a repeated unit raises `ValueError`; empty/whitespace-only string raises `ValueError`; malformed input (unknown units, missing numbers) raises `ValueError`.
- `format(seconds)` — inverse, producing the simplest form: `0` outputs `"0s"`; otherwise greedily use the largest unit that divides the remaining value exactly (integral division priority), e.g. `90 -> "1m30s"`, `86400 -> "1d"`, `3600 -> "1h"`; negative input raises `ValueError`.
- Global rule: every public function must raise `TypeError` when its argument is `None` (never return a value instead): `parse(None)` and `format(None)` both raise `TypeError`.
- Standard library only; no imports of other project modules; no CLI, no package directory.

## What I did

- Created `duration.py` with `parse(s)` and `format(seconds)` implementing the spec above.
  - `parse` raises `TypeError` for `None` (and non-str), `ValueError` for empty/whitespace-only, duplicate units, unknown units, and missing numbers/units.
  - `format` raises `TypeError` for `None` (and non-int), `ValueError` for negatives, returns `"0s"` for 0, and greedily emits the largest exactly-dividing unit first (with remainder segments for the rest).
- Created `tests/test_duration.py` covering: the given examples, unit conversion totals, arbitrary order and spacing, duplicate-unit `ValueError`, empty-string `ValueError`, malformed-input `ValueError`, `0 -> "0s"`, exact-division formatting, composite/greedy formatting, a parse/format round trip, negative `ValueError`, and `TypeError` on `None` for both functions.
- Created this handoff and `team/status/duration-module.json`.

## What I did not do

- Did not touch `isbn.py`, `fence.py`, or their tests.
- Did not modify any other repo file (README, workflow files, other team files).
- Did not commit or push.

## Checks ran and results

- `python -m pytest -q tests/test_duration.py` — passed (all tests green).

## Notes for the validator

- `format` is a builtin shadow by design (per the work-order signature); tests import the module as `duration` and call `duration.format(...)`, so the builtin is not affected.
- `format` rejects non-`int` types (including `bool`) with `TypeError`; the spec only requires `None` to raise `TypeError`, and negatives to raise `ValueError`.
- The parse/format round-trip test asserts `parse(format(n)) == n` for representative values, which exercises the inverse relationship.
