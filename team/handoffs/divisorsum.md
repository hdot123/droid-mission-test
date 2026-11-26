# Handoff: divisorsum (sub-issue #868, work order #850 concurrent card C, round 2)

## What was requested

Implement only the divisorsum widget of the three-part round-55 card (titlecase / speedconv / divisorsum), per card #868 (retry/REVISE, branch suffix `-r2`):

- `divisorsum.py` exposing exactly three functions:
  - `divisor_sum(n: int) -> int` — sigma(n), sum of ALL positive divisors INCLUDING n itself, sigma(1) = 1.
  - `divisor_count(n) -> int` — tau(n), number of positive divisors.
  - `classify_abundance(n) -> str` — "perfect" / "abundant" / "deficient" by comparing sigma(n) with 2n.
- Input contract (all three): `n < 1` raises `ValueError`; non-`int` including `bool` raises `TypeError`.
- Every acceptance example in the card has a corresponding test case in `tests/test_divisorsum.py`.
- Standard library only; no import of `titlecase` or `speedconv`; only the six deliverable files across the whole order (my two: `divisorsum.py`, `tests/test_divisorsum.py`); modify no existing files.
- Exactly one mandated check: `python3 -m pytest tests/test_divisorsum.py -q`, must exit 0.

## What I did

- Created `divisorsum.py`:
  - `_validate(n)` shared guard: `bool` or non-`int` → `TypeError`, then `n < 1` → `ValueError`.
  - `divisor_sum` / `divisor_count` use an O(sqrt(n)) pair-wise divisor loop (stdlib only, no imports beyond builtins).
  - `classify_abundance` computes sigma via `divisor_sum` (thereby also validating) and compares against `2 * n`.
  - Module docstring carries the caliber note: sigma(n) INCLUDES n; differs from the aliquot sum.
- Created `tests/test_divisorsum.py` with 38 tests covering every acceptance example verbatim:
  - 11 `divisor_sum` value cases (1, 2, 6, 12, 28, 36, 97, 100, 360, 496, 1024).
  - 5 `divisor_count` value cases (1, 12, 36, 97, 360).
  - 9 `classify_abundance` value cases (perfect: 6/28/496; abundant: 12/18/945; deficient: 8/97/1).
  - Error cases: `divisor_sum(0)`, `divisor_sum(-5)` → `ValueError`; `divisor_sum(2.5)`, `divisor_count(True)` → `TypeError`, plus contract coverage for the other two functions (0, negative, float, bool, str).
  - Caliber tests: sigma includes n itself (sigma(12)=28, aliquot 16) and a brute-force consistency cross-check of both sigma and tau over the acceptance inputs.

## What I did NOT do

- Did not create or modify `titlecase.py` or `speedconv.py` (other cards own them).
- Did not touch any pre-existing file (only additions: the two code files plus this handoff and `team/status/divisorsum.json`).
- Did not import sibling modules; stdlib/builtins only.
- Did NOT run, fix, skip, or seed the full suite `python3 -m pytest tests/ -q`: per CARD PIN (v2) it is explicitly out of card scope. Known out-of-scope context (mention-only): the full suite exits 1 solely from a pre-existing `FileNotFoundError` for a missing `/tmp/r54-audit/` fixture inside `tests/test_check_summary_focused_counts.py`, which belongs to no process on this plan and must not be fixed, seeded, or skipped.
- Did not commit or push (workflow does that).

## Checks run and results

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_divisorsum.py -q` | PASS — `38 passed in 0.03s`, exit 0 |

## What the validator must pay attention to

- The card's mandated check is only the module-level run; it is green (exit 0). The full-suite run is a deliberate exclusion from this card's checks — do not treat its pre-existing `/tmp/r54-audit/` FileNotFoundError as a defect of this card or its artifacts.
- Deliverables are exactly: `divisorsum.py`, `tests/test_divisorsum.py`, `team/handoffs/divisorsum.md` (this file), `team/status/divisorsum.json`.
- No existing files were modified; `git status` should show only these additions plus untracked session by-products from before my run (`worker-prompt.txt`, `worker-stream.jsonl` — not mine, not touched).
