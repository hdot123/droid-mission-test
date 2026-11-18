# Handoff — base32-codec (sub-issue #354)

## What was requested
Process card `base32-codec` for work order #344 (第四十轮 A 单): implement RFC 4648 Base32 with the
standard alphabet (A–Z, 2–7) and `=` padding, owning only `base32.py` and `tests/test_base32.py`.
Required API:
- `encode(data: bytes) -> str` — standard Base32 with `=` padding; empty input → `""`.
- `decode(text: str) -> bytes` — inverse; must raise `ValueError` on characters outside the
  alphabet (including lowercase), on non-conforming padding, and on non-conforming length.

Constraints: only new files, standard library only, no imports from other project modules, every
acceptance item covered by a test.

## What I did
- Created `base32.py` (no imports at all, so no cross-module dependency): bit accumulator for
  encode, decode table for decode; padding length validated against the RFC-legal set
  {0, 1, 3, 4, 6}; leftover bits after decoding must be zero (catches `MZXW6YT=`, where the
  final sextet has non-zero pad bits).
- Created `tests/test_base32.py` with 9 tests covering every acceptance item verbatim:
  all seven encode vectors, both decode vectors, `decode("MZXW6YT*")` → `ValueError`,
  round-trip identity for `b"\x00\xff\x10"`, plus extra tests for lowercase, bad length,
  bad padding, and a length sweep round-trip (bytes 0..63, lengths 0–64).

## What I did not do
- Did not touch `crc16.py`, `luhn.py`, `roman.py`, `legacy_stringkit.py`, any existing test, or
  any file outside my two deliverables plus the two required team files.
- Did not commit or push.
- Did not implement or test crc16/luhn (other processes own those).

## Checks run
- `python3 -m pytest tests/test_base32.py -q` → **9 passed** (exit 0).
- `python3 -m pytest tests/ -q` → **20 passed** (exit 0; 9 mine + 11 pre-existing).

Note: pytest was not installed in this environment; I installed it with
`python3 -m pip install pytest` (pytest 9.2.0). No project files were changed by that install.

## For the validator
- Watch for decode strictness: lowercase must fail (`decode("my======")` raises), length must be
  a multiple of 8, `=` only at the end in a legal count (0/1/3/4/6 per 8-char block), and pad
  bits must be zero. `decode("MZXW6YT=")` raises because `=` is not one of the legal counts.
- `encode(b"")` returns `""` (length 0, which is a multiple of 8, so it round-trips).
- The only files I added: `base32.py`, `tests/test_base32.py`,
  `team/handoffs/base32-codec.md`, `team/status/base32-codec.json`.
