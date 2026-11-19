# Handoff: bloom-filter (sub-issue #487)

## What was requested

Process card `bloom-filter` from work order #479 (Round 46 · concurrent B, foreman v2.6.5):

- Create `bloom.py`: a fixed-length Bloom filter with deterministic double hashing.
  - `BloomFilter(size: int, k: int)` — `size`/`k` must be positive ints; `<= 0` raises `ValueError`, non-int raises `TypeError`.
  - Hashing pinned by spec (builtin `hash()` forbidden): h1 = FNV-1a 32-bit (init 2166136261, prime 16777619, XOR per byte then multiply, 32-bit wrap), h2 = djb2 32-bit (init 5381, `h = h*33 + byte`, 32-bit wrap), both over UTF-8 bytes; position i = `(h1 + i*h2) % size`.
  - `bit_positions(item: str) -> list[int]`: deduplicated, sorted positions; non-str raises `TypeError`.
  - `add(item: str) -> None`: sets all positions; non-str raises `TypeError`.
  - `__contains__(item: str) -> bool`: True iff all positions set.
  - `set_bits() -> list[int]`: sorted list of all set positions.
  - Every acceptance example gets a test case (size=100, k=3 vectors for "apple"/"banana"/"cherry", membership checks, `set_bits() == [8, 10, 36, 52, 53, 67, 72, 90, 94]`, idempotent re-add, constructor/add validation errors).
- Create `tests/test_bloom.py` covering each acceptance item.
- Constraints: only these two files; modify no existing file; standard library only; no import of other project modules.

## What I did

- Created `bloom.py` with module docstring, `_fnv1a_32` / `_djb2_32` helpers (32-bit mask `0xFFFFFFFF`), and the `BloomFilter` class (`bytearray` bit storage).
  - Validation order: `TypeError` for non-int (bools rejected as non-int per "int" requirement), then `ValueError` for `<= 0`. Note: `isinstance(True, int)` is true in Python, so explicit bool rejection was added.
  - `__contains__` validates `str` before computing positions (so `123 in bf` raises `TypeError`, consistent with `bit_positions`/`add`).
- Created `tests/test_bloom.py` with 15 test cases: each pinned position vector, fresh-filter membership, add/contains flow, multi-item membership, exact `set_bits()` output, idempotent re-add with `len(set_bits()) == 9`, `ValueError` constructors (0, 0-k, negative), `TypeError` constructors (float size, str k), `add(123)` TypeError, `bit_positions(123)` TypeError, `123 in bf` TypeError, fresh `set_bits() == []`, and sorted/dedup invariant.
- Ran the process checks; both pass (results below).

## What I did not do

- Did not touch `triangle.py`, `pangram.py`, `tests/test_triangle.py`, `tests/test_pangram.py`, or any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing tests, README, etc.).
- Did not create or modify any other process's `team/` files.
- Did not commit or push.
- Not in scope of my card, but relevant to the merged result: `tests/test_triangle.py` and `tests/test_pangram.py` did not exist yet when I ran the full suite (other concurrent processes own them).

## Checks run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_bloom.py -q` | 15 passed in 0.02s |
| `python3 -m pytest tests/ -q` | 26 passed in 0.03s (includes 11 pre-existing baseline tests + my 15) |

Environment note: pytest was not preinstalled; I installed it with `python3 -m pip install --break-system-packages pytest` (pytest 9.2.0) to run the required checks. No repository files were changed by that install.

## What the validator must pay attention to

1. Hash values are pinned by the spec. My implementation reproduces the required vectors exactly: `apple -> [10, 53, 67]`, `banana -> [36, 52, 94]`, `cherry -> [8, 72, 90]`, and `set_bits() == [8, 10, 36, 52, 53, 67, 72, 90, 94]`.
2. `bool` inputs: spec says non-int raises `TypeError`; since `bool` is a subclass of `int`, `BloomFilter(True, 3)` raises `TypeError` (explicitly rejected). If a future spec change wants bools accepted, this is the one spot to revisit.
3. `__contains__` with non-str raises `TypeError` rather than returning `False` — this matches the `bit_positions`/`add` TypeError requirement and is covered by a test.
4. Position computation happens before dedup/sort; duplicates within one item's k positions are collapsed, so `len(bit_positions(x)) <= k`.
5. Full-suite result (26 passed) reflects the repo state at my check time; after the other Round 46 B processes merge, the full suite should be re-run as the work order specifies (merged-state full test run is the acceptance authority).
