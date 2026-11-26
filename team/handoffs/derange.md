# Handoff: derange (sub-issue #854, work order #848 并发 A 单)

## What was requested

Process card `derange` from work order #848 (第55轮并发A单): implement the derangement-count
component as **two new files only**:

- `derange.py` — `subfactorial(n: int) -> int` (子阶乘 !n, exact integers) and
  `derangements_upto(n: int) -> list[int]` returning `[!0, !1, …, !n]` (n+1 items).
- `tests/test_derange.py` — one test case per acceptance item in the card.

Input contract (both functions): `n < 0` → `ValueError`; non-`int` (including `bool`) →
`TypeError`. Standard library only; no import of `bearing`/`paritybit` or any project module;
no modification of any existing file.

## What I did

- Implemented `subfactorial` with the exact-integer recurrence
  `!n = (n - 1) * (!(n-1) + !(n-2))` (`!0 = 1`, `!1 = 0`); no floating-point arithmetic
  anywhere, so `subfactorial(20) == 895014631192902121` is a plain `int`.
- Implemented `derangements_upto` with the same recurrence over a list (returns exactly
  n+1 items) and the same shared validator `_validate_n` (bool rejected via
  `isinstance(n, bool)` first, then `isinstance(n, int)`, then `n < 0`).
- Wrote `tests/test_derange.py` covering **every** acceptance item:
  - values 0–8, 10, and 20 (with an explicit `isinstance(result, int)` exactness check);
  - `derangements_upto(0) == [1]`, `derangements_upto(5) == [1, 0, 1, 2, 9, 44]`,
    `len(derangements_upto(10)) == 11`;
  - errors: `subfactorial(-1)`/`derangements_upto(-3)` → `ValueError`;
    `subfactorial(2.5)`/`subfactorial(True)`/`derangements_upto(2.5)`/`derangements_upto(False)`
    → `TypeError`;
  - two extra guard tests: brute-force permutation check for n in 0..7 (proves !n is the
    true derangement count) and the recurrence identity for n in 2..20.

## What I did NOT do

- Did not touch any pre-existing file (`git status` shows only `?? derange.py`,
  `?? tests/test_derange.py`, plus the pipeline's pre-existing `worker-prompt.txt` /
  `worker-stream.jsonl`).
- Did not create `bearing.py`, `paritybit.py`, or their tests (other cards own those).
- Did not edit `team/**` beyond my two assigned files, nor `.github/**`.
- Did not import or depend on the other two modules (no imports at all beyond `itertools`
  and `pytest` in the test file; `derange.py` imports only `__future__`).
- Did not commit or push.

## Checks run and results

From the repository root:

1. `python3 -m pytest tests/test_derange.py -q` → **15 passed in 0.03s** (exit 0).
2. `python3 -m pytest tests/ -q` → **1 failed, 355 passed, 2 skipped in 22.06s** (exit 1).

The single full-suite failure is `tests/test_check_summary_focused_counts.py::
test_summary_block_on_r54_pack_produces_real_focused_counts`:
`FileNotFoundError: '/tmp/r54-audit/a/evidence/packs/damm/checks-output.txt'`. That test reads
fixture evidence from `/tmp/r54-audit/`, which does not exist in this environment.

**Proof it is pre-existing / unrelated to this card:** I temporarily moved my two new files out
of the tree and re-ran that test — it failed with the identical `FileNotFoundError`
(`1 failed, 4 passed`). So the failure exists on the baseline without derange's files.

No `verdict.json` / `verdict.md` by-products were produced; I ran `rm -f verdict.json verdict.md`
anyway (nothing to remove) and cleaned up my temporary hold directory.

## What the validator must pay attention to

- The module-level contract is order-sensitive: type validation (`TypeError`) happens before
  sign validation (`ValueError`), so `subfactorial(True)` and `subfactorial(2.5)` raise
  `TypeError` (not `ValueError`), while `subfactorial(-1)` raises `ValueError`.
- Exactness: `subfactorial(20)` must be the integer `895014631192902121`; the implementation
  uses integer-only arithmetic (no `math.factorial` float ratio, no `//` on floats).
- `derangements_upto(n)` length is always `n + 1`; `derangements_upto(0) == [1]` (not `[]`).
- Full-suite status: expect the one pre-existing environment failure above unless
  `/tmp/r54-audit/...` evidence files are present; all 355 other tests (including my 15) pass.
