# Handoff: fenwick (sub-issue #966, work order #952 B 单)

## What was requested
Implement `fenwick.py` (Fenwick tree / binary indexed tree) per the process-card spec, plus
`tests/test_fenwick.py`, as the only two owned deliverable code files.

Spec highlights implemented verbatim:
- `FenwickTree(values)` from a list of int/float elements, with an **internal copy** of the input list.
- Operations: `add(index, delta)`, `prefix_sum(index)`, `range_sum(lo, hi)` (closed interval),
  `total()` (0 for empty tree), `to_list()`, `len(tree)`. All indices 0-based.
- Validation semantics:
  - `IndexError` for out-of-bounds index (either endpoint of `add` / `prefix_sum` / `range_sum`).
  - `ValueError` for `range_sum` with `lo > hi`.
  - `TypeError` for non-list container, non-numeric element or delta, or index not int (bool counts as non-int).

## What I did
- `fenwick.py`: 1-based BIT internally plus a copied `_data` array for `to_list()`;
  type checks reject `bool` for numbers and indices (`_is_number` / `_check_index`);
  type check runs before bound check.
- `tests/test_fenwick.py`: 18 tests covering every acceptance item:
  - Examples: `prefix_sum(2) == 8`, `range_sum(1,3) == 6`, `total() == 14`, empty-tree `total()/len()`.
  - Property test (seeded `random.Random(5906)`): random sequences length 0–20 with random
    add sequences, op-by-op agreement with a naive list model and with an **independent
    0-based BIT implementation**, plus `to_list()`/`total()`/`range_sum` agreement
    (float comparisons via `pytest.approx` because summation order differs).
  - Pinned non-random 0-based BIT cross-check.
  - Internal-copy test (mutate original list after construction).
  - All TypeError cases (`"123"`, `[1, "a"]`, `[True]`, `add(0, "x")`, plus bool/float index cases).
  - IndexError cases (`add(1, 5)`, `prefix_sum(-1)`, extra range endpoints).
  - ValueError case (`range_sum(1, 0)`).
  - Extra behavior: add-then-query, empty-tree queries, float values.

## What I did NOT do
- Did not touch `bwt.py`, `bezier.py`, or any pre-existing file (only the two owned new
  code files plus the two required team files).
- No `bwt`/`bezier` imports; standard library only in the implementation (`fenwick.py`
  imports nothing).
- Did not commit or push.
- Out of scope per card: work-order acceptance items (a)–(j) beyond my three-file B 单 —
  only the fenwick component is mine.

## Checks run and results
1. `python3 -m pytest tests/test_fenwick.py -q` → **18 passed** (exit 0).
   (First run had 1 failure: float summation-order mismatch in the property test; fixed by
   comparing with `pytest.approx(rel=1e-9, abs=1e-9)` — a test-only fix, semantics unchanged.)
2. `python3 -m pytest tests/ -q` → **360 passed, 2 skipped** (exit 0).

## Notes for the validator
- Exception precedence: type checks run before bound checks, so `prefix_sum("a")` is
  TypeError, `prefix_sum(-1)` is IndexError. `range_sum(1, 0)` on a 2-element tree is
  ValueError (both endpoints in bounds first).
- `bool` is rejected as an index and as a numeric value/delta, per the "含 bool" wording.
- The property test uses fixed seed 5906 — deterministic.
- Any `verdict.json` / `verdict.md` in the repo root are pipeline by-products of the test
  run, not deliverables; removed before finishing.
