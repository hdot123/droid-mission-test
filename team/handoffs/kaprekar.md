# Handoff: kaprekar (sub-issue #885, work order #878 第56轮 C 单)

## What was requested

Implement the four-digit Kaprekar routine as exactly two new files, with no edits to any existing file:

- `kaprekar.py` — `kaprekar_steps(n: int) -> int` (steps to reach 6174, 6174 itself = 0) and `kaprekar_trajectory(n: int) -> list[int]` (full trajectory including start and 6174). Each step: descending-order digits minus ascending-order digits, intermediate values sorted as 4 digits with leading zeros (999 participates as 0,9,9,9); trajectory records integer values (999, not "0999"). Input convention: n outside 1000..9999 raises ValueError; four identical digits raise ValueError; non-int including bool raises TypeError (both functions).
- `tests/test_kaprekar.py` — a test case for every one of the 13 stated acceptance points, including an exhaustive-style sweep of the legal domain for the "reaches 6174 within ≤ 7 steps" property.

Explicitly out of scope: power conversion (A 单 energyconv / this card's sibling powerconv), squeezing, collatz (this routine is digit-sort subtract, not 3n+1), any edit to `team/**` by other owners, `.github/**`, or any existing repo file.

## What I did

- Created `kaprekar.py` (standard library only, no imports of sibling components):
  - `_check_input`: `bool` or non-`int` → `TypeError`; n outside 1000..9999 → `ValueError`; four identical digits → `ValueError`.
  - `_step`: zero-pads to 4 digits (`"%04d" % n`), sorts ascending, computes `descending - ascending`.
  - `_walk`: builds the trajectory to 6174 with a cycle guard (`RuntimeError` if a cycle is hit without reaching 6174 — unreachable for this domain, guarded defensively).
  - `kaprekar_steps` = `len(trajectory) - 1`; `kaprekar_trajectory` = trajectory list.
- Created `tests/test_kaprekar.py` covering all 13 acceptance points:
  - Points 1–5: exact-value tests for 6174/1000/2111 (steps and trajectory).
  - Point 6: exhaustive sweep `range(1000, 10000)` skipping the 9 repeated-digit numbers — asserts each trajectory starts at n, ends at 6174, `0 <= steps <= 7`, integer-typed entries, and `len(trajectory) - 1 == steps`.
  - Points 7–13: ValueError/TypeError cases for both functions where applicable (999, 10000, 1111, 7777, 2222, "1000", True).
  - Extra: boundary values (0, -1, 12345), all nine repeated digits through both functions, non-int types (`False`, `1000.0`, `None`, `[1000]`) through both functions, and a steps/trajectory consistency check.

## What I did NOT do

- Did not create or modify `powerconv.py`, `squeeze.py`, or their tests (owned by sibling cards).
- Did not edit, modify, or delete any pre-existing file; did not touch `team/**` beyond my own two required files, nor `.github/**`.
- Did not commit or push (workflow handles that).
- Did not use anything outside the Python standard library.

## Checks run and results

Both run from repository root, verbatim from the process card:

1. `python3 -m pytest tests/test_kaprekar.py -q` → **34 passed** (0.13s).
2. `python3 -m pytest tests/ -q` → **376 passed, 2 skipped** (21.56s). The 2 skips are pre-existing suite skips unrelated to this card.

No `verdict.json` / `verdict.md` by-products appeared from these runs; none needed cleanup.

## What the validator must pay attention to

- **Zero-padded sorting is load-bearing**: `_step` uses `"%04d" % n` so 999 sorts as 0,9,9,9. The 1000 trajectory `[1000, 999, 8991, ...]` and 2111 trajectory both pass through 999; a regression to unpadded sorting would fail points 4–5.
- **Integer-valued trajectory**: entries are `int` (999, not "0999"); assert `isinstance(..., int)` is covered in the domain sweep.
- **bool rejection**: `kaprekar_steps(True)` must raise `TypeError` (bool is rejected before the range check), covered by points 13 and the parametrized non-int test.
- **Exhaustive domain sweep** in `test_domain_every_legal_number_reaches_6174_within_seven_steps` iterates all 8991 legal numbers — this is the guard for the ≤7 property, not a sample.
- Files delivered: `kaprekar.py`, `tests/test_kaprekar.py` (new only); plus this handoff and `team/status/kaprekar.json`.
