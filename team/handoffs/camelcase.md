# Handoff: camelcase (sub-issue #395)

## What was requested
Implement the process card for work order #381 (round 42 · batch B): create `camelcase.py` in the repository root with exactly two functions, plus `tests/test_camelcase.py` covering every acceptance point. Only these two code files may be added; no existing file may be modified; standard library only; no imports of `atbash` or `rot47`.

## What I did
- Created `camelcase.py`:
  - `snake_to_camel(s: str) -> str` — validates input with `re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", s)`, raising `ValueError` on empty string, leading/trailing/consecutive underscores, uppercase letters, or any other invalid content; keeps the first segment as-is, uppercases the first letter of each subsequent segment, and concatenates.
  - `camel_to_snake(s: str) -> str` — validates with `re.fullmatch(r"[A-Za-z0-9]+", s)`, raising `ValueError` on empty string or any underscore/non-alphanumeric character; inserts `_` before every uppercase letter except the first, then lowercases everything.
- Created `tests/test_camelcase.py` with one test per acceptance point (13 tests total):
  - snake→camel: `hello_world`→`helloWorld`, `hello_world_foo`→`helloWorldFoo`, `hello`→`hello`, `a_b_c`→`aBC`, `hello_` raises, `Hello_world` raises, `""` raises.
  - camel→snake: `helloWorld`→`hello_world`, `helloWorldFoo`→`hello_world_foo`, `HelloWorld`→`hello_world`, `hello`→`hello`, `hello_world` raises, `""` raises.

## What I did NOT do
- Did not touch `atbash.py`, `rot47.py`, `legacy_stringkit.py`, `roman.py`, `README.md`, `tests/test_legacy_stringkit.py`, `tests/test_roman.py`, or any other existing file (those belong to other process cards).
- Did not create `team/` paths other than my own two handoff/status files.
- Did not commit or push.
- Did not add round-trip or extra edge-case tests beyond the listed acceptance points (scope kept minimal).

## Checks run and results
- `python3 -m pytest tests/test_camelcase.py -q` → **13 passed**
- `python3 -m pytest tests/ -q` → **24 passed** (my 13 + 11 pre-existing tests in `tests/test_legacy_stringkit.py` and `tests/test_roman.py`)

Note: the environment initially lacked pytest (`No module named pytest`); I installed it with `python3 -m pip install --user --break-system-packages pytest` (pytest 9.2.0). No repository files were changed by that install.

## What the validator must pay attention to
- All 13 acceptance points have a dedicated test case; both checks pass as written above.
- Only `camelcase.py`, `tests/test_camelcase.py`, `team/handoffs/camelcase.md`, and `team/status/camelcase.json` were added by this process; no pre-existing file was modified.
- Implementation uses only the standard library (`re`) and does not import `atbash` or `rot47`.
