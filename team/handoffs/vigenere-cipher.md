# Handoff: vigenere-cipher (sub-issue #181)

## What was requested
Implement `vigenere.py` in the repository root with exactly two public functions, `encrypt(text, key)` and `decrypt(text, key)`, implementing the Vigenere cipher, plus `tests/test_vigenere.py` covering only this module's behavior.

Spec requirements:
- key must be a non-empty string of pure English letters (case-insensitive), otherwise raise `ValueError`.
- Only English letters are transformed; case (upper/lower) is preserved per character.
- Key letters are used cyclically; the key position advances only when an English letter is encountered in the text; all other characters are kept verbatim.
- Required examples: `encrypt("ATTACKATDAWN", "LEMON")` → `"LXFOPVEFRNHR"`; `encrypt("Attack", "LEMON")` → `"Lxfopv"`; `decrypt("LXFOPVEFRNHR", "LEMON")` → `"ATTACKATDAWN"`.

Constraints: Python standard library only; no import of `ean13.py`/`temperature.py`; no package directory; no CLI.

## What I did
- Created `vigenere.py` (repo root) with a `_validate_key` helper plus `encrypt`/`decrypt`. Validation rejects empty/non-string/non-ASCII/non-alpha keys with `ValueError`. Transformation uses ASCII `a`/`A` bases and a `% 26` shift; `char.isascii() and char.isalpha()` gates which characters advance the key index, so digits, punctuation, spaces, newlines and tabs are preserved verbatim and never advance the key.
- Created `tests/test_vigenere.py` (17 test cases; the parametrized invalid-key case counts as several): the three required examples, a round-trip, invalid keys (`""`, `" "`, `"LE MON"`, `"LE1MON"`, `"L3MON"`, `None`, `123`, `b"LEMON"`) raising `ValueError` from both functions, non-letter characters not advancing the key (`"A B C"` with `"LEMON"` → `"L F O"`; `"hi, there!"` with `"key"` → `"rm, rripo!"`; `"a\nb\tc"` with `"LE"` → `"l\nf\tn"`), and case preservation for both encrypt and decrypt.

## What I did not do
- Did not touch `ean13.py`, `temperature.py`, or their tests (owned by other processes).
- Did not create a package directory, `__init__.py`, CLI entry points, or any files outside `vigenere.py`, `tests/test_vigenere.py`, and the two required team files.
- Did not commit or push; did not modify `team/` beyond my own handoff/status files.

## Checks I ran and results
Both checks were run verbatim from this card's checks column, from the repository root:
1. `python -m pytest -q tests/test_vigenere.py` → `17 passed in 0.01s` (exit 0).
2. `python -m pytest -q` → `17 passed in 0.01s` (exit 0). (At the time of this run, only this process's tests exist in the repo.)

Note: `pytest` was not preinstalled in the environment; I installed it with `python -m pip install pytest` (pytest 9.2.0) to be able to run the required checks.

## What the validator must pay attention to
- `python -m pytest -q` currently passes with 17 tests, all from `tests/test_vigenere.py`. Once sibling processes land `tests/test_ean13.py` and `tests/test_temperature.py`, the same command must still pass entirely; my changes do not affect them (no cross-imports).
- The key validation accepts only ASCII letters: `str.isalpha()` alone would accept e.g. `"é"`, so the implementation additionally requires `str.isascii()`. Non-`str` inputs (`None`, `int`, `bytes`) also raise `ValueError` via the same guard.
- Non-letter handling is gated on `char.isascii() and char.isalpha()`, matching "only English letters are transformed" and "key advances only on English letters".
- Signatures are exactly `encrypt(text, key)` and `decrypt(text, key)`; only these two functions are public (plus the private `_validate_key` helper).
