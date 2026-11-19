# Handoff: primorial-product (sub-issue #474)

## What was requested

Process card "primorial-product" under work order #458 (round 45, concurrent D ticket): create exactly two new files, `primorial.py` and `tests/test_primorial.py`, implementing `primorial(n: int) -> int` — the product of the first n primes (p_n#), with `primorial(0) == 1` (empty product).

Validation rules (verbatim from the card):
- `n` must be an `int` >= 0.
- `n < 0` raises `ValueError`.
- A non-`int` raises `TypeError`, and `bool` must be rejected as well (`primorial(True)` raises `TypeError`).

Every acceptance example had to have a corresponding test case with exactly the specified expected value:
`primorial(0) == 1`; `primorial(1) == 2`; `primorial(2) == 6`; `primorial(3) == 30`; `primorial(4) == 210`; `primorial(5) == 2310`; `primorial(6) == 30030`; `primorial(7) == 510510`; `primorial(8) == 9699690`; `primorial(9) == 223092870`; `primorial(10) == 6469693230`; `primorial(6) // primorial(5) == 13`; `primorial(-1)` raises `ValueError`; `primorial(3.0)` raises `TypeError`; `primorial(True)` raises `TypeError`.

Constraints: standard library only, no import of `convexhull` or `porta`, no modification of any existing file.

## What I did

- Created `primorial.py`: implements `primorial(n)` with the required validation (`isinstance(n, bool)` check first so `bool` is rejected before the `int` check; `n < 0` raises `ValueError`) and computes the product by trial division over successive candidates, using only the standard library (no imports).
- Created `tests/test_primorial.py`: one test case per acceptance example above (15 tests total), using `pytest.raises` for the three error cases, importing `primorial` from the top-level module (same style as `tests/test_roman.py`).
- Ran both process checks (pytest was not installed on the system interpreter; installed it with `python3 -m pip install --user pytest`):
  - `python3 -m pytest tests/test_primorial.py -q` → **15 passed in 0.02s**
  - `python3 -m pytest tests/ -q` → **26 passed in 0.03s**
- Wrote this handoff and `team/status/primorial-product.json`.

## What I did not do

- Did not create or modify `convexhull.py`, `porta.py`, `tests/test_convexhull.py`, `tests/test_porta.py`, or any other existing file.
- Did not touch any `team/` file other than my two assigned ones.
- Did not commit or push anything.
- Did not import `convexhull` or `porta` (my implementation is self-contained).

## Checks run and results

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_primorial.py -q` | 15 passed |
| `python3 -m pytest tests/ -q` | 26 passed |

Note: `python3 -m pytest` initially failed with `No module named pytest`; I installed pytest via `python3 -m pip install --user pytest` (user site, no system files touched), after which both checks passed. The full-suite run covers the pre-existing `test_roman.py` and `test_legacy_stringkit.py` as well, all green.

## What the validator must pay attention to

- `primorial(True)` must raise `TypeError`: the implementation rejects `bool` explicitly before the general `isinstance(n, int)` check, since `bool` is a subclass of `int`.
- `primorial(3.0)` must raise `TypeError` (float is not an `int`), and `primorial(-1)` must raise `ValueError` (order: type check first, then range check).
- All 15 acceptance values are asserted exactly, including the ratio check `primorial(6) // primorial(5) == 13`.
- Only two files were added by this process; the repo should show no modifications to pre-existing files from this card.
