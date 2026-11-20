# Handoff: hashtable (sub-issue #736)

## What was requested

Process card #736 under work order #728 (第五十轮 B 同题复验): create exactly two new files —

- `hashtable.py` — open-addressing hash table: keys must be `str` (non-str raises `TypeError`), hash pinned to djb2 32-bit over UTF-8 bytes (init 5381, `h = (h*33 + byte) mod 2^32`, builtin `hash()` forbidden), home slot `h mod capacity`, linear probing (step 1, wrap). `HashTable()` starts at capacity 8 / size 0; `capacity` property; `__len__` counts live keys. `put` probes to empty slot or same key recording the first tombstone, updates in place (size unchanged) or inserts at first tombstone else empty (size +1), then doubles capacity and rehashes live items in old-slot ascending order when `size*10 > capacity*7` (tombstones discarded). `get` skips tombstones and raises `KeyError` on empty slot; `delete` sets a tombstone (size -1) or raises `KeyError`; `__contains__` returns False for non-str, else get semantics; `probe_sequence(key)` returns indices from home slot up to and including the match or first empty slot (tombstones skipped but counted).
- `tests/test_hashtable.py` — one test case per acceptance item, including the pinned anchors: `djb2("a") == 177670`, home slot 6, probe sequences `[6]`, `[6, 7]`, `[6, 7, 0]`, tombstone skip/reuse behavior, growth to capacity 16 at 6 keys and capacity 32 / len 12 at 12 keys.

No edits to any existing file; standard library only; no cross-module imports.

## What I did

- Implemented `hashtable.py` with a module-level `djb2(key)` helper (used by `home slot` computation) plus the `HashTable` class. Markers are module-level singleton sentinels (`_EMPTY`, `_TOMBSTONE`); entries are `(key, value)` tuples.
- `put` walks the probe chain once, recording the first tombstone, stopping at empty or same key; insertion prefers the recorded tombstone. Growth triggers only after a new-key insertion, doubling capacity and re-inserting live entries in old-table slot order (which equals old-slot ascending since the old table is walked linearly), discarding tombstones.
- `probe_sequence` walks the same chain appending every visited index and stops at match or empty (tombstones appended then skipped over).
- Wrote `tests/test_hashtable.py` with 11 tests covering every acceptance bullet: djb2 anchor, fresh table, two-key probe sequences + get/contains, in-place update, delete→KeyError + tombstone-skipping probe `[6, 7]`, tombstone reuse at slot 6, `delete("missing")` KeyError, `put(1,"x")`/`get(None)` TypeError, non-str `__contains__` is False, growth to 16 at 6 keys with all keys gettable, growth to 32 at 12 keys with len 12 and all keys gettable.

## What I did not do

- Did not touch `eliasgamma.py`, `truncate.py`, or any existing repository file.
- Did not modify any file owned by other processes; did not commit or push.
- Did not implement serialization, iteration, `keys()`/`values()`, or any feature beyond the card.

## Checks run

- `python3 -m pytest tests/test_hashtable.py -q` → **11 passed in 0.02s**
- `python3 -m pytest tests/ -q` → **114 passed in 3.20s**

(pytest was not preinstalled; installed `pytest` 9.2.0 via pip to run the checks.)

## Notes for the validator

- The growth threshold uses strict `size*10 > capacity*7` (load > 0.7): 6 keys in capacity 8 triggers the doubling to 16 (60 > 56), so "after inserting 6 distinct keys `capacity == 16`" holds; 12 keys triggers 16 → 32 (120 > 112), so `capacity == 32`, `len == 12` holds.
- `djb2` is exposed at module level for direct testing of the pinned constant; it is the sole hashing path (no builtin `hash()`).
- Probe sequences count tombstones as visited slots but never stop on them, matching `probe_sequence("i") == [6, 7]` after `delete("a")`.
- All keys used in tests are ASCII so UTF-8 encoding is identity; djb2("a") = 177670 was verified numerically before writing tests.
