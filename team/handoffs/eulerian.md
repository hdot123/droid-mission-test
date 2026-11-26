# Handoff — eulerian (sub-issue #943, work order #926 第58轮 A 单)

## What was requested

Process card `eulerian`: implement exactly two new files, `eulerian.py` and `tests/test_eulerian.py`, exposing:

- `eulerian(n: int, m: int) -> int` — Eulerian number A(n, m), the number of n-element permutations with exactly m descents.
- `eulerian_row(n: int) -> list[int]` — the full row `[A(n, 0), …, A(n, n−1)]`.

Contract: `n < 1` raises `ValueError`; `m` out of range (`< 0` or `> n−1`) raises `ValueError`; non-`int` inputs (including `bool`) raise `TypeError`. `m` counts descent positions (0..n−1), and each row sums to `n!` (not a Bell-like total). Standard library only; no imports of the other components (rectunion, joaat); no modification of any existing file.

## What I did

- Created `eulerian.py`:
  - Uses the standard recurrence `A(n, m) = (n−m)·A(n−1, m−1) + (m+1)·A(n−1, m)`, building rows iteratively from the row of 1.
  - `eulerian(n, m)` validates inputs then returns `row[m]`; `eulerian_row(n)` validates and returns the whole row.
  - Input validation order: type check first (bool excluded via `isinstance(x, bool)`), then range check. So `eulerian(5, True)` raises `TypeError` (bool), while `eulerian(0, 0)` raises `ValueError`.
  - Only standard library is used; in fact there are no imports at all (the recurrence needs none).
- Created `tests/test_eulerian.py` with 11 test functions, one per acceptance item (values transcribed exactly):
  - `eulerian_row(1) == [1]`, `(4) == [1, 11, 11, 1]`, `(5) == [1, 26, 66, 26, 1]`, `(6) == [1, 57, 302, 302, 57, 1]`, `eulerian(10, 3) == 455192`.
  - Properties for n ∈ [1, 12]: row sum equals `n!`; symmetry `eulerian(n, m) == eulerian(n, n−1−m)`; agreement with the Worpitzky alternating sum `Σ_k (−1)^k·C(n+1, k)·(m+1−k)^n`.
  - Brute-force descent counting over all permutations for n ≤ 7.
  - ValueError cases: `eulerian(0, 0)`, `eulerian(5, 5)`, `eulerian(5, -1)`, `eulerian_row(0)`.
  - TypeError cases: `eulerian(5.0, 2)`, `eulerian(5, True)`, `eulerian_row("5")`.

## What I did not do

- Did not touch `rectunion.py`, `joaat.py`, or any pre-existing file (only the two owned new files plus this handoff and `team/status/eulerian.json`).
- Did not commit or push (left to the workflow).
- Did not expand scope beyond the card.

## Checks run

- `python3 -m pytest tests/test_eulerian.py -q` → **11 passed**.
- `python3 -m pytest tests/ -q` → **353 passed, 2 skipped** (whole repository; the skips are pre-existing suite skips, unrelated to this card).

No `verdict.json` / `verdict.md` by-products appeared during my runs; nothing to delete on that front.

## Notes for the validator

- Type-vs-value error precedence is intentional: `bool` is rejected as `TypeError` before any range check, matching the acceptance list (`eulerian(5, True)` → TypeError).
- The Worpitzky test loops `k` from 0 to `m+1` inclusive; terms with `m+1−k == 0` contribute `0^n = 0` (n ≥ 1), so no special-casing is needed.
- All acceptance values are transcribed verbatim from the card; the acceptance section had no conflicts with the body.
