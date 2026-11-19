# Handoff: hashtable (sub-issue #667)

## What was requested

Implement one of the three independent deliverables of work order #662 第四十八轮 B 单 (foreman pattern, v2.7.0):

- `hashtable.py` — open-addressing hash table with linear probing, tombstones, and growth.
- `tests/test_hashtable.py` — a test case for every acceptance point in the spec.

Scope: only these two files. Standard library only, no imports from other project modules, no changes to any existing file. Key points of the spec:

- Keys must be `str`; non-str raises `TypeError` (`__contains__` returns `False` for non-str).
- Hash pinned to djb2 32-bit (init 5381, `h = (h*33 + byte) mod 2**32` over UTF-8 bytes, builtin `hash()` forbidden); home slot = `h mod capacity`; linear probing with step 1 and wraparound.
- `HashTable()`: capacity 8, size 0; `capacity` property; `__len__` = live keys.
- `put` probes to empty slot or matching key, recording the first tombstone; update on same key (size unchanged); new key goes into first tombstone if any else the first empty slot; after a new insert, if `size*10 > capacity*7` then double capacity and rehash all live items in ascending old-slot order (tombstones dropped).
- `get` returns value, raises `KeyError` at an empty slot (skipping tombstones); `delete` tombstones and decrements size, `KeyError` if absent.
- `probe_sequence(key)`: slots from home up to and including the matching key or the first empty slot (tombstones are included in the sequence but do not stop the search).
- Acceptance values: djb2("a") = 177670, home slot 6, plus all listed probe sequences, error cases, and growth boundaries (6 keys → capacity 16, 12 keys → capacity 32 with len 12).

## What I did

- Created `hashtable.py`:
  - Module-level `djb2(key)` helper (pinned 32-bit hash over UTF-8 bytes) and a private `_TOMBSTONE` sentinel object.
  - `HashTable` with `capacity`, `size`, `put`, `get`, `delete`, `__contains__`, `__len__`, `probe_sequence`.
  - Growth implemented as `_rehash(new_capacity)`: live items collected in ascending old slot order and reinserted (tombstones dropped), then capacity updated.
  - Probing logic shared across `put`/`get`/`delete`/`probe_sequence`: stop at first empty slot (None) or matching key; tombstones are skipped for lookup but recorded as the first insertion candidate in `put`. `put` records the first tombstone seen during its probe and inserts there for new keys.
- Created `tests/test_hashtable.py` with 11 tests covering every acceptance point: pinned djb2 value and home slot, initial capacity/len/probe, all three probe sequences after two puts, membership, update-keeps-size, delete + tombstone-skipping probe, tombstone reuse on reinsert, `delete("missing")` KeyError, TypeError for `put(1, ...)`/`get(None)`, `__contains__` with non-str returning False, resize to 16 after 6 keys with all 6 readable, and resize to 32 at 12 keys with len == 12 and all readable.

## What I did not do

- Did not create or touch `eliasgamma.py`, `truncate.py`, their tests, or any pre-existing file (including `team/` files owned by other processes).
- Did not import from any other project module; only `pytest` in the test file (matching the existing `tests/test_roman.py` convention of importing root-level modules directly, which works because `python3 -m pytest` puts the repo root on `sys.path`).
- Did not commit or push.
- No `hash()` builtin use anywhere; hashing is the pinned djb2 only.

## Checks run and results

Environment note: system `python3` had no pytest; installed `pytest` (9.2.0) via pip (declared in `requirements-dev.txt`) to run the mandated checks. No repository files were changed by this.

- `python3 -m pytest tests/test_hashtable.py -q` → **11 passed** (exit 0)
- `python3 -m pytest tests/ -q` → **47 passed** (exit 0), covering the full existing suite plus my new tests

## For the validator

- Verify the two new files only: `hashtable.py` and `tests/test_hashtable.py` (plus this handoff and `team/status/hashtable.json`), with zero diffs to pre-existing files.
- Watch the djb2 pinning: `djb2("a") == 177670`, home slot 6 at capacity 8; the hash must be computed over UTF-8 bytes, not `hash()`.
- Watch probe-sequence semantics: tombstones count as steps in the returned sequence but do not terminate it; an empty slot (None) terminates it and is included.
- Watch `put`'s tombstone-first insertion: after `delete("a")`, a later `put("a", 9)` must reuse slot 6 (first tombstone on the probe path), not the empty slot beyond.
- Watch growth: threshold is strictly `size*10 > capacity*7` evaluated after a new-key insert (updates do not trigger growth), doubling capacity and rehashing live items in ascending old slot order.
- Acceptance-derived expectations used in tests: 6 distinct keys → capacity 16; adding up to 12 → capacity 32, len 12, all keys readable.
