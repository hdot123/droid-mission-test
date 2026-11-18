# Handoff: manchester-codec (sub-issue #319)

## What was requested
Process card `manchester-codec` under work order #312 (第三十八轮 · 并发 A 单). Owns exactly two deliverables:

- `manchester.py` — Manchester coding (IEEE 802.3 convention):
  - `encode(bits: str) -> str`: input string of `0`/`1`; each bit maps to two symbols, `0` → `10`, `1` → `01`; any other character raises `ValueError`; empty string returns empty string.
  - `decode(symbols: str) -> str`: inverse operation; odd length or illegal symbol pairs (`00`, `11`, etc.) raise `ValueError`; empty string returns empty string.
- `tests/test_manchester.py` — one test case per acceptance point.

Constraints: only these two files created; no existing file modified; standard library only; no imports of `base32hex`, `crc8`, or other non-stdlib modules.

## What I did
- Created `manchester.py` with `encode` and `decode` as specified (no imports at all; no third-party or sibling-module dependencies).
- Created `tests/test_manchester.py` covering every acceptance point:
  - `encode("1010") == "01100110"`
  - `encode("0") == "10"`
  - `encode("1") == "01"`
  - `decode("01100110") == "1010"`
  - `decode("00")` raises `ValueError`
  - round-trip identity on `"11001010"`
  - `encode` raises `ValueError` on characters other than `0`/`1`
  - `decode` raises `ValueError` on odd length and on illegal pairs `11`
  - `encode("") == ""` and `decode("") == ""`
- Installed `pytest` into the environment (it was not present); this did not modify any repository file.

## What I did not do
- Did not touch `base32hex.py`, `crc8.py`, or any other existing file.
- Did not create or modify `base32hex`/`crc8` deliverables — those belong to other process cards.
- Did not commit or push.

## Checks run
- `python3 -m pytest tests/test_manchester.py -q` → `11 passed in 0.02s` (exit 0)
- `python3 -m pytest tests/ -q` → `22 passed in 0.03s` (exit 0)

Note: the full-suite run includes other team members' tests in this workspace; all green at the time of this run.

## What the validator must pay attention to
- Both deliverables are new files; `git status` should show them as additions only, with no modifications to pre-existing tracked files.
- `manchester.py` has no imports at all, so the stdlib-only constraint is trivially satisfied.
- `decode` rejects any pair other than exactly `"10"` or `"01"`, so `00`, `11`, and any other two-character pair raise `ValueError` — the tests exercise `00` and `11`.
- Validation order in `decode`: the odd-length check runs before pair iteration, so `decode("0")` raises for odd length, not for an illegal pair.
