# Handoff: collatz-module (sub-issue #40)

## What was requested
Implement `collatz.py` with `sequence(n)`, `steps(n)`, `peak(n)` per the work order:
- `sequence(n)` returns the full Collatz sequence from positive integer `n`, including `n` itself, ending at 1 (even → n/2, odd → 3n+1); raises `ValueError` for non-positive or non-int input (including `0`, negatives, `1.5`, `"3"`, `None`).
- `steps(n)` = `len(sequence(n)) - 1` (e.g. `steps(6) == 8`).
- `peak(n)` = max of the sequence (e.g. `peak(6) == 16`).
- `tests/test_collatz.py` covering all examples, the `n=1` case, ValueError cases, and sequence/steps/peak consistency.
- Standard library only, no package directory, no CLI, tests only for this module.

## What I did
- Created `collatz.py` with the three functions; validation uses `type(n) is not int` so `bool`/floats/strings are rejected, and `n < 1` rejects 0/negatives.
- Created `tests/test_collatz.py` (18 tests): example sequence, `sequence(1)`, start/end invariants, steps/peak examples, parametrized ValueError cases (`0, -1, -7, 1.5, 2.0, "3", None, [3]`), and consistency checks for `n in {1,2,3,6,27}`.

## What I did NOT do
- Did not touch `b64url.py`, `piglatin.py`, their tests, or any file outside `collatz.py`, `tests/test_collatz.py`, and `team/` handoff/status files.
- Did not build a package directory, CLI, or any non-standard-library dependency in the code.
- Did not commit or push.

## Checks run and results
1. `python -m pytest -q tests/test_collatz.py` — initially failed because `pytest` was not installed (`No module named pytest`); after `pip install pytest`, re-run via `python3 -m pytest -q tests/test_collatz.py` → **18 passed**.
2. `python3 -c "from collatz import sequence, steps, peak; assert sequence(6)==[6,3,10,5,16,8,4,2,1]; assert steps(6)==8; assert peak(6)==16; assert sequence(1)==[1]"` → **passed** (`checks ok`).

## What the validator must pay attention to
- `pytest` may need to be installed in the environment (`pip install pytest`) before `python -m pytest -q` works; this is an environment prerequisite, not a code issue.
- Input validation is strict: `type(n) is not int` means `True`/`False` (bool is an int subclass) and `2.0` are rejected — this matches the spec's "non-int types such as 1.5" requirement.
- The module intentionally does not import or reference the other two modules.
