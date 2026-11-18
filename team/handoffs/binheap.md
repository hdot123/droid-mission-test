# Handoff: binheap (sub-issue #447, work order #433 round 44-D)

## What was requested

Implement a binary min-heap from scratch in `binheap.py` plus `tests/test_binheap.py`, as one
of three independent components of round 44 · D. Scope was strictly limited to those two files.

Spec (per the process card):

- `class BinHeap` with `push(x)`, `pop() -> smallest`, `peek() -> smallest without removing`,
  `__len__`, `is_empty() -> bool`.
- `push` accepts only numeric values (bool excluded); anything else (e.g. `"a"`) raises
  `TypeError`. Duplicates allowed.
- `pop()`/`peek()` on an empty heap raise `IndexError`.
- Acceptance sequence: push 5, 3, 8, 1, 9, 2 → `len == 6`; `peek() == 1`; `pop() == 1`;
  next `peek() == 2`; pops then yield 2, 3, 5, 8; final `pop() == 9`; `is_empty() == True`;
  empty-heap `pop()`/`peek()` raise `IndexError`. Also: push 4, 4, 4 → three pops of 4;
  `push("a")` raises `TypeError`.
- Standard library only; must NOT import `heapq`; must not import the other round-44 modules
  (`polygonarea`, `ordinal`).

## What I did

- Created `binheap.py`: a from-scratch array-backed binary min-heap (sift-up on push, sift-down
  on pop). No third-party imports at all — not even `heapq`; the module imports nothing.
  Numeric check is `isinstance(value, (int, float)) and not isinstance(value, bool)`, so `bool`
  (a subclass of `int`) is rejected with `TypeError`, as are strings, `None`, lists, tuples,
  dicts.
- Created `tests/test_binheap.py` with 16 test cases covering every acceptance point in the card
  plus extras (bool rejection, other non-numeric types, negative/float values, peek not removing,
  `len` tracking, a seeded 50-element random insert/drain-vs-sorted check).

## What I did not do

- Did not touch any pre-existing file: `legacy_stringkit.py`, `roman.py`, `README.md`,
  `tests/test_roman.py`, `tests/test_legacy_stringkit.py`, `worker-prompt.txt`,
  `worker-stream.jsonl` are all untouched (verified via `git status`).
- Did not create `polygonarea.py`, `ordinal.py`, or their tests — those belong to other process
  cards.
- Did not commit or push (workflow does that).

## Checks run

1. `python3 -m pytest tests/test_binheap.py -q` → **16 passed** (exit 0)
2. `python3 -m pytest tests/ -q` → **27 passed** (exit 0)

Note: the environment had no `pytest` module initially (`python3 -m pytest` → "No module named
pytest"), so I installed pytest 9.2.0 with `python3 -m pip install --break-system-packages pytest`.
This only affects the Python environment, not repository files.

## What the validator should pay attention to

- Both required checks pass as written; the full-suite run (27) includes this card's 16 tests
  plus the 11 pre-existing tests.
- `bool` rejection is deliberate per spec ("bool 除外"): `push(True)`/`push(False)` raise
  `TypeError` even though `bool` is an `int` subclass.
- `is_empty()` returns a real `bool` (`not self._items`), and `heap.is_empty() is True` is
  asserted in tests.
- Empty-heap errors are `IndexError` (not `KeyError`) for both `pop()` and `peek()`.
- Duplicate values are fully supported; equality ties do not break the sift logic (the sift
  stops on `>=`, which is stable enough for a min-heap).
- Only two files were added: `binheap.py` and `tests/test_binheap.py`.
