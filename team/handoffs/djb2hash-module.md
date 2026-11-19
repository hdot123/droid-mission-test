# Handoff: djb2hash-module (sub-issue #676)

## What was requested

Work order #664 第四十八轮 D 单 · process card `djb2hash-module`: implement the
djb2 字符串散列（32 位回绕） component, owning exactly two new files:

- `djb2hash.py`
- `tests/test_djb2hash.py`

Spec (verbatim scope):

- `djb2(text: str) -> int`: h starts at 5381; iterate over the UTF-8 bytes of
  `text` byte by byte, `h = (h * 33 + byte) mod 2**32` (i.e. `& 0xFFFFFFFF`);
  return the final h. Non-`str` raises `TypeError`.
- `djb2_bytes(data: bytes) -> int`: same algorithm applied directly to a byte
  sequence; non-`bytes`/`bytearray` raises `TypeError`.
- Every acceptance item must have a corresponding test case.

## What I did

- Created `djb2hash.py`: standard library only (no imports at all beyond
  builtins), no imports from unionfind/bizdays or any other deliverable.
  Shared private helper `_djb2_from_bytes` implements the loop once; `djb2`
  encodes to UTF-8 then delegates, `djb2_bytes` validates type then delegates.
  Type checks use `isinstance`, so `bool` is not specially handled here (the
  spec does not require bool rejection for this module).
- Created `tests/test_djb2hash.py` with one test per acceptance item:
  - `djb2("") == 5381`
  - `djb2("a") == 177670`
  - `djb2("abc") == 193485963`
  - `djb2("hello") == 261238937`
  - `djb2("Hello") == djb2_bytes(b"Hello")`
  - `djb2("café") == djb2_bytes("café".encode("utf-8"))`
  - `djb2_bytes(b"") == 5381`
  - `djb2_bytes(b"\x00") == 177573`
  - long-string results always in `0..4294967295` (ASCII, multibyte UTF-8,
    emoji, and raw `bytes` inputs)
  - `djb2(123)`, `djb2(None)` raise `TypeError`
  - `djb2_bytes("abc")` raises `TypeError`
  - extra: `djb2_bytes(bytearray(b"Hello"))` accepted (spec allows bytearray)
- Verified every expected constant independently by running the reference
  algorithm in a scratch snippet before writing the tests; all values matched
  the spec exactly.

## What I did not do

- Did not create or modify `unionfind.py`, `bizdays.py`, or their tests (other
  process cards own those).
- Did not modify any pre-existing file (only the two files above plus the two
  `team/` files required by the workflow).
- Did not add third-party dependencies; `pytest` was already listed in
  `requirements-dev.txt` but was not installed in the environment, so I
  installed it (`python3 -m pip install -r requirements-dev.txt`) to run the
  checks. No repository file was changed by that install.
- Did not commit or push.

## Checks run and results

1. `python3 -m pytest tests/test_djb2hash.py -q` → `12 passed in 0.02s` (exit 0)
2. `python3 -m pytest tests/ -q` → `48 passed in 2.30s` (exit 0)

## What the validator must pay attention to

- Both files are new; `git status` should show only `djb2hash.py`,
  `tests/test_djb2hash.py`, and the `team/` files as additions from this card
  (other cards add their own).
- The module performs no `bool` special-casing: `djb2(True)` raises
  `TypeError` anyway because `bool` is not a `str`, and `djb2_bytes(True)`
  raises `TypeError` because `bool` is not `bytes`/`bytearray`. The spec does
  not require bool handling for this component (unlike unionfind/bizdays).
- Hash values are fixed constants from the spec; they were cross-checked
  against an independent reference implementation before being asserted.
- The full-suite run (48 tests) includes tests owned by other cards; if they
  are not merged yet, that run may fail for reasons unrelated to this card.
