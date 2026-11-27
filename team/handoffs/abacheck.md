# Handoff: abacheck (sub-issue #962)

## What was requested

Work order #953 round-59 C card: implement ABA routing-number check digit as two files only:

- `abacheck.py` (repo root): `aba_check_digit(first8: str) -> str` and `aba_validate(number: str) -> bool`
- `tests/test_abacheck.py`: tests covering every acceptance point

Spec essentials:
- Weight order pinned left-to-right as 3, 7, 1 cycling (digit 1 → 3, digit 2 → 7, digit 3 → 1, digit 4 → 3, ...).
- `aba_check_digit`: exactly 8-digit numeric string; check digit = `(10 - sum mod 10) mod 10`, returned as a single-character string.
- `aba_validate`: exactly 9-digit numeric string; True iff the 9-digit weighted sum mod 10 == 0 (9th digit weight 1). Check-digit failure returns False, never raises.
- Input contract: wrong length or non-digit characters → ValueError; non-str → TypeError.
- Must not mix in Luhn / IBAN mod97 / Damm algorithms; standard library only; no sibling imports; only the two listed files may be created, no existing file modified.

## What I did

- Created `abacheck.py` with a shared shape-check helper (`_check_shape`: type → TypeError, length/digit-only → ValueError using explicit `ch` range checks, not `str.isdigit`, to avoid Unicode digit surprises) and `_weighted_sum` cycling `(3, 7, 1)`.
- Created `tests/test_abacheck.py` covering each acceptance point:
  - `aba_check_digit("02100002") == "1"`, `aba_check_digit("01100001") == "5"`
  - `aba_validate("021000021") is True`, `aba_validate("011000015") is True`, `aba_validate("021000022") is False`
  - Property test (seeded `random.Random(20261127)`, 300 iterations): check digit agrees element-by-element with a right-to-left per-digit extraction reference; appending it yields a 9-digit number that validates True; changing any single digit (position and delta chosen randomly, including position 8 = the check digit) makes validate return False.
  - ValueError: `aba_check_digit("1234567")`, `aba_check_digit("1234567a")`, `aba_validate("0210000210")`
  - TypeError: `aba_check_digit(2100002)`, `aba_validate(None)`

Note on the reference implementation: for an 8-digit prefix, the left-to-right weights are 3,7,1,3,7,1,3,7, so the right-to-left cycle is (7, 3, 1). My first two attempts used (1,7,3) and (7,1,3) and failed the property test; the final committed reference uses (7, 3, 1) and passes for all 300 seeds. This is test-side only; the implementation was unchanged and correct throughout (its known examples pass).

## What I did not do

- Did not touch `zarray.py`, `millerrabin.py`, or any existing repository file.
- Did not implement Luhn/IBAN/Damm or any other check-digit algorithm.
- Did not commit or push.
- Did not address work-order items outside this card (ledger, gates, other sub-issues).

## Checks run

1. `python3 -m pytest tests/test_abacheck.py -q` → **6 passed** (0.02s)
2. `python3 -m pytest tests/ -q` → **348 passed, 2 skipped** (19.65s), exit code 0

No `verdict.json` / `verdict.md` by-products were produced by these runs (none present to delete).

## Validator attention points

- Weight order is 3/7/1 from the LEFT; do not accept a right-to-left 1/7/3 reading. The pinned examples `("02100002" → "1")` distinguish the two orders.
- `aba_validate` must raise ValueError only on shape (length/non-digit) and return False for a bad check digit; `aba_validate("021000022") is False` is the discriminating case.
- `str.isdigit()` was deliberately avoided in shape checking (accepts e.g. "²"); digits are checked with explicit `0 <= ch <= 9`.
- `is True` / `is False` comparisons in tests enforce exact bool returns.
