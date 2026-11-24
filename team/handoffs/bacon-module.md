# Handoff: bacon-module (sub-issue #445)

## What was requested

Work order #432, process card `bacon-module`: add exactly two new files to the repo root/tests:

- `bacon.py` — Bacon 双字母密码（26 字母版）with `bacon_encode(text: str) -> str` and `bacon_decode(code: str) -> str`.
- `tests/test_bacon.py` — a test case for every acceptance point in the card.

Constraints from the card: only these two new files, no edits to any existing file, standard library only, no import of `isoweek` or `trie`.

Spec (verbatim from the card):

- Alphabet encoded as 5-bit binary 0–25, a=0, b=1; table: A=aaaaa B=aaaab C=aaaba D=aaabb E=aabaa F=aabab G=aabba H=aabbb I=abaaa J=abaab K=ababa L=ababb M=abbaa N=abbab O=abbba P=abbbb Q=baaaa R=baaab S=baaba T=baabb U=babaa V=babab W=babba X=babbb Y=bbaaa Z=bbaab.
- `bacon_encode`: case-insensitive; one 5-bit a/b group per letter, groups separated by a single space; empty string → empty string; non-letter character → ValueError; non-str input → TypeError.
- `bacon_decode`: space-separated 5-bit a/b groups → uppercase letters; empty string → empty string; each group must be exactly 5 a/b characters, else ValueError; non-str input → TypeError.

## What I did

1. Created `bacon.py`:
   - Builds the encode/decode tables at import time from `str.format(index, "05b")` translated `0→a`, `1→b`, which produces exactly the specified table (verified against every pair listed in the card).
   - `bacon_encode`: raises `TypeError` for non-`str`, `ValueError` for any character whose `upper()` is not A–Z (covers digits, punctuation, and would cover whitespace); empty string returns `""`.
   - `bacon_decode`: raises `TypeError` for non-`str`; empty string returns `""`; splits on a single space, so a double space yields an empty group, which fails the length/lookup check and raises `ValueError`. Groups that are not exactly 5 chars or contain non-a/b chars (e.g. `aaaa`, `aabbc`) raise `ValueError`.
2. Created `tests/test_bacon.py` with one test function per acceptance point:
   - encode: `"A"`, `"Z"`, `"HELLO"`, `"Hi"`, `""`
   - decode: `"aaaaa"`, `"bbaab"`, the HELLO groups, `""`
   - encode ValueErrors: `"A1"`, `"HELLO!"`
   - decode ValueErrors: `"aaaa"`, `"aabbc"`, `"aabbb  aabaa"` (double space)
   - TypeErrors: `bacon_encode(123)`, `bacon_decode(123)`
   - plus two supplementary tests (full A–Z roundtrip; lowercase case-insensitivity).

## What I did NOT do

- Did not create or touch `isoweek.py`, `trie.py`, `tests/test_isoweek.py`, `tests/test_trie.py` (other processes own those).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, `tests/test_roman.py`, `tests/test_legacy_stringkit.py`, `README.md`, etc.).
- Did not import `isoweek` or `trie`; stdlib only (`pytest` in tests, matching the existing test style).
- Did not commit or push.

## Checks run

- `python3 -m pytest tests/test_bacon.py -q` — pass (15 passed).
- `python3 -m pytest tests/ -q` — pass (26 passed; full suite, includes the other teams' files as present at run time).
- Note: the sandbox had no `pytest` module preinstalled; installed it with `pip3 install --user pytest` (pytest 9.2.0) so the required checks could run. No repo files were affected.

## Notes for the validator

- The decode table is derived programmatically rather than hand-written; the derivation is `format(i, "05b")` with `0→a`/`1→b` for i in 0..25, which is exactly the card's table. The test suite asserts every literal pair from the card (A, Z, HELLO, Hi) so any table drift fails tests.
- Double-space rejection falls out of `str.split(" ")` producing an empty group; the test pins this explicitly.
- Encoding is case-insensitive via `ch.upper()`; a non-letter whose `upper()` is still not A–Z (digit, punctuation, space) raises `ValueError` as required.
- Other process cards (`isoweek-module`, `trie-module`) add their own files; after merge the full-suite check covers all three plus the stock tests.
