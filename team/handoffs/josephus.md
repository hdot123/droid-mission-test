# Handoff: josephus (sub-issue #920, work order #903 三件之一)

## What was requested

Process card #920: implement `josephus.py` at the repository root plus `tests/test_josephus.py`, standard library only, no imports of `decibel` or `circle`, no modifications to any existing file. Spec and acceptance points verbatim from work order #903 section 一:

- `josephus(n: int, k: int) -> int` — n people in a ring, 0-based numbering, count k people from the current position and eliminate the k-th, until one remains; return the survivor.
- `n < 1` or `k < 1` → ValueError; non-int (including bool) → TypeError.
- Acceptance points: `josephus(5, 2) == 2`, `josephus(7, 3) == 3`, `josephus(10, 2) == 4`, `josephus(1, 9) == 0`, property `josephus(n, 1) == n - 1` for any n, full-domain n ≤ 40 / k ≤ 9 agreement with a per-step elimination simulation, k = 2 agreement with the closed form (n = 2^m + L → survivor 2L), `josephus(0, 2)` / `josephus(5, 0)` raise ValueError, `josephus(5.0, 2)` / `josephus(5, True)` raise TypeError.

## What I did

- Created `josephus.py` with `josephus()` implemented via the iterative recurrence `survivor = (survivor + k) % people` for people = 2..n (standard 0-based ring-counting formulation, equivalent to per-step elimination — the counting convention is "the k-th person counted is eliminated", giving `josephus(5, 2) == 2`).
- Argument validation order: type checks first (bool explicitly rejected via `isinstance(x, bool)`), then range checks (`n < 1` / `k < 1` → ValueError).
- Created `tests/test_josephus.py` with 11 tests covering every acceptance point, grouped as:
  - `TestKnownValues`: the four exact examples.
  - `TestProperties`: `k = 1 → n - 1` for n in 1..40; full-domain n ≤ 40, k ≤ 9 comparison against an independent naive per-step elimination simulation (`_simulate`); k = 2 compared against the closed form `_closed_form_k2` (highest power of 2 ≤ n, survivor = 2(n − 2^m)) for n in 1..40.
  - `TestValueErrors`: `josephus(0, 2)`, `josephus(5, 0)`.
  - `TestTypeErrors`: `josephus(5.0, 2)`, `josephus(5, True)`.
- Test file inserts the repo root on `sys.path` (mirroring how repo tests import root-level modules); no dependency on the other two round-57 modules.

## What I did not do

- Did not touch `decibel.py`, `circle.py`, or their tests (owned by sibling processes).
- Did not modify, move, or delete any existing file. `git status` after my run shows only `josephus.py` and `tests/test_josephus.py` as new files I created (the untracked `worker-prompt.txt` / `worker-stream.jsonl` predate my work and were left alone).
- No commit/push (workflow handles that). No shared/assembly artifacts, no `team/` files other than this handoff and `team/status/josephus.json`.
- Note: `verdict.json` / `verdict.md` did not appear in the repo root during my check runs; if present later they are pipeline by-products, not my deliverables.

## Checks run and results

1. `python3 -m pytest tests/test_josephus.py -q` → **11 passed** in 0.02s (exit 0).
2. `python3 -m pytest tests/ -q` → **353 passed, 2 skipped** in 20.12s (exit 0). The 2 skips are pre-existing suite skips unrelated to this card (josephus tests are all among the passes).

## Notes for the validator

- The counting convention is the pinned one: 0-based, "count k from the current position, the k-th person is eliminated". An off-by-one variant would fail `josephus(5, 2) == 2` / `josephus(7, 3) == 3`; both are asserted.
- The simulation reference in the test file is deliberately written independently of the module implementation (list + pop, elimination index `idx + k - 1`), so agreement is real cross-validation, not a mirror of the recurrence.
- Closed-form helper assumes n ≥ 1 (2^0 = 1 ≥ n always holds for the tested domain), fine for the mandated n ≤ 40 sweep.
