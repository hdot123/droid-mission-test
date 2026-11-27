# Handoff: ackermann (sub-issue #956, work order #951 round-59 A)

## What was requested

Process card `ackermann`: create exactly two new files — `ackermann.py` and
`tests/test_ackermann.py` — implementing the Ackermann–Péter function per the
work-order spec, without modifying any existing file.

Spec essentials:
- `ackermann(m: int, n: int) -> int`: m=0 → n+1; n=0 → A(m−1, 1); else A(m−1, A(m, n−1)).
- Domain (tightened, fixed): m ∈ [0, 4], n ≥ 0, and when m = 4 only n = 0.
  Out of domain (including (4, 1) and all m = 4 with n ≥ 1) → ValueError.
  Non-int (including bool) → TypeError.
- (4, 1) = 65533 is documentation only (identity of the m=3 row closed form at
  n = 13, i.e. 2^16 − 3); it is NOT an acceptance point — (4, 1) must raise
  ValueError only.
- Closed forms allowed: A(0,n)=n+1, A(1,n)=n+2, A(2,n)=2n+3,
  A(3,n)=2^(n+3)−3, A(4,0)=13. Standard library only; no cross-module imports.

## What I did

- Created `ackermann.py`: validates types first (bool rejected explicitly,
  TypeError for any non-int), then domain (ValueError for m∉[0,4], n<0, and
  m=4 with n≥1), then computes via the per-row closed forms (all in-domain
  calls are O(1); the m=3 row uses `1 << (n + 3)`). Docstring records the
  tightened-domain rationale and the (4,1)/65533留档 note.
- Created `tests/test_ackermann.py` covering every acceptance point:
  - Values: (0,0)=1, (1,10)=12, (2,100)=203, (3,5)=253, (3,10)=8189, (4,0)=13.
  - Property: grid m∈[0,2] × n∈[0,12] and m=3, n∈[0,10] each compared
    one-by-one against an independent per-row closed-form reference
    (computed with `**`, not the module's `<<`).
  - ValueError: (5,0), (−1,0), (0,−1), (4,1), (4,2), plus (4, n) for n in 1..19.
  - TypeError: (1.0, 0), (0, True), plus (True,0), (0,"1"), (0,2.5), (None,0), (0,[1]).
  - Return type is `int` sanity check.
  - Deliberately NO test asserts ackermann(4, 1) == 65533, per spec.

## What I did not do

- Did not touch `pell.py`, `geohash.py`, any existing file, or any `team/**`
  path other than my own two files (`team/handoffs/ackermann.md`,
  `team/status/ackermann.json`).
- Did not add cross-module imports; module uses only the standard library
  (nothing beyond builtins).
- Did not commit or push.

## Checks run and results

1. `python3 -m pytest tests/test_ackermann.py -q` → **22 passed in 0.02s**
2. `python3 -m pytest tests/ -q` → **364 passed, 2 skipped in 17.95s** (exit 0)

The 2 skips pre-exist in the suite and are unrelated to this card.

## Notes for the validator

- The spec's exception ordering: type errors must be TypeError even when the
  value would also be out of domain (e.g. `(0, True)` → TypeError, not
  ValueError); the implementation checks types before the domain.
- `(4, 1)` must raise **ValueError** — do not accept a test that asserts the
  value 65533; the work order explicitly forbids it as an acceptance point.
- The closed-form property test intentionally re-derives values with `**`
  rather than reusing the module's bit-shift, so agreement is cross-checked
  against an independent computation.
- No `verdict.json` / `verdict.md` by-products were left behind (the full
  suite in this repo did not produce any at root; `git status` verified).
