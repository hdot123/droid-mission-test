# Handoff: radixsort (sub-issue #940, work order #929 round-58 D)

## What was requested

Implement `radix_sort(values) -> list[int]` as an LSD radix sort per the
process card acceptance section (逐字为准), creating exactly two new files:
`radixsort.py` and `tests/test_radixsort.py`. Constraints: standard library
only, no modification of any existing file, every acceptance item must have a
corresponding test case.

Key spec points:
- Returns a new ascending list; input is list or tuple of ints; supports
  negatives; does not modify input.
- Non-int elements (including `bool` and `float`) raise `TypeError`;
  non-list/tuple input (e.g. str, int) raises `TypeError`.

## What I did

1. `radixsort.py`:
   - `_lsd_radix_nonnegative(nums)`: base-256 LSD radix sort over the
     non-negative part (digit = `(n // exp) % 256`, stable bucket passes until
     `max // exp == 0`), operating on a copy.
   - `radix_sort(values)`:
     - Type-checks container (`list`/`tuple` only) and every element
       (`bool`/non-`int` → `TypeError`).
     - Splits into negatives (stored as absolute values) and non-negatives;
       radix-sorts the absolute values of the negatives, reverses them and
       negates back, then concatenates `sorted_negatives + sorted_nonnegatives`
       — negatives land correctly before non-negatives.
     - Never mutates the input; returns a brand-new list.
2. `tests/test_radixsort.py`: 11 test functions covering every acceptance item:
   empty, single, three-element, negatives `[-5, 3, -1, 0]`, classic example
   `[170, 45, 75, 90, 802, 24, 2, 66]`, duplicates, large ints
   `10**18/10**12`, tuple input, input-not-modified snapshot property, random
   property (seeded `random.Random(58)`, 60 iterations, lengths 0–30, values
   ±10^6, compares against `sorted()` and re-checks input untouched), and the
   four `TypeError` cases (`"321"`, `[1, 2.0]`, `[1, True]`, `123`).

## What I did NOT do

- Did not touch `uuencode.py`, `hslconv.py`, or any existing repository file
  (only the two owned files plus these two team files were written).
- No commits/pushes (left to the workflow).
- Did not implement anything outside the radixsort card.

## Checks run

From repository root:

- `python3 -m pytest tests/test_radixsort.py -q` → **11 passed in 0.02s**
- `python3 -m pytest tests/ -q` → **353 passed, 2 skipped in 17.78s**

No `verdict.json` / `verdict.md` by-products appeared during my runs; none
needed cleanup.

## For the validator

- The input is intentionally validated strictly: `bool` and `float` elements
  must raise `TypeError` even though `bool` is an `int` subclass — check the
  `isinstance(v, bool)` guard.
- Negative handling is split-by-sign (abs-sort, reverse, negate), not a single
  pass over negatives as non-negatives; verify `radix_sort([-5, 3, -1, 0]) ==
  [-5, -1, 0, 3]` and that negatives sort by absolute value.
- The result must be a **new** list: `radix_sort(values) is not values` and
  the input list is item-for-item unchanged afterwards.
- Duplicate stability isn't required by spec (sorted order only), so plain
  bucket appends are fine.
