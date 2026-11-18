# Handoff: hamming-distance (sub-issue #352)

## What was requested
Implement the Hamming distance component of work order #345 (第四十轮 B):
- New file `hamming.py` with `distance(a: str, b: str) -> int` returning the number of positions at which two equal-length strings differ; raise `ValueError` if lengths differ.
- New file `tests/test_hamming.py` with a test case for every acceptance point:
  - `distance("karolin", "kathrin") == 3`
  - `distance("1011101", "1001001") == 2`
  - `distance("toned", "roses") == 3`
  - `distance("", "") == 0`
  - `distance("abc", "abc") == 0`
  - `distance("abc", "abd") == 1`
  - `distance("a", "ab")` raises `ValueError`
- Constraints: new files only, no changes to any existing file, standard library only, no import of `varint` or `zigzag`.

## What I did
- Created `hamming.py`: `distance()` compares lengths first (raises `ValueError` on mismatch), then counts differing positions via `zip`.
- Created `tests/test_hamming.py`: 7 tests (pytest), one per acceptance point, including the `ValueError` case via `pytest.raises`.
- Only these two files plus the two team files (`team/handoffs/hamming-distance.md`, `team/status/hamming-distance.json`) were created.

## What I did not do
- Did not touch `varint.py`, `zigzag.py`, or their tests (owned by other process cards).
- Did not modify any existing repository file (`roman.py`, `legacy_stringkit.py`, existing tests, etc.).
- Did not commit or push.

## Checks run and results
1. `python3 -m pytest tests/test_hamming.py -q` → 7 passed.
2. `python3 -m pytest tests/ -q` → 18 passed (full suite, includes other processes' tests present at the time).

Note: `pytest` was not installed in the environment initially; it was installed via `python3 -m pip install pytest` (pytest 9.2.0) to run the required checks. No repository files were changed by this.

## For the validator
- The two checks above are the exact commands from the process card; both pass.
- `hamming.py` uses only the standard library (`zip`, `sum`, `len`) and imports nothing from the repo.
- Acceptance coverage: all 7 listed criteria each have a dedicated test in `tests/test_hamming.py`.
- File ownership: only `hamming.py` and `tests/test_hamming.py` were added; no existing files were modified.
