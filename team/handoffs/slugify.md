# Handoff: slugify (sub-issue #200)

## What was requested
Deliver the `slugify` text utility as one process card of work order #196:
- `slugify.py` in the repo root defining `slugify(text)`: lowercase the text; collapse runs of whitespace and underscores into a single hyphen; remove every character other than ASCII letters, digits, and hyphens; strip leading and trailing hyphens.
- `tests/test_slugify.py` testing only this module.
- Worked examples that must hold: `slugify("Hello World!") == "hello-world"` and `slugify("a_b  c") == "a-b-c"`.
- Constraints: Python standard library only; no package directory; no CLI; `slugify.py` must not import `registry`, `plugin_alpha`, or `plugin_beta`.
- Scope: this process owns only `slugify.py` and `tests/test_slugify.py` (plus these two team files). Stock files `registry.py` and `tests/test_registry.py` are not deliverables and must not be modified or deleted.

## What I did
- Created `slugify.py` with `slugify(text)` implemented via three `re.sub` steps (`[\s_]+` → `-`, strip `[^a-z0-9-]`, then `.strip("-")`), standard library only, no registry/plugin imports.
- Created `tests/test_slugify.py` with 8 tests covering both worked examples plus lowercase conversion, non-alphanumeric removal, hyphen stripping, whitespace-run collapsing, empty/symbol-only input, and a guard that the module exposes `slugify` and has no `registry` attribute.
- Installed `pytest` into the environment (it was absent; `python -m pytest` initially failed with "No module named pytest"), then ran the check command.

## What I did not do
- Did not create or touch `plugin_alpha.py`, `plugin_beta.py`, or their tests (owned by other processes).
- Did not modify or delete `registry.py` or `tests/test_registry.py`.
- Did not create a package directory, CLI, or any non-standard-library dependency.
- Did not commit or push anything.

## Checks run
- `python -m pytest -q tests/test_slugify.py` (via `python3 -m pytest` after installing pytest): **8 passed in 0.01s** (exit 0).
- Earlier attempt with bare `python -m pytest` failed only because pytest was not installed on that interpreter; after `python3 -m pip install pytest` the same check passes.

## What the validator must pay attention to
- Run the acceptance command in an environment where pytest is installed (e.g. `python3 -m pip install pytest` first); the check itself passes cleanly: `8 passed`.
- Both worked examples are asserted verbatim in `tests/test_slugify.py` (`test_hello_world_example`, `test_underscores_and_spaces_example`).
- `slugify.py` imports only `re` from the standard library and contains no reference to `registry`, `plugin_alpha`, or `plugin_beta`; the test file asserts `not hasattr(slugify_module, "registry")`.
- Stock files were left byte-for-byte untouched.
