# Handoff: bitflags (sub-issue #228)

## What was requested
Implement `bitflags.py` (standard library only, no imports of sibling modules, no package dir, no CLI) exposing:
- `define_flags(names)` — maps each name in list order to successive powers of two (1, 2, 4, ...); duplicate names raise `ValueError`; empty list returns `{}`.
- `combine(flags, *names)` — bitwise OR of the named bit values; no names → `0`; unknown name → `ValueError`.
- `contains(value, flag)` — bool: whether `value` contains bit `flag`.
- `names_of(flags, value)` — list of names with bits set, ascending by bit value; undefined bits in `value` → `ValueError`.
Plus `tests/test_bitflags.py` covering every worked example and every stated error case.

## What I did
- Created `bitflags.py` with the four functions exactly as specified (`names_of` validates undefined bits against the OR of all defined bit values, then returns names sorted ascending by bit value).
- Created `tests/test_bitflags.py` with 11 tests covering: the full worked example (`F == {"READ": 1, "WRITE": 2, "EXEC": 4}`, `combine(F, "READ", "EXEC") == 5`, `contains(5, 1) is True`, `contains(5, 2) is False`, `names_of(F, 5) == ["READ", "EXEC"]`, `names_of(F, 0) == []`, `names_of(F, 8)` raises), plus empty list, duplicate names, `combine()` with no names → 0, and unknown name in `combine`.
- Installed `pytest` (9.2.0) into the environment — it was not present (`python -m pytest` failed with "No module named pytest").

## What I did not do
- Did not touch `duration_parse.py`, `wrapwidth.py`, any other test file, `team/` paths other than my two assigned files, `.github/`, or any package directory. No CLI. No commits or pushes.

## Checks run
- `python -m pytest -q tests/test_bitflags.py` → **11 passed in 0.01s** (exit 0). This is the card's check, used verbatim.

## Notes for the validator
- The environment initially lacked pytest; I installed it with `python3 -m pip install pytest`. If the validator runs in a fresh environment, pytest must be available for the check command to work.
- Tests use `import bitflags` (module at repo root), so the check must be run from the repository root, as specified.
- `contains` returns a real `bool` (`bool(value & flag)`), so `is True`/`is False` assertions hold.
