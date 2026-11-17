# Handoff: ipaddr-module (sub-issue #64)

## What was requested
Implement `ipaddr.py` in the repository root with exactly four functions, plus a
real pytest test file `tests/test_ipaddr.py`, per process card `ipaddr-module`
under work order #59 (领班制 v2.6.2, 第十三轮).

Required behavior:
1. `is_valid_ipv4(s)` — strict IPv4 check: exactly four dot-separated decimal
   octets, each 0–255, no leading zeros ("0" itself allowed), no spaces.
   Returns True/False, never raises for malformed input.
2. `to_int(s)` — dotted quad → 32-bit int; raises `ValueError` for invalid input.
3. `from_int(n)` — inverse; `n` must be an `int` in `0..2**32-1` inclusive,
   otherwise `ValueError`; returns dotted-quad string.
4. `is_private(s)` — RFC 1918 check (10/8, 172.16/12, 192.168/16); raises
   `ValueError` for an invalid address.

## What I did
- Created `ipaddr.py` (standard library only, no third-party imports):
  - A private `_parse_ipv4(s)` helper implements the strict rules once and is
    shared by all four public functions:
    - `isinstance(s, str)` check, then `s.split(".")` must yield exactly 4 parts;
    - each part must be non-empty, all decimal digits (`0123456789` set), no
      leading zero unless the part is exactly `"0"`, and `int(part) <= 255`;
    - any violation raises `ValueError`.
  - `is_valid_ipv4(s)` wraps `_parse_ipv4` in `try/except ValueError` → returns
    `False`, so it never raises (covers `None`, bytes, ints, lists, etc.).
  - `to_int(s)` unpacks the four octets and computes
    `(a<<24)|(b<<16)|(c<<8)|d`.
  - `from_int(n)` rejects `bool` and non-`int` types (including floats, strings,
    `None`, `complex`) and out-of-range values with `ValueError`, then formats
    the four bytes.
  - `is_private(s)` parses the address (raising `ValueError` on invalid input)
    and returns `True` for 10/8, 172.16–172.31, or 192.168/16.
- Created `tests/test_ipaddr.py` with 14 test functions and real assertions
  covering every rule from the card, including all five required examples:
  - `to_int("192.168.0.1") == 3232235521`
  - `from_int(3232235521) == "192.168.0.1"`
  - `is_valid_ipv4("01.2.3.4") is False`
  - `is_private("172.31.255.255") is True`
  - `is_private("172.32.0.1") is False`
  plus boundary/round-trip cases (0.0.0.0, 255.255.255.255, 3/5 octets,
  octet 256, empty octet, spaces, `from_int(-1)`/`from_int(2**32)`,
  `is_private` on 10.0.0.1 / 10.255.255.255 / 11.0.0.1 / 192.168.1.1 /
  192.169.0.1, and `is_private` raising on invalid input).
- Also verified the five work-order examples in a direct `python -c` run
  ("all examples OK").

## What I did NOT do
- Did not create or modify `luhn.py`, `csv_parse.py`, or any other test file
  (those belong to sibling process cards).
- Did not modify any pre-existing repository file (`README.md`, `.github`,
  `worker-prompt.txt`, `worker-stream.jsonl`, etc.).
- Did not commit or push anything; only created `ipaddr.py`,
  `tests/test_ipaddr.py`, `team/handoffs/ipaddr-module.md`, and
  `team/status/ipaddr-module.json`.
- pytest was not installed in the environment; I installed it with
  `python -m pip install pytest` (pytest 9.2.0) so the required check could run.

## Checks I ran and results
- `python -m pytest -q tests/test_ipaddr.py` → `14 passed in 0.03s` (exit 0).
- Work-order example verification via `python -c` → `all examples OK`.
- `git status --short` → only new untracked files: `ipaddr.py`, `tests/`,
  `__pycache__/` (generated), plus the pre-existing untracked
  `worker-prompt.txt` / `worker-stream.jsonl` that were already there before I
  started. No tracked file was modified.

## Notes for the validator
- The exact card check `python -m pytest -q tests/test_ipaddr.py` passes;
  note the environment needed pytest installed first (not a repo change).
- `is_valid_ipv4` is deliberately tolerant of non-string types (returns False)
  per "never raises for malformed input"; `to_int`/`is_private` raise
  `ValueError` for the same inputs, and `from_int` rejects `bool` explicitly
  (so `from_int(True)` raises even though `bool` subclasses `int`).
- RFC 1918 boundaries are exact: 172.16.0.0–172.31.255.255 is private,
  172.32.0.1 and 172.15.255.255 are not; tested.
- `tests/test_ipaddr.py` imports `ipaddr` as a top-level module, so pytest must
  be run from the repository root (as the card check does).
