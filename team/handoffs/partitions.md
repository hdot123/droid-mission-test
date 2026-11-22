# Handoff: partitions (sub-issue #673, card id `partitions`)

## What was requested

Process card for work order #663 (round 48, concurrent card C): implement
`partitions(n: int) -> int` in a new `partitions.py`, plus
`tests/test_partitions.py`, covering every listed acceptance point:

- Exact partition count p(n) for n = 0..10, 15, 20, 25, 30, 50, 100
  (`p(0) == 1`, `p(100) == 190569292`).
- Validation: non-int (`2.5`, `"5"`, `True`) raises `TypeError` (bool rejected);
  negative n raises `ValueError`.
- Only the two files above may be added; no existing file may be modified;
  standard library only; no imports of other work-order modules.

## What I did

- Added `partitions.py` exposing `partitions(n)`. Validation first (bool and
  non-int -> `TypeError`, negative -> `ValueError`, `n <= 1` -> `1`), then the
  classic unbounded knapsack DP over part sizes: `counts[0] = 1`, and for each
  `part` in `1..n`, add `counts[k - part]` into `counts[k]` for
  `k = part..n`. Returns exact Python int (`counts[n]`).
- Added `tests/test_partitions.py`:
  - `@pytest.mark.parametrize` over all 17 required (n, p(n)) values.
  - `partitions(-1)` raises `ValueError`.
  - `partitions(2.5)`, `partitions("5")`, `partitions(True)` each raise
    `TypeError`.
- Environment note: `pytest` was not installed in the run environment
  (`No module named pytest`); I installed it with
  `python3 -m pip install pytest` (got pytest 9.2.0). No repository files were
  changed by that install.

## What I did not do

- Did not touch `bifid.py`, `rotate2d.py`, or their tests (owned by other
  processes on the same work order).
- Did not modify any pre-existing file (including `requirements-dev.txt`,
  existing tests, docs, or schemas).
- Did not commit or push.

## Checks run (from repository root)

- `python3 -m pytest tests/test_partitions.py -q` -> `21 passed in 0.02s`
- `python3 -m pytest tests/ -q` -> `57 passed in 2.94s` (includes the 21 new
  partition tests plus all pre-existing tests)

Both exit 0.

## What the validator must pay attention to

- `partitions(0) == 1` and `partitions(1) == 1` are both handled by the
  `n <= 1` early return; the DP array is only built for `n >= 2`.
- `bool` is rejected explicitly before the `isinstance(n, int)` check, because
  `bool` is a subclass of `int` in Python.
- The DP is O(n²) time / O(n) space; `p(100) == 190569292` is computed exactly
  as a native int, no floats involved.
- Test file uses `pytest.mark.parametrize` (21 test cases total in the file).
- The only environment change was installing the `pytest` package; the six
  deliverable files of this work order and all pre-existing files are otherwise
  untouched.
