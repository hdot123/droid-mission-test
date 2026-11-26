# Handoff: farey (sub-issue #931)

## What was requested

Work order #927 (round 58, batch B, card `farey`): implement `farey.py` with
`farey(n: int) -> list[tuple[int, int]]` returning the n-th Farey sequence —
all reduced fractions between 0/1 and 1/1 inclusive with denominator ≤ n,
sorted ascending as `(numerator, denominator)` tuples — plus
`tests/test_farey.py`, covering every acceptance point from the card
verbatim. Only new files; no existing file may be modified; standard library
only; no cross-module imports.

Input contract from the card:
- `n < 1` → `ValueError` (covers `farey(0)`, `farey(-3)`).
- Non-int `n`, **including bool** (`farey(True)`), → `TypeError`
  (covers `farey(2.0)`).

## What I did

Created exactly two files, nothing else:

1. **`farey.py`** — `farey(n)` uses the classic Farey recurrence
   (next-term generation from the adjacent pair with `b*c - a*d == 1`),
   which yields exactly the gcd-reduced, ascending sequence with both
   endpoints `(0, 1)` and `(1, 1)`. The type check runs before the range
   check, so `farey(True)` raises `TypeError` (bool rejected explicitly)
   rather than falling into the `ValueError` path.

2. **`tests/test_farey.py`** — one test per acceptance point:
   - `farey(1)`, `farey(4)`, `farey(5)` exact-list checks;
   - `len(farey(8)) == 23`;
   - property: for n in [1, 30] result equals, item for item, an
     independent gcd-filtered enumeration (sorted by value with
     `fractions.Fraction`);
   - property: length == 1 + Σ φ(k) for k = 1..n (n in [1, 30]);
   - property: for n in [1, 15], every adjacent pair satisfies
     `b*c - a*d == 1`;
   - `farey(0)` / `farey(-3)` raise `ValueError`;
   - `farey(2.0)` / `farey(True)` (plus `False`, `"2"`, `None`) raise
     `TypeError`;
   - extras: endpoints present, tuples reduced (`gcd == 1`), strictly
     ascending order, denominators ≤ n.

## What I did NOT do

- Did not touch `kmpsearch.py`, `lensarea.py`, or any existing file
  (verified: only `farey.py` and `tests/test_farey.py` are new from this
  card; no pre-existing file was edited).
- Did not add cross-module imports (module imports nothing at all).
- Did not commit or push (left to the workflow).
- Did not implement or test anything outside the `farey` card.

## Checks I ran and results

- `python3 -m pytest tests/test_farey.py -q` → **10 passed** (exit 0).
- `python3 -m pytest tests/ -q` → **352 passed, 2 skipped** (exit 0).
  (342 pre-existing + 10 new; the 2 skips are pre-existing suite skips.)

No `verdict.json` / `verdict.md` by-products appeared in the repo root;
nothing needed cleanup.

## Notes for the validator

- Run on Python 3.14.4 in this environment; all listed acceptance values
  match exactly (including `len(farey(8)) == 23`).
- The spec examples are the norm: tuples must be reduced — F5 contains
  `(1, 2)`, never `(2, 4)`; both `(0, 1)` and `(1, 1)` are present.
- `bool` is rejected as `TypeError` before the `n < 1` check; do not
  accept `farey(True)` as `ValueError`.
- Boundary behavior to spot-check independently: `farey(1) == [(0, 1), (1, 1)]`
  and the adjacent-determinant property at n = 1 (trivially vacuous — only
  one adjacent pair).
