# Handoff: partitions-numtheory (sub-issue #740)

## What was requested (work order #729 · item 1)

Implement `partitions.py` and `tests/test_partitions.py` only:

- `partitions(n: int) -> int` returning the partition number p(n) as an exact integer; `partitions(0) == 1` (empty partition).
- Validation: n must be int with `bool` rejected; `n < 0` raises `ValueError`; non-int (float, str, bool) raises `TypeError`.
- Standard library only; must not import from other project modules (bifid, rotate2d, legacy_stringkit, roman, ...).
- Test every acceptance item: values for n = 0,1,2,3,4,5,6,7,8,9,10,15,20,25,30,50,100 (1,1,2,3,5,7,11,15,22,30,42,176,627,1958,5604,204226,190569292); `partitions(-1)` → ValueError; `partitions(2.5)`, `partitions("5")`, `partitions(True)` → TypeError.
- Add only these two new files; touch no pre-existing file.

## What I did

- Created `partitions.py`:
  - `partitions(n)` validates via `isinstance(n, bool) or not isinstance(n, int)` → TypeError, then `n < 0` → ValueError.
  - Core computation uses Euler's pentagonal number theorem recurrence `p(n) = Σ_k (-1)^(k-1) [p(n-g_k) + p(n-g_{-k})]` with `g_k = k(3k-1)//2`, memoized with `functools.lru_cache`. Exact arbitrary-precision integers throughout; `partitions(100)` returns 190569292 exactly.
- Created `tests/test_partitions.py` with pytest.mark.parametrize covering all 17 value items, plus `ValueError` for -1 and `TypeError` for 2.5 / "5" / True — one test case per acceptance item (21 test cases total when parameter expansion counts individually).
- Installed dev requirements (`pip install -r requirements-dev.txt`: jsonschema, pytest) so the checks could run; this only touches the environment, not repository files.

## What I did NOT do

- Did not create or modify `bifid.py`, `rotate2d.py`, or any other process's files.
- Did not modify any pre-existing repository file (only the two new files listed above plus the two team files `team/handoffs/partitions-numtheory.md` and `team/status/partitions-numtheory.json`).
- Did not commit or push.
- Did not import from any project module (only `functools` from stdlib).

## Checks run and results

1. `python3 -m pytest tests/test_partitions.py -q` → **21 passed** (exit 0).
2. `python3 -m pytest tests/ -q` → **124 passed** (exit 0) — the full pre-existing suite plus my new tests, no failures.

## Notes for the validator

- Every acceptance item from the process card has a direct assertion in `tests/test_partitions.py`; the parameterized table is a literal transcription of the spec values.
- The pentagonal recurrence's sign alternates by k parity (`sign = 1 if k % 2 == 1 else -1`), applied to both the `+g_k` and `-g_k` terms — this matches Euler's theorem and is verified against all 17 spec values, including p(100).
- `bool` is rejected before the negative check, so `partitions(True)` raises TypeError (not silently 1).
- Memoization is per-process only (lru_cache on a module-level helper); no state is persisted between tests.
