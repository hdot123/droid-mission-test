# Handoff: tally-module (sub-issue #34)

## What was requested
Implement `tally.py` in the repository root with a single function `verdict(score)` using only the Python standard library, returning `"pass"` when `score >= 70` and `"fail"` otherwise, plus `tests/test_tally.py`. Scope was limited to `tally.py` and `tests/test_tally.py`.

Note on the conflicting spec: the work order's deliverable text says the pass line is 60 (`verdict(65)` → `"pass"`), but the acceptance criteria explicitly override this: the pass line must be 70 (`verdict(65)` → `"fail"`, `verdict(70)` → `"pass"`). I followed the acceptance criteria and the process card, which both mandate 70.

## What I did
- Created `tally.py` with `verdict(score)`: returns `"pass"` if `score >= 70`, else `"fail"`. No imports, no CLI, no `__main__` block, no package directory.
- Created `tests/test_tally.py` with four pytest tests: `verdict(70) == "pass"`, `verdict(65) == "fail"`, `verdict(59) == "fail"`, `verdict(0) == "fail"`. The test file imports only `tally`.

## What I did not do
- Did not touch `hexcodec.py`, `initials.py`, or any other test file.
- Did not create a CLI, package directory, or any cross-module imports.
- Did not commit or push.

## Checks run and results
- `pip install pytest` (pytest was not present in the environment; installed pytest 9.2.0).
- `python -m pytest -q tests/test_tally.py` → **4 passed** (exit code 0).

## What the validator must pay attention to
- The pass line is **70**, not 60. `verdict(65)` must be `"fail"` and `verdict(70)` must be `"pass"` per the acceptance criteria; the deliverable text's mention of 60 is superseded.
- Other process cards may implement their modules with a 60 threshold (hexcodec/initials don't involve thresholds; any full-repo `python -m pytest -q` run must still pass with tally at 70).
- Only `tally.py` and `tests/test_tally.py` were modified by this process.
