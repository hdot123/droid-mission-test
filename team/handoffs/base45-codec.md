# Handoff: base45-codec (sub-issue #485)

## What was requested

Implement Base45 encode/decode per RFC 9285 in `base45.py`, with full test coverage in `tests/test_base45.py`. Process card scope: only these two new files; standard library only; no imports of hill/yearday or other new modules; never modify any existing file.

Spec highlights:
- Alphabet: `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:` (45 chars).
- Encode: pairs of bytes -> 3 chars (x = b0*256 + b1; output x%45, (x//45)%45, x//2025, low order first); trailing single byte -> 2 chars (x%45, x//45). Non-bytes -> TypeError.
- Decode: inverse; length mod 3 == 1 -> ValueError; char outside alphabet -> ValueError; 2-char group value > 255 or 3-char group value > 65535 -> ValueError; non-str -> TypeError.
- Every acceptance item 1-15 needs a test case, plus 2-char overflow coverage.

## What I did

- Created `base45.py` with `base45_encode(data: bytes) -> str` and `base45_decode(s: str) -> bytes` using a char->value lookup table.
- Decode processes full 3-char groups from the left, then a trailing 2-char group (the length check `len % 3 == 1` up front guarantees only 0 or 2 chars remain).
- Created `tests/test_base45.py` with 21 test cases covering all 15 acceptance items, both overflow paths (2-char > 255 via "ZZ" and ":X"; 3-char > 65535 via ":::"), and 4 parametrized round-trips including `bytes(range(256))`.

## What I did NOT do

- Did not touch `hill.py`, `yearday.py`, or any other existing file (legacy_stringkit.py, roman.py, existing tests, README, etc.).
- Did not import hill/yearday or any non-stdlib module in base45.py.
- Did not commit or push.

## Checks run and results

- `python3 -m pytest tests/test_base45.py -q` -> 21 passed.
- `python3 -m pytest tests/ -q` -> 32 passed.

(Note: pytest was not preinstalled; installed it via pip into the environment first.)

## Notes for the validator

- One iteration was needed: the first decode loop mishandled group boundaries (checked `remaining == 3` but a trailing 2-char group is reached when `remaining == 2` only after consuming all 3-char groups; initial version raised ValueError on valid trailing pairs). Fixed by consuming 3-char groups while `i + 3 <= n`, then handling the final pair.
- `base45_encode` accepts exactly `bytes` (bytearray is rejected to match the spec's "non-bytes input raises TypeError" strictly).
- Encode of `b"\xff"` -> "U5" and `b"\x00"` -> "00" verified; RFC examples "BB8" and "%69 VD92EX0" verified in both directions.
