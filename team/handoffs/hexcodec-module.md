# Handoff: hexcodec-module (sub-issue #32)

## What was requested
Process card `hexcodec-module` for work order #30 (领班制 v2.6.1 确认轮):

- Create `hexcodec.py` in the repository root with:
  - `encode(data: bytes) -> str`: lowercase hex string; `encode(b"\xde\xad") == "dead"`, `encode(b"") == ""`.
  - `decode(s: str) -> bytes`: inverse conversion; `decode("dead") == b"\xde\xad"`, `decode("") == b""`; raises `ValueError` on odd length or non-hex characters.
- Create `tests/test_hexcodec.py` with pytest tests covering the examples plus round-trip and `ValueError` cases; the test file must only test `hexcodec`.
- Standard library only; no CLI, no `__main__`, no package directory, no imports of other project modules.
- Verify with `python -m pytest -q tests/test_hexcodec.py`.

## What I did
- Wrote `hexcodec.py` with `encode` and `decode`.
  - `decode` performs an explicit odd-length check, then a strict per-character hex check (only `0123456789abcdefABCDEF`), then delegates to `bytes.fromhex`. This is deliberate: `bytes.fromhex` silently accepts ASCII whitespace as separators, which the spec forbids ("含非法字符时抛 ValueError"); the explicit check makes `"de ad"` raise `ValueError`.
  - Non-`str`/non-bytes inputs raise `TypeError` (not covered by the spec, added defensively; not tested as required behavior).
- Wrote `tests/test_hexcodec.py` with 8 tests: both examples, empty inputs, full byte-range/lowercase property, round-trip, odd-length `ValueError`, and non-hex `ValueError` (including whitespace).
- Created `team/handoffs/hexcodec-module.md` and `team/status/hexcodec-module.json`.

## What I did NOT do
- Did not touch `tally.py`, `initials.py`, or any other test file (owned by other processes).
- Did not add a CLI, `__main__` block, `__init__.py`, or package directory.
- Did not commit or push.

## Checks run
- `python -m pytest -q tests/test_hexcodec.py` → **8 passed** (exit code 0).
- Note: `pytest` was not installed in this environment; I installed it with `pip3 install pytest` to run the check. No repository files were changed by that install.

## For the validator
- The acceptance criterion in the work order body says the `tally.py` pass line is 70 while the 交付物 section says 60. That conflict belongs to the `tally` process card, not this one; `hexcodec` behavior is unaffected.
- Watch that `decode` rejects whitespace (e.g. `"de ad"`) even though stock `bytes.fromhex` would accept it — this is intentional strictness per the spec.
- Only `hexcodec.py`, `tests/test_hexcodec.py`, and the two team files under `team/` were created by this process.
