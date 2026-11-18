# Handoff: baseconv-radix-convert

## What was requested
Process card `baseconv-radix-convert` (sub-issue #364), part of work order #347 (第四十轮 D). Implement `baseconv.py` with exactly one function `convert(text: str, from_base: int, to_base: int) -> str`:

- Digit characters `0-9` and `a-z`; input letters case-insensitive, output always lowercase.
- Leading negative sign supported.
- Bases must be 2-36 inclusive, else `ValueError`.
- Empty string, lone minus sign, or any digit whose value is not less than `from_base` raises `ValueError`.
- Output has no leading zeros; zero itself and negative zero both output `"0"`.
- Standard library only; no imports from other project modules.
- Create `tests/test_baseconv.py` with a test case for every acceptance item, verbatim.
- Only create the two owned files; touch no existing file; do not commit.

## What I did
- Created `baseconv.py` (new file): parses the sign, validates bases and input, converts via integer arithmetic, and renders the result with the lowercase digit alphabet. Zero (including negative zero, since `-0` parses to value 0) returns `"0"` before any sign handling.
- Created `tests/test_baseconv.py` (new file): 14 tests, one per acceptance item:
  - `convert("ff", 16, 10) == "255"`, `convert("FF", 16, 10) == "255"`, `convert("255", 10, 16) == "ff"`, `convert("1010", 2, 10) == "10"`, `convert("10", 10, 2) == "1010"`, `convert("z", 36, 10) == "35"`, `convert("35", 10, 36) == "z"`, `convert("-255", 10, 16) == "-ff"`, `convert("0", 10, 2) == "0"`, `convert("007", 10, 10) == "7"` (10 positive/negative/edge conversions).
  - `pytest.raises(ValueError)` for `convert("2", 2, 10)`, `convert("10", 1, 10)`, `convert("10", 10, 37)`, `convert("", 10, 10)` (4 error cases).

## What I did not do
- Did not create or modify `isbn13.py`, `tempconv.py`, `tests/test_isbn13.py`, `tests/test_tempconv.py` (owned by other process cards).
- Did not modify any pre-existing file (README.md, roman.py, legacy_stringkit.py, tests/test_roman.py, tests/test_stringkit.py, or anything else).
- Did not add any lone-minus acceptance test because the work order lists none; lone-minus is still guarded in the implementation and will raise `ValueError` per spec.
- Did not commit or push.

## Checks run and results
1. `python3 -m pytest tests/test_baseconv.py -q` → `14 passed in 0.02s` (exit 0).
2. `python3 -m pytest tests/ -q` → `25 passed in 0.04s` (exit 0).

Note: pytest was not preinstalled in the environment; I installed it with `python3 -m pip install pytest` (pytest 9.2.0) so the mandated checks could run. No repository files were affected by that install.

## What the validator must pay attention to
- Scope: only `baseconv.py`, `tests/test_baseconv.py`, `team/handoffs/baseconv-radix-convert.md`, `team/status/baseconv-radix-convert.json` were created; no existing file was modified.
- Every acceptance item from the work order has a dedicated test, including all four `ValueError` cases.
- Full suite is green (25 tests): existing `tests/test_roman.py` (11) plus this card's 14.
- Edge behavior implemented per spec but not explicitly in the acceptance list: negative zero returns `"0"` (no `-0`), out-of-range bases raise before any parsing, invalid characters (e.g. `!`, `?`) raise `ValueError` via the digit parser, and `to_base` validation happens first so bad target bases fail even with otherwise valid input.
