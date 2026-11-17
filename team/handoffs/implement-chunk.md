# Handoff: implement-chunk (sub-issue #45)

## What was requested
Execute process card `implement-chunk` from work order #42 (foreman v2.6.1 rerun round):
implement the `chunk` module only, with these requirements:

- `chunk.py` (repo root, Python standard library only):
  - `chunk(items, size)` splits a list into sublists of at most `size` elements each,
    preserving order. Example: `chunk([1, 2, 3, 4, 5], 2)` → `[[1, 2], [3, 4], [5]]`.
    Raises `ValueError` when `size <= 0`; empty list returns `[]`.
  - `flatten(chunks)` concatenates a sequence of sublists in order into a single
    one-dimensional list. Example: `flatten([[1, 2], [3], []])` → `[1, 2, 3]`.
- `tests/test_chunk.py` covering exactly this module's behavior:
  both spec examples, `size <= 0` raising `ValueError`, empty input list returning `[]`,
  chunks of size 1 and size larger than the list, `flatten` ignoring empty sublists,
  and `flatten(chunk(xs, n))` round-tripping to `xs` for several inputs.
- No imports of other project modules, no CLI, no package directory.

## What I did
- Created `chunk.py` with `chunk(items, size)` (validates `size <= 0` → `ValueError`,
  slices via `range(0, len(items), size)`) and `flatten(chunks)` (extends a fresh list
  in order). No imports at all.
- Created `tests/test_chunk.py` with 10 test functions (14 collected cases via
  parametrization of the round-trip test): both spec examples, `size == 0` and
  negative size raising `ValueError`, empty list → `[]`, size 1, size larger than
  the list, flatten ignoring empty sublists, flatten of empty input, and five
  parametrized round-trip cases (`flatten(chunk(xs, n)) == xs`).

## What I did NOT do
- Did not touch `vigenere.py`, `anagram.py`, or their test files (owned by other processes).
- Did not touch `README.md`, `worker-prompt.txt`, `worker-stream.jsonl`, `.github/`, or any
  other repo file.
- Did not run the full `python -m pytest -q` suite (other processes' files are out of scope
  for this card; the foreman/validator runs the full suite).
- Did not commit or push anything.
- Note: `pytest` was not installed in the environment, so I installed it with
  `python3 -m pip install pytest` (pytest 9.2.0) to run the checks. No repo files
  were changed by that install.

## Checks run and results

1. `python -m pytest tests/test_chunk.py -q` → **PASS**: `14 passed in 0.02s`
2. `python -c "import chunk; assert chunk.chunk([1,2,3,4,5],2)==[[1,2],[3,4],[5]]; assert chunk.flatten([[1,2],[3],[]])==[1,2,3]; import pytest; pytest.raises(ValueError, chunk.chunk, [1], 0)"` → **PASS** (exit 0)

## What the validator must pay attention to
- Both checks are green as written in the process card; `chunk.py` and
  `tests/test_chunk.py` are the only files this process created/edited.
- `chunk` raises `ValueError` before touching `items`, so `chunk([], 0)` also raises
  (size check first) — this is intentional and consistent with the spec ("size <= 0 抛 ValueError").
- The test file imports `pytest` and `chunk` only; it does not import or exercise
  `vigenere` or `anagram`, satisfying the "each test file only tests its own module" constraint.
- `python -m pytest -q` at repo root depends on the other processes' files; that full-suite
  run is the foreman's gate, not part of this card.
