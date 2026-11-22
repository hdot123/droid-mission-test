# Handoff: nthprime (#767)

## What was requested

Sub-issue #767 of work order #762 (round 52, concurrent B batch): implement `nthprime.py` and `tests/test_nthprime.py` only, per the verbatim spec below.

Spec:
- `nth_prime(n: int) -> int`: 1-based counting (the 1st prime is 2). `n` must be `int` (bool rejected); non-int raises `TypeError`; `n < 1` raises `ValueError`.
- Stdlib only; must not import the other two modules (`dijkstra`, `windscale`).

Acceptance items (each has a corresponding test case):
- Values: `nth_prime(1) == 2`, `(2) == 3`, `(3) == 5`, `(4) == 7`, `(5) == 11`, `(6) == 13`, `(10) == 29`, `(25) == 97`, `(50) == 229`, `(100) == 541`, `(1000) == 7919`.
- `nth_prime(0)`, `nth_prime(-3)` raise `ValueError`.
- `nth_prime(2.0)`, `nth_prime("3")`, `nth_prime(True)` raise `TypeError`.

## What I did

Created exactly two new files:
- `nthprime.py` — `nth_prime(n)`: validates `isinstance(n, bool)` or non-`int` → `TypeError`; `n < 1` → `ValueError`; then trial division (divisors up to `sqrt(candidate)`, primes accumulated as found) to produce the nth prime. No imports of any repo module; stdlib only (none needed beyond builtins).
- `tests/test_nthprime.py` — four tests: `test_first_six_primes` (1–6), `test_larger_values` (10/25/50/100/1000), `test_non_positive_raises_value_error` (0, -3), `test_non_int_raises_type_error` (2.0, "3", True). Style follows existing `tests/test_roman.py` (bare `pytest.raises`, module-level import).

## What I did not do

- Did not touch `dijkstra.py`, `windscale.py`, or any other process's files.
- Did not modify any pre-existing file (only additions).
- Did not import `dijkstra` or `windscale` (spec forbids cross-imports).
- Did not commit or push (workflow does that).

## Checks run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_nthprime.py -q` | 4 passed in 0.01s |
| `python3 -m pytest tests/ -q` | 141 passed, 1 skipped in 14.35s |

Note: `pytest` was not installed in the environment initially (`No module named pytest`); installed it via `python3 -m pip install -q -r requirements-dev.txt` (jsonschema + pytest, both already pinned in `requirements-dev.txt`). The full-suite skip is pre-existing (not related to this change).

## What the validator must pay attention to

- Only `nthprime.py` and `tests/test_nthprime.py` were added by this process; `team/handoffs/nthprime.md` and `team/status/nthprime.json` are also written as required by the harness.
- `nth_prime` rejects `bool` explicitly before the general int check, so `nth_prime(True)` raises `TypeError` (not silently treated as 1).
- The 1000th-prime case (7919) is covered; trial division is fast enough (test file runs in ~0.01s).
- Full-suite count (141 passed, 1 skipped) includes other workers' concurrent additions; a validator should re-run both checks after merge.
