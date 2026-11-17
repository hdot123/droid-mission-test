# Handoff: fence-module (sub-issue #28)

## What was requested
Process card `fence-module` for work order #24: implement only the fence tool module plus its tests.

- `fence.py` in the repo root, exposing two public functions:
  - `wrap(text, width)`: greedy word wrap. Words are never split; a word longer than `width` goes on its own line untruncated (may exceed `width`). Output words separated by single spaces; input whitespace runs are word separators.
  - `unwrap(text)`: collapse wrapped text to one line by joining lines with single spaces. Trailing hyphens at line ends are preserved as-is (never removed; next word still joined with a single space). Blank lines/whitespace normalized to single spaces.
  - GLOBAL RULE: every public function raises `TypeError` when any argument is `None` (`wrap(None, 10)`, `wrap('a', None)`, `unwrap(None)`).
  - `width <= 0` raises `ValueError`.
- `tests/test_fence.py` covering: wrap within width, long word on its own line, unwrap round-trip, hyphen-at-line-end preservation, blank-line normalization, `ValueError` on non-positive width, `TypeError` on `None` for every argument of both functions.
- Constraints: Python standard library only; no cross-module imports; no CLI; no package directory; tests test only `fence.py`.

## What I did
- Created `fence.py` (root) with `wrap` and `unwrap` as specified. Both functions check arguments in the order `text is None` then `width is None` (TypeError), then `width <= 0` (ValueError) for `wrap`.
- `wrap` uses `str.split()` so all whitespace runs (spaces, tabs, newlines) collapse to word separators; empty/whitespace-only input returns `""`.
- `unwrap` is `" ".join(text.split())`, which joins lines with single spaces, normalizes blank lines, and keeps any trailing hyphen token (e.g. `"well-"`) intact.
- Created `tests/test_fence.py` with 15 tests (parametrized on `width`), covering every behavior named in the card.

## What I did not do
- Did not touch `isbn.py`, `duration.py`, or their tests.
- Did not modify any other repo file (no README, no other team files besides my two required ones).
- Did not commit or push.
- Did not add CLI, package directory, or non-standard-library dependencies.

## Checks ran and results
- `python -m pytest -q tests/test_fence.py` → **15 passed in 0.02s** (exit 0).
- Note: `pytest` was not preinstalled in this environment (`No module named pytest`); I installed it with `python -m pip install pytest` to run the required check. No repo files were changed by that install.

## What the validator must pay attention to
- `unwrap` keeps a trailing hyphen exactly as-is and still inserts a space: `"a well-\nknown fact"` → `"a well- known fact"`. If the spec had intended hyphen re-joining, this would differ — the card says "kept as-is, not removed or joined", which is what is implemented.
- `wrap` returns `""` for empty or whitespace-only input (no exception).
- `wrap` with a single word longer than `width` returns that word alone on one line exceeding `width`, per spec.
- `TypeError` is raised for `None` before any `ValueError` width check (so `wrap(None, 0)` raises `TypeError`).
- `pytest` had to be pip-installed in the environment; a validator running the check in a fresh environment may need to install it first.
