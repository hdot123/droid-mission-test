# Handoff: gasmark-table (sub-issue #649)

## What was requested

Process card `gasmark-table` under work order #630 (第四十七轮 · 并发 A 单). Create exactly two new files, standard library only, no cross-module imports, no modification of any pre-existing file:

- `gasmark.py` — Gas Mark oven temperature lookup with the pinned table (mark → Celsius → Fahrenheit): `1/4 → 110 → 225`, `1/2 → 120 → 250`, `1 → 140 → 275`, `2 → 150 → 300`, `3 → 165 → 325`, `4 → 180 → 350`, `5 → 190 → 375`, `6 → 200 → 400`, `7 → 220 → 425`, `8 → 230 → 450`, `9 → 240 → 475`.
  - `gasmark_to_celsius(mark) -> int` / `gasmark_to_fahrenheit(mark) -> int`: mark accepts int 1–9 or str (`"1/4"`, `"1/2"`, `"1"`–`"9"`); other values raise `ValueError`, other types raise `TypeError` (bool rejected, float not accepted).
  - `celsius_to_gasmark(c) -> str`: c must be numeric (int/float, bool rejected) else `TypeError`; returns the mark string with the smallest absolute Celsius difference; ties take the lower (earlier-in-table) mark.
- `tests/test_gasmark.py` — a test case for every acceptance criterion in the spec.

## What I did

- Created `gasmark.py` with the pinned table as an ordered tuple (table order = tie-break order), a shared `_normalize_mark` validator, the two lookup functions, and `celsius_to_gasmark` using a strict `<` comparison so ties keep the earlier/lower mark.
- Created `tests/test_gasmark.py` covering every acceptance point: all listed lookups (int and str, fraction marks), exact/reverse lookups, the 185 tie case, bounds (0 → `"1/4"`, 500 → `"9"`), 167 → `"3"`, `ValueError` for `0`/`10`/`"3/4"`, `TypeError` for `4.0`/`True` (mark) and `"180"`/`True`/`None` (celsius).

## What I did not do

- Did not create or touch `trifid.py`, `mobius.py`, or their tests (other workers' scope).
- Did not modify any pre-existing file (only the two owned files plus this handoff and `team/status/gasmark-table.json` were written).
- Did not commit or push.
- No cross-module imports; `gasmark.py` uses only the standard library (in fact, no imports at all).

## Checks run and results

Note: pytest was not installed in the environment; installed it via `pip install -r requirements-dev.txt` (dev requirements already listed `pytest>=7.4.0`).

1. `python3 -m pytest tests/test_gasmark.py -q` → **12 passed** in 0.02s.
2. `python3 -m pytest tests/ -q` → **41 passed** in 2.25s (full suite: legacy_stringkit, roman, foreman wall contract, plus the new gasmark tests).

## Notes for the validator

- The full-suite count (41) includes other workers' concurrently added tests if they land before merge; acceptance is defined as the merged full-suite run, so re-run `python3 -m pytest tests/ -q` at merge time.
- Tie-break semantics: `celsius_to_gasmark` initializes the best candidate to the first table entry (`"1/4"`) and only replaces it on a strictly smaller difference, so equal-distance inputs (e.g. 185, equidistant from 180/190) resolve to the lower mark as specified.
- Type rules are strict: `bool` is rejected before `int` checks (so `gasmark_to_celsius(True)` and `celsius_to_gasmark(True)` raise `TypeError`), and floats are rejected for `mark` (`TypeError`) while accepted for `c` (`celsius_to_gasmark(180.0)` works).
- Out-of-range ints (`0`, `10`) and unknown strings (`"3/4"`) raise `ValueError`, not `TypeError`, per spec.
