# Handoff: semver-module (sub-issue #112)

## What was requested
Process card `semver-module` under work order #108 (round 21, foreman v2.6.4): implement `semver.py` exposing `compare(a, b)` plus `tests/test_semver.py`, standard library only, no imports of `baseconv` or `runlength`, no CLI, no package directory.

Spec for `compare(a, b)`:
- Compares two semantic version strings like `"1.2.3"`: three dot-separated numeric segments; segments may be omitted and are padded with `0` (`"1.2"` equals `"1.2.0"`).
- Returns `-1` (a < b), `0` (equal), `1` (a > b), compared segment-wise numerically.
- Raises `ValueError` for: non-numeric segment, more than three segments, empty string.
- Acceptance examples: `compare("1.10.0", "1.9.9") -> 1`, `compare("2.0", "2.0.0") -> 0`.

Owned files only: `semver.py`, `tests/test_semver.py`, plus `team/handoffs/semver-module.md` and `team/status/semver-module.json`.

## What I did
- Created `semver.py` with `_parse(version)` (validates type, empty string, segment count > 3, non-numeric/empty segments via `str.isdigit()`, pads to three segments with `0`) and `compare(a, b)` returning `-1`/`0`/`1` via tuple comparison of parsed integers.
- Created `tests/test_semver.py` (8 tests) covering:
  - both acceptance examples (`1.10.0` vs `1.9.9` -> 1; `2.0` vs `2.0.0` -> 0),
  - ordering results -1/0/1,
  - omitted-segment padding equivalence (`"1.2"` vs `"1.2.0"`, `"1"` vs `"1.0.0"`, `"1.2"` vs `"1.2.10"`),
  - all three `ValueError` cases (non-numeric segment including empty segment `"1..0"`, more than three segments, empty string on either or both sides).
- Installed `pytest` (via `python -m pip install pytest`, pytest 9.2.0) because it was missing from the environment (`python: No module named pytest`); this was a prerequisite to running the mandated check.

## What I did not do
- Did not touch `baseconv.py`, `runlength.py`, `tests/test_baseconv.py`, `tests/test_runlength.py`, or any other repository file.
- Did not import `baseconv` or `runlength` from `semver.py` or its tests.
- Did not add a CLI, package directory, or non-standard-library dependency (pytest is the test runner only, invoked as specified by the card).
- Did not commit or push.

## Checks run and results
Verbatim from this card's checks list:

1. `python -m pytest tests/test_semver.py -q` — initially failed with `No module named pytest` (environment lacked pytest, not a code failure). After `python -m pip install pytest`, the same command run verbatim:
   - Result: `........ [100%]` / `8 passed in 0.01s` (exit code 0).

## Validator notes
- The only check on the card is `python -m pytest tests/test_semver.py -q`; it passes 8/8 only after pytest is installed. If the validation environment lacks pytest, install it first (`python -m pip install pytest`) before rerunning — the earlier failure was environmental, not a code defect.
- `semver.compare` rejects non-string inputs with `ValueError` as well (defensive, not required by spec but consistent with the invalid-format contract).
- Files outside this process's scope were not modified; `git status` before my work showed only untracked `worker-prompt.txt` and `worker-stream.jsonl` (pre-existing, untouched).
