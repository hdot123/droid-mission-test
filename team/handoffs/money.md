# Handoff: money (sub-issue #341)

## What was requested

Work order #337 (round 39), process card `money`: implement `money.py` (integer-cent amount helpers) plus `tests/test_money.py`, as new files only. No other file may be created or modified. Requirements verbatim from the card:

- `parse(text: str) -> int`: amount string to integer cents. Accepted form: optional leading `-`, integer part of one or more digits, optional decimal point followed by one or two fractional digits (a single fractional digit is padded as tenths). Thousand-separator commas, whitespace, and `+` are not allowed; malformed form raises `ValueError`.
- `format(cents: int) -> str`: the inverse operation, always two decimal places (e.g. `1234.56`, `-0.05`, `0.00`).
- `split(cents: int, n: int) -> list[int]`: split as evenly as possible into `n` parts; remainder cents go one cent each to the first parts; sum is conserved; `n < 1` raises `ValueError`; negative amounts are split by absolute value and then negated uniformly.
- Acceptance points, each with a test case: `parse("12.3") == 1230`; `parse("0.07") == 7`; `parse("-5") == -500`; `format(123456) == "1234.56"`; `format(-5) == "-0.05"`; `format(0) == "0.00"`; `split(100, 3) == [34, 33, 33]`; `split(-100, 3) == [-34, -33, -33]`; `parse("1,000.00")` and `parse("12.345")` raise `ValueError`; round-trip `format` then `parse` on `-98765` is identity.
- Also cover: `+` rejected, whitespace rejected, more than two fractional digits rejected, single fractional digit as tenths, `split` with `n < 1` raises `ValueError`, sum conservation in `split`, split of a positive amount into exact shares.

## What I did

- Created `money.py`:
  - `parse` uses a strict anchored regex `^-?\d+(?:\.\d{1,2})?$` (rejects commas, whitespace, `+`, empty, leading/trailing `.`, multiple dots, exponent forms), then converts to cents with a single fractional digit padded to two (`"12.3"` -> `1230`).
  - `format` computes sign, `abs(cents) // 100`, and `abs(cents) % 100` zero-padded, so it always emits exactly two decimal places including `0.00` and `-0.05`.
  - `split` validates `n` (must be an `int` >= 1, else `ValueError`), computes `base, remainder = divmod(abs(cents), n)`, adds `1` to the first `remainder` parts, then negates uniformly for negative inputs.
- Created `tests/test_money.py` covering every acceptance point plus the extra required cases (exact-share split, sum conservation across positive/negative/zero inputs, part-size bound, malformed-form rejection list, module export check).

## What I did not do

- Did not modify, create, or delete any other file: `fractionx.py`, `unixpath.py`, other tests, `roman.py`, `legacy_stringkit.py`, `README.md`, and existing tests are untouched.
- Did not implement or test `fractionx` or `unixpath` (other process cards own those).
- Did not commit or push.

## Checks run

1. `python3 -m pytest tests/test_money.py -q` — passed (22 passed in 0.02s).
2. `python3 -m pytest tests/ -q` — passed (33 passed in 0.03s; existing `test_roman.py` / `test_legacy_stringkit.py` plus the new money tests).

Note: `pytest` was not preinstalled in the environment; installed it with `python3 -m pip install pytest` (pytest 9.2.0) so the checks could run.

## Notes for the validator

- `format` shadows the Python builtin `format` inside `money.py` only; tests import it as `money.format` / `from money import format`, matching the card's specified API name.
- Round-trip identity case is `parse(format(-98765)) == -98765` (i.e. `-987.65`), exercised both as its own test and in `test_format_round_trips_negative`.
- `split` returns exactly `n` parts for every input; for `cents=0` all parts are `0`, and the sum-conservation test includes `0`.
