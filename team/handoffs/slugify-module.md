# Handoff: slugify-module

## What was requested

Implement `slugify.py` exposing `slugify(text)` that lowercases input, collapses each run of non-alphanumeric characters into a single `-`, and strips leading/trailing `-`. Provide `tests/test_slugify.py` covering the given examples (`"Hello, World!"` -> `"hello-world"`, `"  A  B  "` -> `"a-b"`), the empty-string edge case, and a run of consecutive separators. Standard library only; no sibling imports, no package directory, no CLI. Scope limited to `slugify.py` and `tests/test_slugify.py` plus the two team files.

## What I did

- Created `slugify.py` with a single `slugify(text)` function using `re.sub(r"[^a-z0-9]+", "-", text.lower())` followed by `.strip("-")`.
- Created `tests/test_slugify.py` with 4 pytest cases: the basic example, multi-space example, empty string, and consecutive separators (`foo---bar!!baz` -> `foo-bar-baz`, `a--b` -> `a-b`).

## What I did not do

- Did not touch `wordcount.py`, `textcase.py`, or any other test file.
- Did not add package directories, `__init__.py`, CLI entry points, or third-party dependencies.
- Did not commit or push anything.

## Checks run

- `python -m pytest tests/test_slugify.py -q` from the repository root: **4 passed** (had to install pytest first; it was not present in the environment: `python -m pytest` initially failed with "No module named pytest").

## Notes for the validator

- The environment lacked pytest; I installed it via `python3 -m pip install pytest` (pytest 9.2.0). This is an environment setup step, not a project dependency change.
- Test file imports `slugify` from the repository root, so pytest must be run from the repo root (as the acceptance criterion specifies: `python -m pytest -q`).
- `slugify` only depends on the standard-library `re` module.
