# Handoff: isbn10 (sub-issue #302)

## What was requested
Implement ISBN-10 check digit validation as part of work order #299 (round 36). Owns only two new files:

- `isbn10.py`
- `tests/test_isbn10.py`

Spec:
- `check_digit(first9: str) -> str`: input must be exactly 9 digits; returns the check character ('0'-'9' or 'X'), weights from left 10 down to 2, modulo 11 rule; wrong length or any non-digit raises `ValueError`.
- `is_valid(isbn: str) -> bool`: exactly 10 characters, last may be 'X' (only the last position), overall checksum valid returns `True`; anything else returns `False`, never raises an exception.

## What I did
- Created `isbn10.py` (standard library only, no imports from other deliverable modules):
  - `check_digit` validates length 9 and pure ASCII digits (raises `ValueError` otherwise), computes the weighted sum with weights 10..2, then `(11 - sum % 11) % 11`; value 10 maps to `'X'`, otherwise the digit.
  - `is_valid` returns `False` for non-strings, wrong length, non-digit body, or a last character outside `0-9X` (so lowercase `x` is rejected); otherwise compares `check_digit(first9)` to the last character. Wrapped so it never raises.
- Created `tests/test_isbn10.py` with a test case for **every** acceptance example from the process card, plus extra edge cases (non-digit input, wrong lengths, `X` outside last position, non-string inputs never raising).

## What I did not do
- Did not modify any existing file.
- Did not implement `base64url.py` or `semvercmp.py` (owned by other processes).
- Did not add or import any other deliverable module.
- Did not commit or push.

## Checks run and results
- `python3 -m pytest tests/test_isbn10.py -q` → **11 passed**
- `python3 -m pytest tests/ -q` → **22 passed**

Note: pytest was not installed in the environment initially; I installed it via `python3 -m pip install pytest` (now 9.2.0) to run the checks.

## What the validator must pay attention to
- Acceptance mapping is 1:1: each of the 7 acceptance examples in the process card has a dedicated test function in `tests/test_isbn10.py`.
- Lowercase `x` must be rejected: `is_valid("080442957x")` is `False`; only uppercase `'X'` in the final position is accepted.
- `check_digit` raises `ValueError` for any non-digit or wrong length (e.g. `"03064061"`).
- `is_valid` must never raise, including for non-string inputs (returns `False`).
- Full suite is green with all three deliverables' tests present in the final merged run (at time of writing, 22 tests passed; other processes' test files may add more).
