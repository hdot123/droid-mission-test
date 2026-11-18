# Handoff: implement-dllist (sub-issue #252)

## What was requested
Implement the `DoublyLinkedList` class in `dllist.py` plus `tests/test_dllist.py`, per the process card "implement-dllist" under work order #248 (round 33, group D, foreman v2.6.5).

Behavior required:
- Elements compared by value equality (`==`).
- `append(value)` tail insert; `prepend(value)` head insert.
- `__len__` returns element count.
- `to_list()` head-to-tail values; `to_list_reversed()` tail-to-head values.
- `remove_first(value)` deletes the first element equal to value, returns `True` on success, `False` if absent.
- `pop_front()` / `pop_back()` remove and return head/tail; raise `IndexError` when empty.
- Worked example must hold: `append(1), append(2), append(3), prepend(0)` → `to_list() == [0,1,2,3]`, `to_list_reversed() == [3,2,1,0]`, `len == 4`; `remove_first(2) is True` → `[0,1,3]`; `remove_first(9) is False`; `pop_back() == 3`, `pop_front() == 0`, `to_list() == [1]`.

Constraints: stdlib only, no imports of `lrucache`/`pqueue`, no package dirs, no CLI, tests cover only `DoublyLinkedList`.

## What I did
- Created `dllist.py` with `DoublyLinkedList` (doubly linked nodes with `prev`/`next`, explicit head/tail/size tracking). All operations are O(n) at worst; `remove_first` scans from the head so duplicates remove the earliest occurrence, per spec.
- Created `tests/test_dllist.py` with 11 tests covering: append order, prepend order, `__len__`, `to_list` / `to_list_reversed`, `remove_first` success (True) and absent (False), duplicate removal (earliest first), `pop_front` / `pop_back` return values, `IndexError` on empty `pop_front` and empty `pop_back`, the full worked example sequence, empty-list basics, and a single-element list.

## What I did NOT do
- Did not touch `lrucache.py`, `pqueue.py`, or any other process's files (those belong to sibling cards).
- Did not add package directories, CLI entry points, or any imports beyond `pytest` in the test file (module itself imports nothing).
- Did not commit or push; the workflow does that.

## Checks run and results
- Command: `python -m pytest -q tests/test_dllist.py`
- Result: **PASS** — `11 passed in 0.03s` (exit code 0).
- Note: the base environment had no pytest (`python -m pytest` failed with "No module named pytest"). I installed `pytest 9.2.0` via `pip install pytest` as test tooling so the acceptance check could run. This affects only the test runner, not the delivered modules (stdlib only).

## What the validator must pay attention to
- Both owned files exist: `dllist.py` and `tests/test_dllist.py`.
- The exact acceptance command is `python -m pytest -q tests/test_dllist.py`; on a fresh env without pytest, install pytest first (the module code needs nothing beyond stdlib).
- Signatures match the spec exactly: `append`, `prepend`, `__len__`, `to_list`, `to_list_reversed`, `remove_first`, `pop_front`, `pop_back`.
- `remove_first` returns a strict `True`/`False` (not truthy/falsy objects), and removes only the first match.
- Empty-list `pop_front()` / `pop_back()` raise `IndexError`, not `KeyError` or `StopIteration`.
- No cross-module imports: `dllist.py` imports nothing; `tests/test_dllist.py` imports only `pytest` and `dllist`.
