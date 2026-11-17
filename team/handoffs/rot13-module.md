# Handoff: rot13-module (sub-issue #9)

## What was requested
- Create `rot13.py` exposing:
  - `rot13(text)` — ROT13 on English letters only, preserving case, non-letters unchanged; must equal `rot_n(text, 13)`.
  - `rot_n(text, n)` — Caesar shift by any integer `n` (negative allowed), wrapping within `a-z`/`A-Z`, preserving case, non-letters unchanged.
- Create `tests/test_rot13.py` with pytest tests covering: basic rot13 of mixed case and non-letters, rot13 round-trip identity, rot_n with negative and larger-than-26 shifts, case preservation, and non-letter invariance. Tests must only cover rot13 behavior.
- Constraints: Python standard library only; no imports of other project modules; no package directories; no CLI.

## What I did
- Created `rot13.py` with `rot_n(text, n)` (single implementation doing case-preserving, wrapping shift) and `rot13(text)` delegating to `rot_n(text, 13)`.
- Created `tests/test_rot13.py` with 11 tests covering all required behaviors plus known vectors, zero shift, and empty string.
- No imports other than none (module uses only builtins); test file imports only `rot13`.

## What I did not do
- Did not create or touch `palindrome.py`, `runlength.py`, or any other test file.
- Did not create package directories or a CLI.
- Did not edit shared infrastructure, workflow files, or other team processes' files.
- Did not run the full-repo acceptance run (`python -m pytest -q` at repo root across all tests) — that is outside my scope; I ran only my check.
- Did not commit or push.

## Checks run and results
- `python -m pytest -q tests/test_rot13.py` → **11 passed** (ran from repository root).
- Note: pytest was not preinstalled; installed it with `pip install pytest` (pytest 9.2.0) to run the check. This is environment setup, not a repo change.
- One initial test failure was an error in my own test expectation (`rot_n("AbC", -5)` is `VwX`, not `WxZ`); I verified the module output is correct and fixed the test expectation. Final run: 11 passed, 0 failed.

## Validator notes
- Ensure only `rot13.py`, `tests/test_rot13.py`, `team/handoffs/rot13-module.md`, and `team/status/rot13-module.json` were added/modified by this process.
- `rot13(text)` is verified equal to `rot_n(text, 13)` for a mixed string including non-ASCII (the non-ASCII char `é` is left unchanged, as it is not an ASCII letter).
- Full acceptance (`python -m pytest -q` at repo root) depends on the other workers' modules and should be run by the acceptance process, not assumed from my check alone.
