# Handoff: bifid (sub-issue #675, work order #663 C 单)

## What was requested

Implement the Bifid cipher component only:
- `bifid.py`: 5×5 Polybius square pinned to alphabet `ABCDEFGHIKLMNOPQRSTUVWXYZ` (no J, J→I), row-major fill; `bifid_encrypt(text: str, period: int = 5) -> str` and `bifid_decrypt(cipher: str, period: int = 5) -> str` with the exact grouping/transposition rules from the card; validation (period non-int → TypeError, period ≤ 0 → ValueError, non-str text → TypeError).
- `tests/test_bifid.py`: a test case for every acceptance point in the card.
- Scope: only these two files; standard library only; no cross-imports of other modules; no modification of existing files.

## What I did

- Created `bifid.py`:
  - `ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"`; letter→(row, col) map built from row-major index.
  - `_preprocess`: uppercase, J→I, keep only in-alphabet chars.
  - `bifid_encrypt`: validates types first, groups plaintext by `period`, per group writes all row digits then all column digits, pairs digits back to letters via `ALPHABET[(r-1)*5 + (c-1)]`. Empty input → `""`.
  - `bifid_decrypt`: same grouping; per group each cipher letter's (row, col) written as 2 digits, first half = row-column digits, second half = column digits, zipped to restore letters. Empty input → `""`. Returns preprocessed plaintext (merged I).
  - Validation: `bool` rejected for period (`isinstance(period, bool)` check first), non-int → TypeError, ≤0 → ValueError, non-str text/cipher → TypeError.
- Created `tests/test_bifid.py` covering every acceptance point: all eight encrypt vectors (HELLO/FNNVD, A, "", J→I, JUMP/INUK, CRYPTOGRAPHY period 6, HELLOWORLD period 3), decrypt vector, empty decrypt, two round-trips (THEQUICKBROWNFOX@5, ATTACKATDAWN@4), period-affects-result inequality, ValueError on period 0 (and −1), TypeError on period "5", text 42, decrypt 42, and bool period.

## What I did not do

- Did not touch `partitions.py`, `rotate2d.py`, or any other existing file.
- Did not commit or push.
- Did not add any dependency (standard library only in `bifid.py`).

## Checks run and results

From repository root:

1. `python3 -m pytest tests/test_bifid.py -q` → **18 passed**
2. `python3 -m pytest tests/ -q` → **54 passed**

(Note: pytest was not preinstalled; installed via `python3 -m pip install -r requirements-dev.txt` — no repo files changed.)

## Validator notes

- `bifid_encrypt("JUMP", 5)` relies on J→I preprocessing producing "INUK"; if a future refactor changes preprocessing order (e.g. filtering before J-merge), that vector breaks.
- Decrypt is specified to return the *preprocessed* plaintext (uppercase, J merged to I, non-letters dropped) — round-trip tests use already-preprocessed inputs, which matches the card.
- Period validation happens after text type validation in encrypt (both raise before any work); ordering between the two TypeErrors is unspecified by the card, current order is text first, then period.
- Square/`ALPHABET` are module-level constants; no state, thread-safe, standard library only, no imports from sibling modules.
