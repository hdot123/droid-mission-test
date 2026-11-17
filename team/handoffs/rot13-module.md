# Handoff: rot13-module (sub-issue #139)

## What was requested
Implement `rot13.py` exposing `apply(text)` that performs ROT13 on English letters only (a-z, A-Z), preserving case and passing every other character through unchanged, with the involution property `apply(apply(x)) == x`. Create `tests/test_rot13.py` covering: a simple word (`apply("abc") == "nop"`), case preservation (`apply("AbC") == "NoP"`), non-letter characters preserved (punctuation, digits, spaces), the `apply("Hello, World!")` round-trip, and the involution property on a mixed string. Standard library only; no imports of other project modules, no package directory, no CLI. Only `rot13.py` and `tests/test_rot13.py` may be created/edited.

## What I did
- Created `rot13.py` with a `str.maketrans` table (built once at import from `string.ascii_uppercase`/`ascii_lowercase`, shifting each letter by 13 within its case) and `apply(text)` returning `text.translate(_TABLE)`. Non-letters are untouched by construction; double application restores the original.
- Created `tests/test_rot13.py` with 6 pytest tests: simple word, case preservation, non-letter preservation, punctuation/digits/spaces preserved, `Hello, World!` round-trip, and involution on a mixed string.
- Wrote this handoff and `team/status/rot13-module.json`.

## What I did NOT do
- Did not touch `palindrome.py`, `fizzbuzz.py`, any other test file, `team/**` (other than my two assigned team files), or `.github/**`.
- Did not commit or push.
- Did not add a CLI, package directory, or any non-standard-library dependency.

## Checks run and results
- Verbatim check command from the card, run from the repository root:
  `python -m pytest -q tests/test_rot13.py`
  - First attempt failed with `No module named pytest` (pytest was not installed in the environment).
  - Installed pytest (`python -m pip install -q pytest`), then re-ran the check command: **6 passed in 0.01s** (exit code 0).

## Notes for the validator
- The only deviation from a bare run of the check command was the environment prerequisite: pytest had to be installed first. The check command itself was then run verbatim and passed.
- `rot13.py` imports only `string` (standard library) and defines only `apply`. The tests import `rot13` via `sys.path` insertion of the repo root, not via package `__init__` files (no package directory exists).
- Scope held: only `rot13.py`, `tests/test_rot13.py`, and the two assigned team files were created.
