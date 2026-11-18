# Handoff — caesar-cipher (sub-issue #366, process card for work order #348)

## What was requested
Implement `caesar.py` with `shift(text: str, n: int) -> str` as one of three independent classical-cipher/number-theory components (round 40 · concurrent unit E). Only `caesar.py` and `tests/test_caesar.py` were in scope for this process card. Requirements, verbatim from the work order:

- Shift ASCII letters by `n` positions (`n` taken modulo 26; negative `n` shifts backward), preserve case, leave all non-letter characters unchanged.
- Acceptance points, each requiring a corresponding test:
  - `shift("abc", 1) == "bcd"`
  - `shift("xyz", 3) == "abc"`
  - `shift("Abc XyZ", 2) == "Cde ZaB"`
  - `shift("Hello, World!", 13) == "Uryyb, Jbeyq!"`
  - `shift("abc", 26) == "abc"`
  - `shift("abc", -1) == "zab"`
  - `shift("", 5) == ""`
  - `shift("123 !", 7) == "123 !"`
- Constraints: only new files; standard library only; no imports of other task modules (vigenere/euclid).

## What I did
- Created `caesar.py` (new): implements `shift` via `n %= 26`, then per-character range checks — `'a'..'z'` and `'A'..'Z'` are shifted within their own case band using modular arithmetic; everything else is appended unchanged. Short-circuits when `n % 26 == 0`. No imports beyond the module docstring; standard library only.
- Created `tests/test_caesar.py` (new): 8 tests, one per acceptance point, named descriptively (`test_shift_forward_one`, `test_shift_wraps_around`, `test_shift_preserves_case_and_spaces`, `test_shift_rot13`, `test_shift_full_rotation_is_identity`, `test_shift_negative_moves_backward`, `test_shift_empty_string`, `test_shift_non_letters_unchanged`).

## What I did not do
- Did not create or touch `vigenere.py`, `euclid.py`, `tests/test_vigenere.py`, or `tests/test_euclid.py` — those belong to sibling process cards.
- Did not modify any pre-existing file (including `README.md`, `legacy_stringkit.py`, `roman.py`, existing tests, or git-tracked files).
- Did not commit or push; left that to the workflow.
- Did not import from any other task module.

## Checks run and results
From the repository root:

1. `python3 -m pytest tests/test_caesar.py -q` → `8 passed in 0.01s`
2. `python3 -m pytest tests/ -q` → `19 passed in 0.02s`

Note: `pytest` was not initially installed in the environment; I installed it with `python3 -m pip install pytest` (version 9.2.0) to run the required checks. That is an environment setup step, not a repository change.

## Notes for the validator
- The two checks above are the process card's exact commands and both pass on the merged tree as of this handoff (19 tests total = 8 caesar + 11 pre-existing).
- `caesar.py` is importable from the repo root with no package wiring (flat module, tests import `from caesar import shift`), matching how the existing tests import `roman`/`legacy_stringkit`.
- Every one of the 8 acceptance points has a dedicated, individually named test case — no combined/parameterized test, so each criterion is individually visible in the test output.
- Scope is strictly the two files listed in `files`; no other repository file was created or modified by this process.
