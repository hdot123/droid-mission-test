# Handoff: collatz-module (sub-issue #216)

## What was requested

Implement `collatz.py` in the repository root with two functions, plus `tests/test_collatz.py`:

- `sequence(n)`: return the complete Collatz sequence from positive integer `n` to 1, as a list including both the first element `n` and the final `1`. Rule: even numbers divide by 2, odd numbers become `3*n + 1`. Raise `ValueError` if `n` is not a positive integer (not an `int` type, or less than 1).
- `steps(n)`: return the number of steps from `n` to 1, defined as `len(sequence(n)) - 1`; shares `sequence`'s `ValueError` behavior.
- Required examples: `sequence(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]`, `steps(6) == 8`, `sequence(1) == [1]`, `steps(1) == 0`, `steps(27) == 111`.
- Tests must cover all examples plus `ValueError` for `n = 0`, `-1`, `1.5` (float), `"6"` (str) from **both** `sequence` and `steps`.
- Constraints: Python standard library only; `collatz.py` must not import `luhn`/`euclid`/any local module; no package directory; no CLI; `tests/test_collatz.py` tests only collatz behavior.
- Scope: owns only `collatz.py` and `tests/test_collatz.py`.

## What I did

- Created `collatz.py` with `sequence(n)` and `steps(n)`. Validation: `if not isinstance(n, int) or isinstance(n, bool) or n < 1: raise ValueError`. Note: `isinstance(n, bool)` excludes `True`/`False` (which are `int` subclasses in Python) from being accepted as valid input — a defensive choice consistent with "not an int type" in spirit; no test or spec example covers booleans.
- `sequence` iterates the 3n+1 rule until it reaches 1, appending each value; `steps` is implemented as `len(sequence(n)) - 1` exactly per spec.
- Created `tests/test_collatz.py` using `pytest.mark.parametrize` for the four invalid inputs (`0`, `-1`, `1.5`, `"6"`) against both `sequence` and `steps`, plus the five required positive examples.

## What I did not do

- Did not touch `luhn.py`, `euclid.py`, `legacy_stringkit.py`, or any other test file.
- Did not create a package directory, CLI entry point, or any local import in `collatz.py`.
- Did not commit or push (left to the workflow).

## Checks I ran and their results

All three checks from the process card, run from the repository root:

1. `python -c "import collatz; ..."` (spec assertions incl. ValueError loop over `0, -1, 1.5, '6'`) — **PASS** (exit 0).
2. `python -m pytest -q tests/test_collatz.py` — **PASS**: `13 passed in 0.02s`.
3. `python -m pytest -q` (full suite) — **PASS**: `17 passed in 0.02s`.

Note: the environment initially had no pytest (`No module named pytest`); I installed it via `python -m pip install pytest` (pytest 9.2.0) so the acceptance command could run. This is an environment setup step, not a repo change.

## Notes for the validator

- `collatz.py` validation intentionally rejects booleans (`True`/`False`) even though they are `int` subclasses; all spec'd invalid inputs (`0`, `-1`, `1.5`, `"6"`) raise `ValueError` from both functions.
- The full suite (`python -m pytest -q`) passed with 17 tests at the time of this handoff — collatz contributes 13, the pre-existing `tests/test_legacy_stringkit.py` contributes 4. If sibling processes (luhn/euclid) have landed their files, the count will be higher; the suite must still be fully green.
- Handoff and status files are at `team/handoffs/collatz-module.md` and `team/status/collatz-module.json`.
