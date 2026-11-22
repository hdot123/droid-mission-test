# Handoff: base62 (sub-issue #778, work order #761 第52轮并发A单)

## What was requested

Implement `base62.py` and `tests/test_base62.py` only (new files, no pre-existing file touched):

- Alphabet pinned to `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz` (index 0–61 maps to the character value).
- `base62_encode(n: int) -> str`: `n` must be `int` (`bool` rejected) else `TypeError`; `n < 0` else `ValueError`; `base62_encode(0) == "0"`.
- `base62_decode(s: str) -> int`: non-`str` raises `TypeError`; empty string raises `ValueError`; out-of-alphabet character raises `ValueError`.
- Every acceptance point from the card must have a corresponding test case.
- Standard library only; must not import `chaocipher` or `centroid`.

## What I did

- Created `base62.py` with `ALPHABET`, a precomputed decode map, and both functions implementing the pinned spec (type checks before value checks; `bool` explicitly rejected for encode).
- Created `tests/test_base62.py` covering every acceptance point: single-digit/boundary encodes (0, 1, 9, 10, 35, 36, 61), multi-digit carry (62, 63, 3843, 238327), samples (12345 → "3D7", 987654321 → "14q60P"), decodes, round-trips for 0, 1, 61, 62, 3844, 10**12, 2**63-1, `ValueError` cases (-1; "", "!", "a b"), and `TypeError` cases (1.5, True, "12"; 123, None).

## What I did not do

- Did not touch `chaocipher.py`, `centroid.py`, their tests, or any pre-existing file.
- Did not add or modify anything under `team/` beyond my two assigned files.
- Did not commit or push.
- Did not import `chaocipher` or `centroid`.

## Checks run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_base62.py -q` | 21 passed in 0.03s |
| `python3 -m pytest tests/ -q` | 158 passed, 1 skipped in 15.74s |

Note: `pytest` was not installed in the environment; I installed it with `pip install pytest` (pytest 9.2.0) to run the required checks. `requirements-dev.txt` already pins `pytest>=7.4.0`.

## What the validator must pay attention to

- The single skip in the full suite is pre-existing and unrelated to base62 (it comes from the baseline suite, not from my files).
- Alphabet order is case-sensitive: digits → uppercase → lowercase. Spot-check `base62_encode(10) == "A"` and `base62_encode(36) == "a"`.
- `base62_encode(True)` must raise `TypeError`, not encode as `1` — `bool` is explicitly rejected before the `int` check.
- `base62_decode` validates per character and raises `ValueError` on the first out-of-alphabet character, including spaces (so `"a b"` is `ValueError`, not `TypeError`).
