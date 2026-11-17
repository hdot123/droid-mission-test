# Handoff: luhn-module (sub-issue #62)

## What was requested
Implement exactly one process card: `luhn.py` (root) plus `tests/test_luhn.py`, per work order #59's deliverable 1. Three functions, standard library only, no third-party deps, no changes to any existing repository file. Required behaviors:

- `is_valid(number)`: string input; strip spaces and hyphens first; after stripping must be all digits with length 12–19 inclusive, otherwise `False` (never raises); return Luhn check result.
- `check_digit(prefix)`: strip spaces/hyphens; must be all digits and non-empty, else `ValueError`; return the single check-digit character string.
- `generate(prefix)`: stripped prefix + check digit as a pure digit string.

Given examples that must hold:
- `is_valid("4539 1488 0343 6467") is True`
- `is_valid("4539-1488-0343-6468") is False`
- `check_digit("4539 1488 0343 646") == "7"`

## What I did
- Created `luhn.py` with the three required public functions and two private helpers (`_strip`, `_luhn_sum_digits`, plus `_is_all_digits` / `_ASCII_DIGITS` for strict ASCII-digit checks so that e.g. full-width digit characters cannot slip through `str.isdigit()`).
- Luhn core: sum digits left of the check digit right-to-left, doubling every other digit (index 0 = rightmost), subtracting 9 when doubled value > 9; valid iff `(sum + check_digit) % 10 == 0`. `check_digit` computes `(10 - sum % 10) % 10`.
- `is_valid` guards `isinstance(number, str)` (returns `False` for non-strings, never raises), then length gate, then ASCII-digit gate, then the Luhn test.
- Created `tests/test_luhn.py` with 20 real pytest tests covering: all three given examples; hyphenated and mixed-separator acceptance; length gates at 11 and 20 rejected and boundaries 12/19 accepted; out-of-range after stripping with separators; empty/separator-only/non-digit/non-string inputs never raising from `is_valid`; `check_digit` raising `ValueError` for empty, separator-only, and non-digit prefixes, and accepting hyphenated prefixes; `generate` returning pure digit strings; generate → `is_valid` round-trips at lengths 12, 16, 16, 19; `generate` rejecting invalid prefixes.
- Installed `pytest 9.2.0` via pip because the environment had no pytest module (needed to run the mandated check command; does not touch repository files or module dependencies).

## What I did not do
- Did not touch `csv_parse.py`, `ipaddr.py`, `README.md`, `.github/`, `worker-prompt.txt`, `worker-stream.jsonl`, or any existing repository file.
- Did not write any test file other than `tests/test_luhn.py`.
- Did not commit or push anything.

## Checks ran and results
- `python -m pytest -q tests/test_luhn.py` → `20 passed in 0.02s` (exit 0). This is the process card's single check command, run verbatim.

## Notes for the validator
- All three work-order examples are asserted verbatim in `tests/test_luhn.py` (`test_is_valid_space_grouped_example_true`, `test_is_valid_hyphenated_wrong_check_digit_example_false`, `test_check_digit_given_example`).
- Note on the second example: `4539-1488-0343-6468` strips to `4539148803436468`, which has correct length and all digits but fails the Luhn sum — verified `False`.
- The check digit for prefix `453914880343646` is `7`; `generate("4539 1488 0343 646") == "4539148803436467"` and `is_valid(...)` is `True`.
- Files delivered: `luhn.py`, `tests/test_luhn.py`, plus this handoff and `team/status/luhn-module.json`.
