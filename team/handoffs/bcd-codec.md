# Handoff: bcd-codec (sub-issue #399)

## What was requested
Process card `bcd-codec` under work order #383 (round 42 · D): create only two new files, `bcd.py` and `tests/test_bcd.py`, implementing packed-BCD encode/decode with the listed acceptance items, using only the standard library, without touching any existing file or any other process's files.

## What I did
- Created `bcd.py` with:
  - `encode(n: int) -> int` — packs each decimal digit into one hex nibble (123 -> 0x123); raises `ValueError` for negative `n`.
  - `decode(b: int) -> int` — inverse; raises `ValueError` if `b` is negative or any nibble is greater than 9.
- Created `tests/test_bcd.py` with a dedicated test case per acceptance item:
  - `encode(0/9/12/123/2026/99)` equality checks.
  - `decode(0x123/0x2026/0x99)` equality checks.
  - `ValueError` cases: `decode(0x1A)`, `decode(-1)`, `encode(-1)`.
  - Round-trip identity `decode(encode(i)) == i` for every `i` in 0..999.
- Ran the process checks from the repository root (pytest was not installed in the environment; I installed it with `pip3 install pytest`).

## What I did not do
- Did not create or modify `julian.py`, `angle.py`, their tests, or any pre-existing file (`roman.py`, `legacy_stringkit.py`, `tests/test_roman.py`, `tests/test_legacy_stringkit.py`, etc.).
- Did not modify anything under `team/` other than my own two files: `team/handoffs/bcd-codec.md` and `team/status/bcd-codec.json`.
- Did not commit or push anything.

## Checks run and results
- `python3 -m pytest tests/test_bcd.py -q` → **13 passed** (exit 0).
- `python3 -m pytest tests/ -q` → **24 passed** (exit 0) — includes the 11 pre-existing baseline tests.

## Notes for the validator
- `encode(0)` returns `0` (0x0) by design: the loop emits the single digit 0 and stops, so there is no spurious leading nibble.
- `decode` rejects any nibble > 9 (e.g. 0x1A) with `ValueError`, and rejects negatives for both functions, exactly as specified.
- Implementation uses only bit/arith operations on `int`; no imports at all, so no cross-module coupling with `julian` or `angle`.
- The environment lacked pytest; it was installed locally to run the required checks. No repository files were affected by that install.
