# Handoff: sllist (sub-issue #823)

## What was requested

Work order #815 第54轮并发D单, process card `sllist`: implement a single linked list component as exactly two new files — `sllist.py` (repo root) and `tests/test_sllist.py` — with the `SinglyLinkedList` class semantics pinned by the card (constructor from iterable, `__len__`, `to_list`, `append`, `prepend`, `get`, `find`, `remove`, `remove_at`, `reverse`, `clear`; `bool` rejected as index → `TypeError`; out-of-range index → `IndexError`; equality via `==`). Standard library only; no import of `daycount360` or `harmonic`. One test case per acceptance item. Plus this handoff and `team/status/sllist.json`.

## What I did

- Created `sllist.py`: `SinglyLinkedList` over a `_Node` structure with head/tail pointers and size counter. Index validation shared via `_validate_index` (rejects `bool` and non-`int` with `TypeError`, out-of-range with `IndexError`), used identically by `get` and `remove_at`. `remove`/`remove_at` maintain the tail correctly (including head removal on a one-element list); `reverse` is in-place and fixes the tail.
- Created `tests/test_sllist.py`: 15 test cases covering every acceptance item on the card (14 bullets; the IndexError and TypeError bullets are covered by two tests each — `get`/`remove_at` IndexError, `get` float/`bool` TypeError).
- Installed `pytest` from `requirements-dev.txt` (it was missing in this environment) to run the checks.

## What I did NOT do

- Did not create `daycount360.py`, `harmonic.py`, or their tests (other process cards own those).
- Did not modify, delete, or move any pre-existing repository file.
- Did not commit or push; did not touch `team/` files owned by other processes.
- No cross-module imports; standard library only.

## Checks run and results

- `python3 -m pytest tests/test_sllist.py -q` → **15 passed** in 0.03s.
- `python3 -m pytest tests/ -q` → **202 passed, 2 skipped** in 16.50s (repo-wide suite green; the 2 skips are pre-existing pipeline skips, not from this card).

No `verdict.json` / `verdict.md` byproducts appeared; repo checked clean of them.

## What the validator must pay attention to

- Acceptance sequence in the card builds one list stepwise: `[1,2,3]` → append(4) → prepend(0) → find/remove/remove_at/reverse/clear. The tests mirror that sequence per bullet rather than as one chained mega-test, so each bullet is independently asserted.
- `remove(99) is False` test also asserts the list is unchanged (card: "表不变").
- `get(True)` and `get(1.0)` both raise `TypeError` (bool explicitly rejected before the int check).
- `reverse()` returns `None` (in-place); the test only checks `to_list()` afterward, per card ("不返回新表").
