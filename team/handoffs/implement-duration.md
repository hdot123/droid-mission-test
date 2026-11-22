# Handoff: implement-duration (sub-issue #172)

## What was requested
Work order #159, process card `implement-duration`: implement `duration.py` with two functions and a dedicated test file.

- `parse_duration(s)` — parse a duration string into total seconds (int). Supports units `d`, `h`, `m`, `s`. Each unit may appear at most once and must appear in descending order d, h, m, s (e.g. `"1h30m"`). Invalid format raises `ValueError`.
- `format_duration(seconds)` — inverse: split into d/h/m/s, omit zero-valued units; `0` returns `"0s"`; negative raises `ValueError`.
- Body examples that must hold:
  - `parse_duration("1h30m") == 5400`
  - `parse_duration("45s") == 45`
  - `parse_duration("2d") == 172800`
  - `format_duration(5400) == "1h30m"`
  - `format_duration(3661) == "1h1m1s"`
  - `format_duration(0) == "0s"`
- Constraints: Python standard library only; `duration.py` must not import `stack` or `wraplines`; no package directory, no CLI; tests cover both functions, every body example, the descending-order and at-most-once unit rules, `ValueError` on invalid format, and `ValueError` on negative seconds; test file tests only `duration.py`.

## What I did
- Created `duration.py`:
  - `parse_duration(s)` tokenizes with `re.findall(r"(\d+)([dhms])")`, reconstructs the string to reject any unconsumed input (covers empty string, bare numbers, unknown units, signs, fractional/whitespace forms), rejects duplicate units, and enforces strictly descending unit order via index comparison into `("d","h","m","s")`. Raises `ValueError` on invalid input; `ValueError` also covers non-string input. Multipliers: d=86400, h=3600, m=60, s=1.
  - `format_duration(seconds)` raises `ValueError` on negatives (and non-numeric input), returns `"0s"` for 0, otherwise greedily extracts d/h/m/s with `divmod` and joins non-zero parts. (Non-integer positive input is truncated to an integer, which is the natural reading of "总秒数（整数）".)
- Created `tests/test_duration.py` with 24 tests covering: all six body examples, descending-order violations (`"30m1h"`, `"5s30m"`, `"1s1d"`), descending-order acceptance, at-most-once violations (`"1h2h"`, `"1m1m"`, `"1d1d"`), 10 invalid-format cases, non-string input, zero-unit omission in formatting, negative-seconds `ValueError`, and a parse/format round trip.
- Installed `pytest` into the environment (it was absent: `/usr/bin/python: No module named pytest`); this is environment setup only, no repository files changed by it.

## What I did not do
- Did not create or modify `stack.py`, `wraplines.py`, or any other test file (owned by other process cards).
- Did not touch `team/` paths other than my own two files, nor `.github/`.
- Did not commit or push (workflow handles that).
- No CLI, no package directory, no third-party dependencies in shipped code.

## Checks run and results
Check command (verbatim from this card's `checks` field), run from repository root:

```
python -m pytest -q tests/test_duration.py
```

Result: `........................ [100%]` / `24 passed in 0.03s` (exit 0).

Additionally ran `python -m pytest -q` (full suite) as a cross-check: `24 passed` (exit 0) — no failures from my files; at the time of running, no other worker's tests were present in the tree.

## Notes for the validator
- `parse_duration("")` and any string whose token concatenation does not reproduce the input raise `ValueError`, so malformed formats are covered by construction, not just by the enumerated test cases.
- The at-most-once and descending-order checks run after format validation, so `"1h1h"` fails on duplication and `"30m1h"` fails on order, both as `ValueError`.
- Signature check: `duration.py` exposes exactly `parse_duration(s)` and `format_duration(seconds)`; it imports only `re` from the standard library and does not import `stack` or `wraplines`.
