# Handoff: motzkin (sub-issue #912, work order #902 B 单)

## What was requested

Process card "motzkin": implement `motzkin.py` exposing `motzkin(n: int) -> int` returning the Motzkin number M_n (Motzkin paths of length n over U/D/F steps, non-negative height, ending at 0; M_0 = 1), plus `tests/test_motzkin.py` covering every acceptance item. Input contract: `n < 0` → ValueError; non-int (including bool) → TypeError. The work order explicitly forbids using the Catalan-sum identity as an acceptance shortcut (direct computation against the anchor list only). Files owned: only `motzkin.py` and `tests/test_motzkin.py`.

## What I did

- Created `motzkin.py` with a single public function `motzkin(n)`:
  - Type check first: `isinstance(n, bool) or not isinstance(n, int)` → TypeError; `n < 0` → ValueError.
  - Computes directly via the standard three-term recurrence `M_n = ((2n+1)*M_{n-1} + (3n-3)*M_{n-2}) / (n+2)` with exact integer arithmetic (`//`, integral at every step). No Catalan/partition shortcuts; only the standard library.
- Created `tests/test_motzkin.py` with:
  - A parametrized anchor test over all 12 required values: (0,1), (1,1), (2,2), (3,4), (4,9), (5,21), (6,51), (7,127), (8,323), (9,835), (10,2188), (15,310572), each also asserting `type(result) is int`.
  - Explicit test for `motzkin(15) == 310572` as exact int.
  - Explicit test `motzkin(0) == 1`.
  - `motzkin(-1)` raises ValueError; `motzkin(2.0)` raises TypeError; `motzkin(True)` raises TypeError.

Total: 17 test cases (12 parametrized anchors + 5 explicit), every acceptance item has a corresponding test.

## What I did not do

- Did not touch any existing file (no modifications, deletions, or moves).
- Did not implement `line2d.py` or `extractnums.py` (other process cards), and `motzkin.py` imports neither of them (standard library only, no intra-repo imports).
- Did not commit or push.
- Did not use the Catalan identity `M_n = Σ_k C(n, 2k)·Catalan(k)` anywhere.

## Checks ran and results

1. `python3 -m pytest tests/test_motzkin.py -q` → **17 passed in 0.03s**
2. `python3 -m pytest tests/ -q` → **359 passed, 2 skipped in 21.83s** (the 2 skips are pre-existing suite skips, unrelated to this card)

No `verdict.json` / `verdict.md` by-products were produced by these runs (none found; verified after checks).

## What the validator must pay attention to

- The `motzkin(15)` result is exact integer 310572 (asserted with `type(...) is int`, not float equality).
- TypeError is checked **before** the negativity check, so bool input raises TypeError (bool is an int subclass in Python but is explicitly rejected per spec).
- The recurrence uses exact integer division; it is exact by construction of the Motzkin recurrence — no floating point involved.
- My own test count: 17 (12 anchors + 5 explicit) in `tests/test_motzkin.py`.
