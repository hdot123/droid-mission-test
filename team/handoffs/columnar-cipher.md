# Handoff: columnar-cipher (sub-issue #439)

## What was requested

Process card `columnar-cipher` under work order #431 (第四十四轮 · B). Owns exactly two new files at the repository root:

- `columnar.py` — keyword columnar transposition cipher with two public functions:
  - `columnar_encrypt(text: str, keyword: str) -> str`: lay plaintext row-by-row into a full rectangle of width `len(keyword)`, pad the short last row with `X`; read columns in keyword alphabetical order, ties broken left-to-right (stable sort on `(letter, column index)`). Empty string returns `""`. Keyword must be a non-empty pure alphabetic string, else `ValueError`; non-`str` arguments raise `TypeError`.
  - `columnar_decrypt(cipher: str, keyword: str) -> str`: inverse — refill column-by-column in the same order, read row-by-row, return plaintext **including** padding `X` (no stripping). Ciphertext length not a multiple of keyword length raises `ValueError`; same keyword/type rules; empty string returns `""`.
- `tests/test_columnar.py` — one test case per acceptance item, verbatim.

All 12 acceptance examples plus the extra coverage items from the process card are covered as individual test cases.

## What I did

- Implemented `columnar.py` using only the standard library. Shared helpers: `_validate` (type + keyword validation, `TypeError` checked before `ValueError`) and `_column_order` (stable sort on `(letter, index)` via `sorted(range(len(keyword)), key=lambda i: (keyword[i], i))`).
- Encryption pads with `"X" * ((-len(text)) % width)` (no padding needed when length is already a multiple), builds rows, then reads each column in keyword order.
- Decryption splits the ciphertext into `height = len(cipher) // width` chunks in keyword read order, distributes each chunk down its column, and joins rows.
- Wrote `tests/test_columnar.py` with 18 tests: every acceptance example verbatim (6 encrypt happy-path, 3 decrypt happy-path, 4 error cases from the spec), plus empty-string decrypt, `TypeError` cases for non-`str` cipher/keyword on both directions, and `ValueError` keyword cases for decrypt (all required by the "keyword rules identical to encrypt" clause).

## What I did NOT do

- Did not touch any pre-existing file (only created the two owned files plus the two team files below).
- Did not create `primepi.py` or `lengthconv.py`, nor their tests — those belong to other process cards.
- Did not import the other modules; no cross-module dependency.
- Did not edit `team/` beyond my own two files, never edited `.github/`.
- Did not commit or push.

## Checks run and results

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_columnar.py -q` | 18 passed in 0.02s |
| `python3 -m pytest tests/ -q` | 29 passed in 0.04s (18 new columnar + 11 pre-existing roman/legacy_stringkit tests) |

Note: pytest was not preinstalled in the environment; I installed it with `python3 -m pip install pytest` before running the checks.

## Notes for the validator

- Padding is never stripped on decrypt: `columnar_decrypt("EOHLLX", "KEY") == "HELLOX"` and the ZEBRAS example ends in five `X`s. This is intentional per spec.
- Validation order: non-`str` input raises `TypeError` even if the value would also fail the keyword rules; keyword emptiness/non-alpha raises `ValueError` only for `str` inputs.
- The full-suite check passes with the other workers' modules absent (their tests do not exist yet); after merge, the combined suite is expected to pass unchanged since all three deliverables are independent new files.
