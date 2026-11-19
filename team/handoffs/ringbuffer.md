# Handoff: ringbuffer (sub-issue #496, process card "ringbuffer")

## What was requested

Create exactly two deliverable files for the fixed-capacity ring buffer (work order #481, 第 46 轮 D):

- `ringbuffer.py` — `RingBuffer(capacity: int)` with:
  - `capacity <= 0` raises `ValueError`; non-int capacity (e.g. `2.5`, `"3"`) raises `TypeError`.
  - `append(item) -> None`: writes at the tail when not full; overwrites the oldest item when full (FIFO overwrite).
  - `__len__() -> int` (always ≤ capacity), `is_empty() -> bool`, `is_full() -> bool`.
  - `to_list() -> list` and `__iter__`: both oldest-to-newest.
- `tests/test_ringbuffer.py` — one test case per acceptance criterion from the process card.

Plus the two team files: `team/handoffs/ringbuffer.md` (this file) and `team/status/ringbuffer.json`.

## What I did

- Implemented `RingBuffer` in `ringbuffer.py` using a fixed-size list with a start index and size counter; stdlib only, no imports from other deliverables.
- Constructor rejects `bool`/non-int capacity with `TypeError` and non-positive int capacity with `ValueError` (bool check first, so `RingBuffer(True)` would be TypeError; the card only requires `2.5` and `"3"` → TypeError, `0`/`-2` → ValueError).
- Wrote `tests/test_ringbuffer.py` covering every acceptance criterion: fresh-empty state, fill-to-capacity state, single overwrite, repeated overwrite, iteration order, capacity=1 overwrite, storing `None`, `RingBuffer(0)`/`RingBuffer(-2)` → `ValueError`, `RingBuffer(2.5)`/`RingBuffer("3")` → `TypeError`. All 11 cases pass.

## What I did not do

- Did not touch `pressureconv.py`, `century.py`, or any other process's files.
- Did not modify any pre-existing file (only the six new files owned by this card's deliverables plus the two team files were created; no existing repo file was edited).
- Did not commit or push.
- Did not add a `capacity` property requirement (added as a convenience only; not required by the card, harmless).

## Checks run and results

Environment note: `pytest` was not installed in this environment; I installed it with `python3 -m pip install --user pytest` (pytest 9.2.0) so the mandated checks could run. This does not change any repo file.

1. `python3 -m pytest tests/test_ringbuffer.py -q` → **11 passed in 0.02s**
2. `python3 -m pytest tests/ -q` → **22 passed in 0.02s** (11 ringbuffer + 11 pre-existing legacy_stringkit/roman tests)

## Validator notes

- Every acceptance criterion in the process card has a dedicated test in `tests/test_ringbuffer.py`; grep for the test names above if re-verifying.
- `to_list()` and `__iter__` both return oldest-to-newest; after wrap-around (`append(4/5/6)` on capacity 3) the order is `[4, 5, 6]`.
- `None` is a legal element; emptiness is tracked by size, not by sentinel values.
- Full suite is green; no existing files were modified.
