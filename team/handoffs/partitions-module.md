# Handoff: partitions-module (sub-issue #643)

## What was requested

Work card `partitions-module` from work order #632 (round 47, concurrent card C): implement `partitions.py` with `partitions(n: int) -> int` returning the integer partition number p(n) (exact int), and `tests/test_partitions.py` covering every acceptance item verbatim. Validation rules: `n` must be `int` with `bool` rejected; `n < 0` raises `ValueError`; non-int (float, str, bool) raises `TypeError`. Convention: `partitions(0) == 1`. Only the standard library; must not import the other new modules. Only these two files plus the two team files may be created; no existing file may be modified.

## What I did

- Created `partitions.py`: `partitions(n)` validates `n` (bool rejected via `isinstance(n, bool)` first, then `isinstance(n, int)`; negative → `ValueError`; non-int → `TypeError`), then computes p(n) with Euler's pentagonal number theorem recurrence (`p(m) = Σ (-1)^(k-1) p(m - g_k)` over generalized pentagonal numbers `g_k = k(3k-1)/2` and `k(3k+1)/2`). Exact integer arithmetic, O(n^1.5) time, no non-stdlib imports, no imports of other deliverable modules.
- Created `tests/test_partitions.py`: parametrized value test covering all 17 acceptance values (0,1,2,3,4,5,6,7,8,9,10,15,20,25,30,50,100 with expected 1,1,2,3,5,7,11,15,22,30,42,176,627,1958,5604,204226,190569292), a dedicated `partitions(0) == 1` test, `partitions(-1)` → `ValueError`, and `partitions(2.5)`, `partitions("5")`, `partitions(True)` → `TypeError`.

## What I did not do

- Did not touch `bifid.py`, `rotate2d.py`, or their tests (other process cards own those).
- Did not modify any pre-existing file (roman.py, legacy_stringkit.py, existing tests, docs, schemas, scripts, etc.).
- Did not commit or push.
- Did not add dependencies; `pytest` was installed into the environment (it was missing) from `requirements-dev.txt` — no repo file was changed by this.

## Checks run and results

1. `python3 -m pytest tests/test_partitions.py -q` → **22 passed in 0.02s**
2. `python3 -m pytest tests/ -q` → **51 passed in 2.76s** (includes all pre-existing tests plus my 22)

Note: the first attempt failed with `No module named pytest`; installing pytest per `requirements-dev.txt` (`pytest>=7.4.0`) resolved it. No test failures at any point.

## Validator notes

- Every acceptance item from the work order has a corresponding test case in `tests/test_partitions.py`; the value list matches the spec verbatim.
- Error-type precedence: bool is rejected before the `int` check, so `partitions(True)` raises `TypeError` (not `ValueError`), even though `bool` subclasses `int` in Python.
- `partitions(0) == 1` is asserted twice (in the parametrized table and a dedicated test) to satisfy the explicit acceptance line.
- Only `partitions.py` and `tests/test_partitions.py` were created beyond the two required team files (`team/handoffs/partitions-module.md`, `team/status/partitions-module.json`).
