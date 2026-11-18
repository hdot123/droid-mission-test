# Handoff: bytesize (sub-issue #358)

## What was requested
Process card for work order #346 (round 40 · unit C): implement `bytesize.py` (byte-size human-readable formatting and parsing) plus `tests/test_bytesize.py`. Owns only those two files; standard library only; no imports from other project modules (`rangemerge`, `colorhex`); every acceptance item from the work order must have a corresponding test case. Checks to run from repo root: `python3 -m pytest tests/test_bytesize.py -q` and `python3 -m pytest tests/ -q`.

Spec implemented (verbatim from the work order):
- `format(n: int) -> str`: base-1024, units B, KiB, MiB, GiB, TiB; `n < 1024` prints `"<n> B"` (integer); otherwise the largest unit not exceeding TiB, value rounded to one decimal (e.g. `"1.5 KiB"`); negative `n` raises ValueError.
- `parse(text: str) -> int`: inverse; form must be `"<value> <unit>"` (exactly one space; value a non-negative integer or one-decimal number; unit one of the five above); result must be a whole number of bytes, else ValueError.

## What I did
- Created `bytesize.py` using only `re` from the standard library. `format` rejects negatives, returns plain `"<n> B"` below 1024, else divides by 1024^index for the largest unit index <= TiB and formats with `%.1f`. `parse` splits on a single space (so `"1.5KiB"` and multi-space forms fail), validates the unit against the five allowed names, matches the value against `^(\d+)(?:\.(\d))?$` (rejects `1.5 KB`-style units, missing spaces, non-hex-free garbage, extra dots), scales by unit, and raises ValueError if the result is not a whole number of bytes (e.g. a fractional byte).
- Created `tests/test_bytesize.py` with one test per acceptance item (10 test functions covering: format 0/1023/1024/1536/1048576/1234567/1073741824/1099511627776; parse "0 B"/"512 B"/"1.5 KiB"/"2 KiB"/"1.0 MiB"; `format(-1)` ValueError; `parse("1.5KiB")` and `parse("1.5 KB")` ValueError; round-trip `parse(format(1536)) == 1536`).

## What I did not do
- Did not touch `rangemerge.py`, `colorhex.py`, or any existing file (`roman.py`, `legacy_stringkit.py`, existing tests, README, etc.).
- Did not create or modify anything under `team/` other than my two assigned files (`team/handoffs/bytesize.md`, `team/status/bytesize.json`).
- Did not commit or push.
- No dependencies on other processes; other units' files are not imported and do not affect these tests.

## Checks run and results
Environment note: `pytest` was not installed in this image; I installed it with `python3 -m pip install pytest` (pytest 9.2.0) so the mandated checks could run. This touches only the environment, not the repository.

- `python3 -m pytest tests/test_bytesize.py -q` → 10 passed (exit 0).
- `python3 -m pytest tests/ -q` → 21 passed (exit 0) (10 mine + 11 pre-existing roman/legacy_stringkit tests).

## What the validator must pay attention to
- The whole suite passes after my change; my tests exercise every acceptance bullet listed in the work order, including both ValueError paths and the 1536 round-trip.
- `parse` deliberately rejects anything that is not exactly `"<non-negative int or one-decimal> <one of B|KiB|MiB|GiB|TiB>"` with a single space; e.g. `"1.5 KB"` fails on unit, `"1.5KiB"` fails on the space split.
- `format` never emits a fractional B value: values below 1024 stay integer, and all parsed forms are checked to be whole byte counts before returning.
- Only `bytesize.py` and `tests/test_bytesize.py` were added by this process (plus the two `team/` files the workflow asked for).
