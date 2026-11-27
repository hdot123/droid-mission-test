# Handoff: natsort (sub-issue #970, work order #954 第59轮 D 单)

## What was requested

Implement `natural_sort(items: list[str]) -> list[str]` in a new `natsort.py` plus a new `tests/test_natsort.py` covering every acceptance point of the natsort card:

- Natural order: split each string into alternating numeric/non-numeric segments; compare segment by segment — numeric segments by numeric value, equal value → fewer digits first (fewer leading zeros first); numeric vs non-numeric → numeric first; non-numeric by code point; one segment list a prefix of the other → shorter first.
- Return a NEW list; never mutate the input.
- Input contract: non-list container or non-str element → `TypeError` (no `ValueError` surface).
- Standard library only; must not import huffman or happy.
- Only create `natsort.py` and `tests/test_natsort.py`; edit no existing file.

## What I did

- Created `natsort.py`:
  - `_segments` uses `re.findall(r"\d+|\D+")` for the alternating segment split.
  - `_sort_key` encodes each segment as a tuple with a type tag first: numeric → `(0, int, len, "")`, non-numeric → `(1, 0, 0, text)`. The tag pins "numeric first", value compares before digit count, and digit count breaks the `"a01"` vs `"a1"` tie deterministically (no ambiguous tie).
  - `_compare` is an explicit comparator implementing the same rules (used only by the test's cross-check path via a test-local reference; `natural_sort` itself uses `sorted(..., key=_sort_key)`).
  - `natural_sort` validates `isinstance(items, list)` and every element `isinstance(str)` raising `TypeError`, then returns `sorted(...)` (a new list).
- Created `tests/test_natsort.py` with a case for every acceptance point:
  - `["a10","a2","a1"]` → `["a1","a2","a10"]`; `["a01","a1","a001"]` → `["a1","a01","a001"]`; `["x","1","a"]` → `["1","a","x"]`; `[]` → `[]`.
  - Input unchanged item-by-item (identity-checked) and result is a new list.
  - Random property: 40 seeded random word lists (seed 20261127) — key-function sort vs an independent explicit comparator (test-local `_ref_compare`, reimplemented from the spec, not importing natsort internals) agree element by element.
  - `TypeError` for `"a10"`, `["a", 1]`, `None`.
  - Extra boundary cases: prefix-shorter-first (`["ab","a"]`, `["a1b","a1"]`) and alternating-segment comparison (`["2b","10a","2a"]` → `["2a","2b","10a"]`).

## What I did NOT do

- Did not touch `huffman.py`, `happy.py`, or any existing repo file (only the two owned files plus this handoff and `team/status/natsort.json`).
- Did not commit or push.
- Did not add a `ValueError` surface (none exists for this card).
- No cross-module imports (huffman/happy untouched; natsort imports only `re` from the stdlib; tests import only stdlib + `natsort`).

## Checks run

From repo root:

1. `python3 -m pytest tests/test_natsort.py -q` → **12 passed** in 0.02s.
2. `python3 -m pytest tests/ -q` → **354 passed, 2 skipped** in 19.71s (whole suite, exit 0).

No `verdict.json` / `verdict.md` byproducts were produced by these runs (checked with `ls`; none present).

## What the validator must pay attention to

- The `"a01"` vs `"a1"` tie is broken by digit count in the key tuple's third element — this is pinned behavior, not input-order dependent; randomized property test would catch any regression.
- `natural_sort` returns a fresh list from `sorted()`; the test asserts result is not the input object and the input is unchanged item-by-item.
- The random property test uses a test-local reference comparator reimplemented from the spec text — agreement is independent evidence, not circular reuse of the implementation.
- Only two new files exist for this card: `natsort.py`, `tests/test_natsort.py` (plus this handoff and `team/status/natsort.json` as team files).
