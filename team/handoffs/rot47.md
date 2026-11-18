# Handoff: rot47 (sub-issue #394)

## What was requested
Implement `rot47.py` with `rot47(text: str) -> str`: printable ASCII (33-126) rotates by 47 via `chr(33 + (ord(c) - 33 + 47) % 94)`; characters outside 33-126 (including space) are kept as-is. Add `tests/test_rot47.py` covering every acceptance point. Standard library only; no imports of atbash or camelcase. Only add these two files; modify no existing file.

## What I did
- Created `rot47.py` implementing `rot47` exactly as specified (generator join over characters, branch on `33 <= ord(c) <= 126`).
- Created `tests/test_rot47.py` with one test per acceptance point:
  - `rot47("Hello, World!") == "w6==@[ (@C=5P"`
  - `rot47("abc") == "234"`
  - `rot47("ABC") == "pqr"`
  - `rot47("ROT47") == "#~%cf"`
  - `rot47("") == ""`
  - `rot47(" ") == " "`
  - round-trip identity: `rot47(rot47("Hello, World! 123")) == "Hello, World! 123"`

## What I did not do
- Did not create or modify `atbash.py`, `camelcase.py`, or any other existing file.
- Did not touch any `team/` file other than `team/handoffs/rot47.md` and `team/status/rot47.json`.
- Did not commit or push.

## Checks run and results
- `python3 -m pytest tests/test_rot47.py -q` — PASSED
- `python3 -m pytest tests/ -q` — PASSED (full suite, includes pre-existing tests)

## Notes for the validator
- The acceptance string `"w6==@[ (@C=5P"` matches the standard ROT47 output for `"Hello, World!"` (verified by running the check).
- Space (chr 32) is outside 33-126 and must be preserved; the implementation's branch handles this.
- The round-trip test exercises self-inversion of ROT47 on `"Hello, World! 123"` (digits rotate, spaces do not).
