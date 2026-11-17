# Handoff: isbn-module (sub-issue #26)

## What was requested
Process card "isbn-module" for work order #24 (领班制 v2.6.1), scope limited to two files:

- `isbn.py` in the repo root with two public functions:
  - `is_valid(isbn)` — validates ISBN-10 and ISBN-13; ignores hyphens and spaces anywhere; ISBN-10 check digit may be `X` (only as the last character); other illegal characters return `False` without raising; ISBN-10 checksum is `sum(digit*(10-i) for i in 0..8) + check_value` divisible by 11; ISBN-13 checksum is alternating 1/3 weights over 12 digits plus check, divisible by 10.
  - `to_isbn13(isbn)` — converts a valid ISBN-10 to ISBN-13 (`978` prefix + correct check digit); raises `ValueError` on any input that is not a valid ISBN-10.
- Global rule: every public function raises `TypeError` when its argument is `None` (never returns `False`/`None`).
- `tests/test_isbn.py` covering: valid ISBN-10/ISBN-13, hyphen/space stripping, `X` check digit, invalid characters, invalid checksums, conversion result, `ValueError` on invalid input, `TypeError` on `None` for both functions.
- Constraints: Python standard library only; no imports of other project modules; no package directory; no CLI; test file tests only `isbn.py`.

## What I did
- Created `isbn.py` with `is_valid` and `to_isbn13`. Shared helpers: `_require_str` (raises `TypeError` for `None` and for any non-`str`), `_digits_or_none` (length + character validation, `X` allowed only at the last position), `_isbn10_checksum_ok`, `_isbn13_checksum_ok`.
  - `is_valid` returns `True`/`False` only for string inputs of length 10 or 13 after stripping `-` and spaces; everything else malformed returns `False` (no exception). `None` (and non-strings) raise `TypeError`.
  - `to_isbn13` strips `-`/spaces, requires a well-formed and checksum-valid ISBN-10, else raises `ValueError`; `None`/non-strings raise `TypeError`. Result is 13 digits: `978` + first 9 digits + computed check digit.
- Created `tests/test_isbn.py` (17 tests) covering every case listed in the card, including `X` placement rules, checksum failures, length errors, conversion round-trip through `is_valid`, parametrized `ValueError` cases, and `TypeError` for `None` on both functions. Tests import `isbn` via a `sys.path` insert of the repo root (no package install).
- Nothing outside the two owned files plus the two required team files was created or modified.

## What I did NOT do
- Did not touch `duration.py`, `fence.py`, or their tests (owned by other processes).
- Did not modify `README.md`, `.github/`, or any other repo file.
- Did not add a package directory, `__init__.py`, CLI, or third-party dependency (pytest was installed into the environment to run the required check; it is not imported by `isbn.py`).
- Did not commit or push.

## Checks run
- `python -m pytest -q tests/test_isbn.py` → initially failed to start: `/usr/bin/python: No module named pytest` (pytest not installed in the environment).
- `python3 -m pytest -q tests/test_isbn.py` → same missing-module failure on Python 3.14.4.
- Installed pytest (`python3 -m pip install --quiet pytest`), then re-ran the card check:
  - `python3 -m pytest -q tests/test_isbn.py` → **17 passed in 0.03s** (exit code 0).

## What the validator must pay attention to
- The environment ships without pytest; the checker must install it (or use an interpreter that has it) before running `python -m pytest -q`. After installation the card check passes.
- `is_valid` deliberately returns `False` for non-string inputs other than `None` (e.g. `123`), matching the card's "illegal character → False, no exception" spirit; only `None` (the global rule) and other explicit `TypeError` cases are exceptions. `to_isbn13` raises `ValueError` for any invalid ISBN-10, including a valid ISBN-13 passed in.
- `X` is accepted only as the final character of an ISBN-10; lowercase `x` and `X` anywhere else return `False`.
- ISBN-10 check-digit weighting is `digit * (10 - i)` for `i = 0..8` plus the check value, equivalent to the card's `digit*(11-position)` for positions 1..9 plus check, divisible by 11.
