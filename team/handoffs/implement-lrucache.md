# Handoff: implement-lrucache (sub-issue #250)

## What was requested
Implement `lrucache.py` with a fixed-capacity `LRUCache` class plus `tests/test_lrucache.py`, per process card `implement-lrucache` (work order #248, round 33 group D).

Spec requirements:
- `LRUCache(capacity)`: capacity must be a positive integer, else `ValueError`.
- `get(key, default=None)`: hit returns value and refreshes key to most recently used; miss returns default with no order change.
- `put(key, value)`: insert or update (update refreshes); after writing, evict least recently used if over capacity.
- `__len__`: element count. `__contains__`: existence only, no order refresh.
- `keys_oldest_first()`: keys from least to most recently used.
- Stdlib only; no imports of dllist/pqueue; no package dirs; no CLI.
- Worked example from the card must hold exactly.

## What I did
- Created `lrucache.py`: `LRUCache` backed by `collections.OrderedDict` (oldest-first insertion order). Capacity validation rejects `0`, negatives, non-int (including `bool`, `str`, `float`, `None`) with `ValueError`. `get` uses pop/re-insert to refresh; `put` uses the same pattern and `popitem(last=False)` for LRU eviction; `__contains__` is a plain membership test that does not reorder.
- Created `tests/test_lrucache.py` with 12 tests covering: capacity validation (reject and accept), get hit/miss (with and without default) and no-order-change on miss, put insert/update refresh, eviction of least recently used (both plain and after a `get` refresh), `put` of an existing key not evicting, `__len__`, `__contains__` without order refresh, `keys_oldest_first`, and the card's worked example verbatim.
- Wrote `team/handoffs/implement-lrucache.md` and `team/status/implement-lrucache.json`.

## What I did not do
- Did not create or modify `dllist.py`, `pqueue.py`, `tests/test_dllist.py`, `tests/test_pqueue.py`, or any file outside my scope plus the two required team files.
- Did not commit or push (workflow handles that).
- Did not add CLI, package directories, or non-stdlib imports.

## Checks run and results
- `python -m pytest -q tests/test_lrucache.py` → **12 passed in 0.02s** (exit 0).
- Note: the environment's `python` initially had no pytest (`No module named pytest`); I installed `pytest 9.2.0` via `pip install pytest` so the exact card check command could run. The first run had 2 failures, both caused by wrong expectations in my own tests (I forgot `put("c")` evicts `"a"` when no `get` refresh occurred); I corrected the tests to match the spec semantics and reran to green. The `LRUCache` implementation itself needed no changes.

## Notes for the validator
- The spec's worked example (`get("a")` before `put("c")`) is what makes `keys_oldest_first()` return `["a", "c"]`; without that refresh the evicted key is `"a"`, not `"b"`. Both cases are covered by tests.
- `capacity` validation deliberately rejects `bool` (`LRUCache(True)` raises `ValueError`) since `bool` is a subclass of `int`; this is the stricter reading of "positive integer" and is asserted in tests.
- `LRUCache.capacity` is exposed as a read-only property (extra, harmless; not required by spec).
