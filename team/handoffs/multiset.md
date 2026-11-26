# Handoff: multiset (sub-issue #893, D 单 third item)

## What was requested

Implement `multiset.py` with class `MultiSet(iterable=None)` — a mutable
multiset with set algebra — plus `tests/test_multiset.py`. Add-only: no
existing file may be modified, standard library only, no imports from the
sibling work-order modules (`fuelconv`, `jaro`). Every acceptance item in the
card must have a corresponding test.

Spec summary:
- Construction counts each item of the iterable in order.
- `add(item, n=1)` / `remove(item, n=1)`: `n < 1` → ValueError; non-int `n`
  (including `bool`) → TypeError; removing more than held → ValueError; a
  count reaching zero deletes the item.
- Queries: `count` (0 for missing), `total`, `distinct`, `elements` (grouped,
  first-insertion order), `to_dict`.
- Set algebra, each returning a NEW MultiSet without mutating the original:
  `union` (per-item max, not sum), `intersection` (per-item min, not
  product), `difference` (per-item subtraction floored at 0, zero items
  dropped).
- `is_subset(other)`; `__len__` = total; `__contains__`; `__eq__` (False
  against any non-MultiSet).

## What I did

Created exactly two files:
- `multiset.py` — the `MultiSet` implementation above. Internal store is a
  plain `dict`, which in Python 3.7+ preserves first-insertion order, so
  `elements()` and `to_dict()` fall out naturally. `_validate_n` rejects
  `bool` before `int` (since `bool` is an `int` subclass) and rejects
  `n < 1`. `_require_multiset` raises TypeError for non-MultiSet operands in
  the set-algebra methods and `is_subset`. Union/intersection/difference
  build fresh count dicts and return `MultiSet._from_counts(...)`; the
  originals are never touched. `__eq__` returns False for non-MultiSet
  operands.
- `tests/test_multiset.py` — 27 tests covering every acceptance item: basic
  construction/queries (`MultiSet("aabbbc")`), empty-constructor equality,
  inequality of different counts, `to_dict`, `elements` first-insertion
  order (including the `banana` sorted round-trip and a generator input),
  union/intersection/difference both directions plus new-object identity and
  non-mutation, zero-dropping in difference, disjoint union, `is_subset` both
  directions, `MultiSet("ab") == {"a": 1, "b": 1}` is False, the
  add/remove lifecycle (`add("x", 3)` → `remove("x", 2)` → count 1 → further
  `remove` → absent and `distinct() == 0`), and every ValueError case
  (`remove("a", 2)` on `MultiSet("ab")`, `remove("ghost")` on empty,
  `add("x", 0)`, `add("x", -1)`) and TypeError case (`add("x", 1.5)`,
  `add("x", True)`, plus non-int/bool `remove`).

## What I did not do

- Did not touch `fuelconv.py`, `jaro.py`, or their tests — those belong to
  the sibling D 单 cards.
- Did not modify any pre-existing file (no edits to `roman.py`,
  `legacy_stringkit.py`, existing tests, docs, or config).
- Did not import anything outside the standard library, and no sibling
  work-order module.
- Did not commit or push.
- Did not implement tally/freqtable-style report functions; this is a
  mutable structure with set algebra, per the spec note.

## Checks run

- `python3 -m pytest tests/test_multiset.py -q` → **27 passed** in 0.04s
- `python3 -m pytest tests/ -q` → **369 passed, 2 skipped** in 19.50s

(The 2 skips are pre-existing suite skips, unrelated to this card. Note the
full-suite count will rise once the sibling `fuelconv` / `jaro` cards land.)

## Notes for the validator

- The trap called out in the work order (union = max not sum,
  intersection = min not product) is implemented and asserted; the original
  operands' `to_dict()` is re-checked inside the algebra tests to prove no
  mutation.
- `bool` is an `int` subclass in Python, so the TypeError check must test
  `isinstance(n, bool)` first; the implementation does, and the test
  `MultiSet().add("x", True)` asserts it raises TypeError (not ValueError).
- `elements()` grouping order is first-insertion order of distinct items;
  `MultiSet("aab").elements() == ["a", "a", "b"]` and
  `MultiSet("ab")` after `remove("a"); add("a")` yields `["b", "a"]` — both
  are asserted.
- Two extra ValueError tests (`remove` with n=0) were added beyond the
  literal list since `n < 1` is in the spec; they pass.
- `verdict.json` / `verdict.md` (if produced by the suite) are pipeline
  by-products, not deliverables, and were not kept.
