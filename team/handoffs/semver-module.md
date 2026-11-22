# Handoff: semver-module (sub-issue #50)

## What was requested
Implement `semver.py` in the repository root (Python standard library only, no project imports, no package dir, no CLI) with:
- `parse(s)`: parse `"MAJOR.MINOR.PATCH"` into a tuple of three non-negative ints. Raise `ValueError` for `"1.2"`, `"1.2.x"`, `"v1.2.3"`, and leading-zero segments like `"01.2.3"`.
- `compare(a, b)`: segment-wise numeric comparison returning -1/0/1 (e.g. `compare("1.10.0", "1.9.9") == 1`, `compare("2.0.0", "2.0.0") == 0`).
- `is_valid(s)`: bool, never raises (e.g. `is_valid("1.2") == False`).
- `tests/test_semver.py` covering the examples, invalid formats including leading zeros, numeric (not lexicographic) comparison, and `is_valid` never raising.

## What I did
- Created `semver.py`: regex-based `_PATTERN = (0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z` enforces exactly three segments, digits only, and no leading zeros. `parse` returns the int tuple or raises `ValueError`; `compare` parses both sides and compares tuples; `is_valid` wraps `parse` in `try/except (ValueError, TypeError)` and returns bool.
- Created `tests/test_semver.py` (31 tests): all spec examples, zero/large segments, 11 invalid-format cases (too few/many segments, `x`, `v` prefix, leading zeros in each segment, negative, empty, whitespace), numeric-vs-lexicographic comparison (`1.10.0` vs `1.9.9`), dominance checks, `is_valid` returning `bool` and never raising (including `None` and `42`).

## What I did NOT do
- Did not touch `levenshtein.py`, `base32.py`, or their tests (owned by other processes).
- Did not commit or push (workflow does that).
- Did not create any package directory or CLI.

## Checks run
- `python -m pytest -q tests/test_semver.py` → **31 passed in 0.02s** (exit 0).
- Note: `python` initially had no pytest; installed `pytest 9.2.0` via `pip install --user pytest` so the check command runs. The check was executed as `python3 -m pytest -q tests/test_semver.py` (same interpreter/pytest).

## Validator attention
- `parse` raises `TypeError` (not `ValueError`) for non-str inputs such as `None`/`42`; the spec only requires `ValueError` for invalid format strings, and `is_valid` swallows both so it never raises.
- Leading zeros are rejected by regex (`0|[1-9][0-9]*`), so `"01.2.3"`, `"1.02.3"`, `"1.2.03"` are all invalid, matching the spec.
- `compare` propagates `ValueError` for invalid inputs; only `is_valid` guarantees no raise.
- Full-suite command `python -m pytest -q` may also run other workers' tests; mine passes standalone.
