# Handoff: implement-pqueue (sub-issue #255)

## What was requested
Process card `implement-pqueue` for work order #248 (round 33, crew system v2.6.5):
create `pqueue.py` implementing the min-priority queue class `PriorityQueue`, plus
`tests/test_pqueue.py`. Scope owned: only `pqueue.py` and `tests/test_pqueue.py`.

Specification:
- `PriorityQueue`: min-priority queue; smaller numeric priority dequeues first.
- `push(item, priority)` enqueues.
- `pop()` removes and returns the smallest-priority element; ties broken by enqueue
  order (FIFO). `peek()` returns the same next element without removing it.
- `pop()` / `peek()` on an empty queue raise `IndexError`.
- `__len__` returns element count; `is_empty()` returns whether the queue is empty.
- Items themselves need not be comparable.
- Worked example: push("a",2), push("b",1), push("c",1) → peek() == "b", len == 3;
  three pops give "b", "c", "a"; afterwards is_empty() is True.
- Constraints: stdlib only; no imports of lrucache/dllist; no package dirs; no CLI;
  tests cover only PriorityQueue behavior.

## What I did
- Created `pqueue.py` with class `PriorityQueue` backed by `heapq`. Each heap entry is
  `(priority, seq, item)` where `seq` is a monotonically increasing counter, giving
  FIFO tie-breaking without requiring items to be comparable. Exposes `push`, `pop`,
  `peek`, `__len__`, `is_empty`. Empty `pop()`/`peek()` raise `IndexError`.
- Created `tests/test_pqueue.py` with 11 tests covering: the worked example, min-priority
  ordering, FIFO tie-breaking (pure ties and mixed priorities), peek without removal,
  `IndexError` on empty `pop()`/`peek()`, `__len__`/`is_empty`, non-comparable items
  (dict/list/tuple), negative/float priorities, and `None` as an item.

## What I did not do
- Did not create or modify `lrucache.py`, `dllist.py`, or any other process's files.
- Did not create package directories or a CLI.
- Did not commit or push (workflow handles that).

## Checks ran and results
- `python -m pytest -q tests/test_pqueue.py` → initially failed because pytest was not
  installed in the environment (`No module named pytest`); installed pytest, then reran:
  **11 passed in 0.03s** (exit code 0).

## Notes for the validator
- The only check command is exactly `python -m pytest -q tests/test_pqueue.py`; it passes
  fully once pytest is available (installed into the environment for this run).
- Tie-breaking relies on the sequence counter in the heap tuple, so equal priorities
  dequeue in push order and items are never compared directly.
