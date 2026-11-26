# Handoff: jaro (sub-issue #890)

## What was requested

Process card `jaro` under work order #879 (第56轮 D 单). Implement the **original Jaro string similarity, without Winkler prefix weighting**, in two new files only:

- `jaro.py`
- `tests/test_jaro.py`

Hard constraints: add only those two files, modify no existing file, standard library only, no cross-imports between the three work-order modules (fuelconv / jaro / multiset), and every acceptance item in the card must have a corresponding test case.

## What I did

- **`jaro.py`** — single public function `jaro_similarity(s1: str, s2: str) -> float`:
  - Input contract: any non-`str` argument (including `None`, `int`, `bytes`, `bool`) raises `TypeError`.
  - `s1 == s2` returns `1.0` (covers both-empty `("", "") -> 1.0` and identical strings); one empty side returns `0.0`.
  - Match window = `max(len(s1), len(s2)) // 2 - 1`, floored at 0.
  - Greedy left-to-right in-window matching with a visited flag per side; `m == 0` returns `0.0`.
  - Transpositions counted as half the mismatches between the two matched subsequences aligned in order; formula `(m/len1 + m/len2 + (m - t)/m) / 3`.
  - **No Winkler prefix bonus term anywhere.**
- **`tests/test_jaro.py`** — 11 test functions covering every acceptance item: the four reference pairs (MARTHA/MARHTA 0.9444…, DWAYNE/DUANE 0.8222…, DIXON/DICKSONX 0.7666…, CRATE/TRACE 0.7333…), empty-string cases, identical/disjoint strings, single chars, the `("ab","ba") -> 0.0` zero-window case, symmetry across 17 pairs, value-in-[0,1] across the same pairs, and `TypeError` for `"a"/1`, `None/"a"`, `1/"a"`, `b"a"/"a"`, `True/"a"`.

## What I did NOT do

- Did not touch any existing file (no edits to `roman.py`, `legacy_stringkit.py`, README, scripts, schemas, or any other test).
- Did not implement `fuelconv.py` or `multiset.py` (owned by sibling cards on the same work order).
- Did not add any Jaro–Winkler behavior, prefix scaling constant, or bonus term.
- Did not commit or push anything.

## Checks run and results

1. `python3 -m pytest tests/test_jaro.py -q` → **11 passed in 0.02s**
2. `python3 -m pytest tests/ -q` → **353 passed, 2 skipped in 19.59s** (pre-existing skips, unrelated to this card)

No `verdict.json` / `verdict.md` by-products were produced in the repo root (checked; nothing to delete).

## Validator notes

- The headline trap: accepted values are the **original Jaro** numbers. `DWAYNE/DUANE` must be `0.8222…` (not `0.84`) and `DIXON/DICKSONX` must be `0.7666…` (not `0.8133`). My tests explicitly assert `!= pytest.approx(0.84)` and `!= pytest.approx(0.8133)` so a Winkler implementation fails here.
- `("ab","ba") == 0.0` is exact: with window 0 only diagonal positions match, `a`↔`b` and `b`↔`a`, so `m = 0`.
- All acceptance tolerances use `pytest.approx(..., rel=1e-9)` per the card's floating-point rule; exact-equality cases (`== 1.0`, `== 0.0`) are asserted directly.
- The file is stdlib-only (`pytest` is only imported in the test file, matching the repo's existing test convention as seen in `tests/test_roman.py`).
