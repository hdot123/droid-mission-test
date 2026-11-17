# Handoff: flatten-module

## What was requested (process card #137, sub-issue of work order #133)

Implement `flatten.py` exposing `flatten(nested)` that flattens arbitrarily nested
lists into a one-dimensional list, preserving element order; non-list elements are
kept as-is; an empty list returns an empty list. Example:
`flatten([1, [2, [3, 4]], 5]) -> [1, 2, 3, 4, 5]`. Constraints: Python standard
library only; must not import `anagram` or `gcdx`; no package directories; no CLI.
Scope: only `flatten.py` and `tests/test_flatten.py`.

## What I did

- Created `flatten.py` with a single recursive `flatten(nested)` function. It walks
  the input, recursing into `list` items via `isinstance(item, list)` and appending
  everything else unchanged, preserving order.
- Created `tests/test_flatten.py` with 4 tests covering only flatten behavior:
  - the worked example from the spec,
  - empty list -> `[]`,
  - non-list elements preserved (int, str, float, None, bool),
  - deep nesting with order preservation (5 levels deep, plus a mixed
    strings/empties case).
- Installed `pytest` into the environment (`pip3 install pytest`, version 9.2.0)
  because it was not present; no repository files were changed for this.
- Ran the card's check command verbatim: `python -m pytest -q tests/test_flatten.py`
  from the repository root. Result: `4 passed in 0.01s`, exit code 0.

## What I did NOT do

- Did not touch `anagram.py`, `gcdx.py`, `tests/test_anagram.py`,
  `tests/test_gcdx.py`, `team/**` (other than my two handoff/status files), or
  `.github/**`.
- Did not create package directories, a CLI, or any import of other modules.
- Did not commit or push anything.
- Did not run `python -m pytest -q` on the whole repository: at the time of my run
  only my own test file existed, and the full-suite check is owned by the work
  order's acceptance step, not by this process card. The single check listed on my
  card is `python -m pytest -q tests/test_flatten.py`, which passed.

## Checks I ran and results

| Command | Result |
| --- | --- |
| `python -m pytest -q tests/test_flatten.py` | pass — `4 passed in 0.01s` (exit 0) |
| `python3 -c "import pytest; ..."` (after install) | pass — `pytest 9.2.0` |

Note: the very first attempt at the check failed with
`/usr/bin/python: No module named pytest` because pytest was not installed in the
environment. I installed it and re-ran the exact command; the failure was an
environment gap, not a code failure.

## What the validator must pay attention to

1. The card's check command, `python -m pytest -q tests/test_flatten.py`, passes
   with 4 tests, exit code 0. This is the only check on my card.
2. `flatten` signature is `flatten(nested)` exactly as specified; behavior matches
   the spec and the worked example (verified by `test_worked_example`).
3. `flatten.py` and `tests/test_flatten.py` are the only code files I created;
   the two team files (`team/handoffs/flatten-module.md`,
   `team/status/flatten-module.json`) are this process's required reporting files.
4. `flatten` treats any `isinstance(item, list)` as nestable, including `[]`
   (which contributes nothing), so `flatten([[], 1]) -> [1]` and
   `flatten([[]]) -> []` hold.
5. Full-repo `python -m pytest -q` must be run once the sibling modules
   (`anagram.py`, `gcdx.py` and their tests) land; my module does not depend on
   them and they do not depend on mine.
