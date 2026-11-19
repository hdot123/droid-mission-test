# Handoff: crc64-xz (sub-issue #461)

## What was requested

Implement `crc64(data: bytes) -> int` in a new `crc64.py` (CRC-64/XZ / ECMA variant):
reflected polynomial `0xC96C5795D7870F42`, initial value `0xFFFFFFFFFFFFFFFF`, final XOR
`0xFFFFFFFFFFFFFFFF`, returning an integer in `[0, 2**64)`. Non-`bytes` input raises
`TypeError`. Every acceptance example from the work order must have a corresponding test
in a new `tests/test_crc64.py`. Standard library only; no imports of `playfair` or
`swatchbeats`; add-only (no edits to any existing file).

## What I did

- Created `crc64.py`: table-driven reflected CRC-64 implementation (256-entry table
  built from the reflected polynomial, per-byte `crc = (crc >> 8) ^ table[(crc ^ b) & 0xFF]`,
  init `0xFFFFFFFFFFFFFFFF`, final XOR masked to 64 bits). Raises `TypeError` for any
  non-`bytes` input (checked before processing, so `crc64("hello")` raises).
- Created `tests/test_crc64.py` with one test per acceptance example, transcribed
  verbatim:
  - `crc64(b"") == 0`
  - `crc64(b"123456789") == 0x995DC9BBDF1939FA`
  - `crc64(b"hello") == 0x9B1EDAE5DBB937B1`
  - `crc64(b"abc") == 0x2CD8094A1A277627`
  - `crc64(b"\x00") == 0x1FADA17364673F59`
  - `crc64(b"\xff" * 8) == 0xFFFFFFFFFFFFFFFF`
  - `crc64(b"The quick brown fox jumps over the lazy dog") == 0x5B5EB8C2E54AA1C4`
  - `crc64("hello")` raises `TypeError`

## What I did not do

- Did not touch `playfair.py`, `swatchbeats.py`, or their tests (other process cards).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing
  tests, `README.md`, git state, etc.).
- Did not commit or push.
- Did not import anything outside the Python standard library.

## Checks run

1. `python3 -m pytest tests/test_crc64.py -q` → **8 passed** (exit 0)
2. `python3 -m pytest tests/ -q` → **19 passed** (exit 0)

Note: pytest was not present in the environment at session start; it was installed via
`pip3 install pytest` (pytest 9.2.0) to run the required checks. No repo files were
affected by that install.

## For the validator

- The environment initially lacked pytest; if a fresh environment fails with
  "No module named pytest", install pytest first — that is environmental, not a code
  issue.
- Full-suite run includes other teams' modules; the 19 passing tests comprise 8
  (crc64) + the pre-existing 11 (roman, legacy_stringkit). If other process cards land
  concurrently, the total count will grow.
- The implementation is standard reflected CRC-64/XZ; the acceptance values match the
  canonical CRC-64/XZ check value for `"123456789"` (`0x995DC9BBDF1939FA`), confirming
  the polynomial/init/xorout parameters are correct.
