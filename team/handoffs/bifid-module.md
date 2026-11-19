# Handoff: bifid-module (sub-issue #709)

## What was requested

Implement `bifid.py` (Bifid cipher: fixed 5x5 Polybius square plus period transposition) and `tests/test_bifid.py` under process card #700 (round 49, concurrent card C). Process card scope: only these two new files; no other process's files; no modifications to existing files; standard library only; no imports of other delivery modules (`partitions`, `rotate2d`, etc.).

Spec highlights:
- Alphabet pinned to `ABCDEFGHIKLMNOPQRSTUVWXYZ` (25 letters, no J; J folded into I), row-major fill: cell (r, c) (1-based) holds alphabet index `(r-1)*5 + (c-1)` (0-based).
- `bifid_encrypt(text: str, period: int = 5) -> str`: prepare text (uppercase, J->I, keep only in-alphabet letters), split into groups of `period` (last group may be short). Per group: write all row coordinates, then all column coordinates, then pair digits as (row, col) back to letters. Empty string returns empty string.
- `bifid_decrypt(cipher: str, period: int = 5) -> str`: inverse, same grouping; per group the per-letter (row, col) pairs are written side by side, first half = row column, second half = column column, paired back. Returns the prepared plaintext (with folded I).
- Validation: `period` must be positive int (non-int -> TypeError, <= 0 -> ValueError); `text`/`cipher` non-str -> TypeError.

## What I did

- Created `bifid.py` with `ALPHABET`, `bifid_encrypt`, `bifid_decrypt`, using only the standard library. No imports of any other project module.
- Created `tests/test_bifid.py` with one test case per acceptance point, verbatim:
  - `bifid_encrypt("HELLO", 5) == "FNNVD"`
  - `bifid_decrypt("FNNVD", 5) == "HELLO"`
  - `bifid_encrypt("A", 5) == "A"`, `bifid_encrypt("", 5) == ""`, `bifid_decrypt("", 5) == ""`
  - `bifid_encrypt("J", 5) == "I"`, `bifid_encrypt("JUMP", 5) == "INUK"`
  - `bifid_encrypt("CRYPTOGRAPHY", 6) == "DXSMUTICKGEO"`
  - `bifid_encrypt("HELLOWORLD", 3) == "FNVNVROOFD"`
  - Round-trips: `bifid_decrypt(bifid_encrypt(t, p), p) == t` for ("THEQUICKBROWNFOX", 5) and ("ATTACKATDAWN", 4)
  - Period affects result: `bifid_encrypt("HELLOWORLD", 5) != bifid_encrypt("HELLOWORLD", 4)`
  - `bifid_encrypt("ABC", 0)` raises ValueError; `bifid_encrypt("ABC", "5")` and `bifid_encrypt(42, 5)` raise TypeError
  - Extra coverage: default `period=5` behaves like explicit 5; decrypt raises on non-str and non-positive period.

## What I did not do

- Did not create or touch `partitions.py`, `rotate2d.py`, `tests/test_partitions.py`, `tests/test_rotate2d.py` (owned by sibling processes).
- Did not modify any pre-existing file (including `requirements-dev.txt`, `roman.py`, `legacy_stringkit.py`, existing tests, docs, schemas, scripts).
- Did not commit or push.

## Checks run and results

1. `python3 -m pytest tests/test_bifid.py -q` — **passed**: `17 passed in 0.02s` (exit 0).
2. `python3 -m pytest tests/ -q` — **passed**: `97 passed in 2.37s` (exit 0).

Environment note: pytest was not installed in the base image; I installed `requirements-dev.txt` (pytest>=7.4.0, jsonschema>=4.20.0) with `python3 -m pip install -r requirements-dev.txt`. No repository files were changed by this.

## What the validator must pay attention to

- Per-period grouping is applied independently to each group: row string + column string per group, not globally across the whole message. All acceptance vectors were computed under this rule and match.
- `bifid_decrypt` returns the prepared plaintext (uppercase, J already folded into I) as specified.
- `period` validation happens before text-type validation in my implementation? No: text type is checked first, then period. Both raise the specified error types regardless of order for the acceptance cases given.
- The 17 tests in `tests/test_bifid.py` map one-to-one to the acceptance list; the full suite (97 tests) includes pre-existing repo tests plus sibling-process tests and is green.
