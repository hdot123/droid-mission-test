# Handoff: sdbmhash (sub-issue #859, work order #849 concurrent card B)

## What was requested

Implement the sdbm string-hash component of round 55's concurrent three-card batch:

- `sdbm_hash(text: str) -> int`: sdbm hash over the text's UTF-8 bytes, iterating
  `h = b + (h << 6) + (h << 16) - h` (equivalent to `h = h * 65599 + b`) with a
  32-bit unsigned truncation after every step; empty string = 0.
- `sdbm_hex(text) -> str`: 8-digit lowercase hex of `sdbm_hash` (zero-padded).
- Non-`str` input raises `TypeError`.
- Every acceptance point from the work order must have a corresponding test case.

Scope: only two new files, `sdbmhash.py` and `tests/test_sdbmhash.py`. No existing
files modified, no other deliverables, standard library only, no import of
`monthgrid.py` / `deque.py`.

## What I did

- Added `sdbmhash.py` with `sdbm_hash` and `sdbm_hex`. Input type guard first
  (`TypeError` with a message naming the offending type), then a byte loop with
  `& 0xFFFFFFFF` truncation per step; `sdbm_hex` formats via `format(..., "08x")`.
- Added `tests/test_sdbmhash.py` with 10 tests, one per acceptance point group:
  - `""` -> 0; `"a"` -> 97; `"abc"` -> 807794786
  - `sdbm_hex("") == "00000000"`; `sdbm_hex("a") == "00000061"`
  - order sensitivity (`abc` vs `acb`, `ab` vs `ba`)
  - range `0..0xFFFFFFFF` and hex length always 8 (plus lowercase charset and
    `int(hex, 16) == hash`), on ASCII, multibyte CJK, emoji, and 1000-char inputs
  - long-input hex/hash consistency
  - equivalence with the multiplicative form `h = h * 65599 + b` on a UTF-8 string
  - `TypeError` for `b"abc"` and `123`

## What I did not do

- Did not touch any pre-existing file (verified: `git status` shows only my two
  new files plus the pre-existing untracked `worker-prompt.txt` / `worker-stream.jsonl`).
- Did not create `monthgrid.py` / `deque.py` or their tests (other cards).
- Did not commit or push.
- Did not write `verdict.json` / `verdict.md`; no such by-products were produced by my runs.

## Checks run and results

1. `python3 -m pytest tests/test_sdbmhash.py -q` -> **10 passed**.
2. `python3 -m pytest tests/ -q` -> **1 failed, 350 passed, 2 skipped**.
   The single failure is `tests/test_check_summary_focused_counts.py::
   test_summary_block_on_r54_pack_produces_real_focused_counts`, which reads an
   external fixture `/tmp/r54-audit/a/evidence/packs/damm/checks-output.txt` that
   does not exist on this machine. I re-ran that test with `sdbmhash.py` and
   `tests/test_sdbmhash.py` temporarily moved out of the tree: it fails identically
   (**1 failed, 4 passed**), so it is pre-existing and unrelated to this card.

## What the validator must pay attention to

- The full-suite run is expected to show that one pre-existing failure (missing
  `/tmp/r54-audit` fixture on a clean machine); it must not be attributed to the
  sdbmhash card. The card's own check `pytest tests/test_sdbmhash.py -q` is fully green.
- `sdbm_hash` validates type before encoding, so `sdbm_hash(b"abc")` and
  `sdbm_hash(123)` raise `TypeError` (not `AttributeError` from `.encode`).
- The three batch cards are independent; `sdbmhash.py` imports nothing beyond the
  standard library and no sibling modules.
