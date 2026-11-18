# Handoff: plugin-alpha

## What was requested
Sub-issue #198: deliver `plugin_alpha.py` and `tests/test_plugin_alpha.py` only.
- `plugin_alpha.py` must register a handler named `alpha` into the stock `registry` at import time; the handler uppercases its text argument.
- Acceptance: (1) after importing `plugin_alpha`, `registry.names() == ["alpha"]` exactly — test must arrange isolation itself (e.g. `registry.clear()` then `importlib.reload(plugin_alpha)`); (2) `registry.get("alpha")("abc") == "ABC"`; (3) `python -m pytest -q tests/test_plugin_alpha.py` passes; (4) both files exist and match spec; (5) stock files `registry.py` and `tests/test_registry.py` must not be modified or deleted.
- Constraints: Python stdlib only, no package directory, no CLI; `plugin_alpha` may depend only on the stock `registry` (must not import `plugin_beta` or `slugify`); test file tests only its own module.

## What I did
- Created `plugin_alpha.py`: imports `registry`, defines `_upper(text)` returning `text.upper()`, and calls `registry.register("alpha", _upper)` at module level (import time).
- Created `tests/test_plugin_alpha.py` with two tests, each isolating state via `registry.clear()` then `importlib.reload(plugin_alpha)`:
  - `test_alpha_is_only_handler_after_import`: asserts `registry.names() == ["alpha"]`.
  - `test_alpha_uppercases_text`: asserts `registry.get("alpha")("abc") == "ABC"`.

## What I did not do
- Did not touch `registry.py`, `tests/test_registry.py` (verified unmodified via `git status` / `git diff --stat` — no diff on either).
- Did not create or edit `plugin_beta.py`, `slugify.py`, or any `team/` files other than this handoff and `team/status/plugin-alpha.json`.
- Did not commit or push.

## Checks ran and results
- `python -m pytest -q tests/test_plugin_alpha.py` → `2 passed in 0.01s` (exit 0). Note: pytest was not preinstalled in this environment; I installed it with `pip install --user pytest` to run the check. The acceptance command itself is the one transcribed from the card and passes.
- `git status --short` / `git diff --stat -- registry.py tests/test_registry.py` → stock files show no changes; only new untracked files `plugin_alpha.py` and `tests/test_plugin_alpha.py` (plus `__pycache__/` byproducts and pre-existing untracked `worker-*` files).

## Validator notes
- The isolation pattern matters: the test clears the registry and reloads `plugin_alpha` before asserting `names() == ["alpha"]`, so it passes regardless of test ordering or other suites having registered handlers first.
- Reload works because `plugin_alpha` re-executes `registry.register("alpha", _upper)` on each import; duplicate registration of the same name is a no-op overwrite per the stock registry's contract.
- `registry.names()` returns a sorted list, so the exact-match assertion `== ["alpha"]` is order-stable.
