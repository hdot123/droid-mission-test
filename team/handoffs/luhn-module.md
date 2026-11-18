# Handoff: luhn-module (sub-issue #286)

## What was requested
Process card `luhn-module` from work order #278 (round 35, foreman v2.6.5):
- Create `luhn.py` with two functions:
  - `is_valid(number: str) -> bool` — Luhn-check a pure-digit string; returns `False` (no exception) for empty strings or strings with non-digit characters.
  - `check_digit(prefix: str) -> int` — given a non-empty pure-digit prefix, return the check digit (0–9) making the whole number pass Luhn; raises `ValueError` for empty or non-digit input.
- Create `tests/test_luhn.py` covering all seven mandatory acceptance items.
- Constraints: only new files, standard library only, no imports from `isbn13` or `mod97`, do not modify any existing file.

## What I did
- Wrote `luhn.py`:
  - `is_valid` iterates digits right-to-left, doubling every second digit (subtracting 9 when the doubled value exceeds 9), sums, and returns `sum % 10 == 0`. Non-str, empty, or non-digit input short-circuits to `False`.
  - `check_digit` validates input (raises `ValueError` otherwise), then computes the sum with the weights shifted one position (prefix's rightmost digit gets weight 2, since the appended check digit occupies weight 1) and returns `(10 - total % 10) % 10`.
- Wrote `tests/test_luhn.py` with one test per mandatory acceptance item, plus three extras:
  - `check_digit("7992a39871")` raises `ValueError` (non-digit prefix),
  - round-trip: `check_digit("7992739871")` then `is_valid(prefix + str(digit))` is `True`,
  - `check_digit` result is always in `0..9` for several prefixes.

## What I did not do
- Did not create or touch `isbn13.py`, `mod97.py`, or their tests (other processes own those).
- Did not modify any pre-existing file (`README.md`, `roman.py`, `legacy_stringkit.py`, `tests/test_roman.py`, `tests/test_legacy_stringkit.py`, etc.).
- Did not commit or push.
- Note: `pytest` was not installed in the environment; I installed it with `python3 -m pip install pytest` (environment setup only, no repo files changed).

## Checks run and results
- `python3 -m pytest tests/test_luhn.py -q` → `10 passed in 0.02s`
- `python3 -m pytest tests/ -q` → `21 passed in 0.03s` (includes the pre-existing 11 tests)

## What the validator must pay attention to
- All seven mandatory acceptance items are covered by dedicated tests; the extra tests are additive, not substitutes.
- `is_valid("0")` is `True` because the single digit 0 sums to 0, which is divisible by 10.
- `check_digit` and `is_valid` use the same weighting scheme shifted by one position; the round-trip test (`test_check_digit_round_trip`) proves they agree.
- No cross-module imports exist in `luhn.py`; it is fully standalone.
