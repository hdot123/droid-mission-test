# Handoff: luhn-module (sub-issue #125)

## What was requested
Process card `luhn-module` for work order #121 (第二十三轮 B 单 · v2.6.5 并发重考):
own exactly `luhn.py` and `tests/test_luhn.py`, implementing `is_valid(number)` per spec:
- ignore spaces and hyphens;
- remaining content must be pure digits with length >= 2, otherwise `ValueError`;
- Luhn algorithm: from the right, double every second digit, subtract 9 if doubled
  value > 9, valid iff sum % 10 == 0;
- stdlib only; no cross-module imports; no package dir; no CLI;
- tests must cover: valid numbers, invalid numbers, separators ignored, rejection of
  non-digit content, rejection when length < 2; test file tests only luhn.py.

## What I did
- Created `luhn.py` at repository root with `is_valid(number)` exactly as specified
  (ValueError for non-digit content and for digit length < 2; Luhn doubling from right).
- Created `tests/test_luhn.py` with 5 test functions covering all five required
  behaviors (valid, invalid, separators ignored incl. separator-only input rejected,
  non-digit rejection, length < 2 rejection including empty string).
- Installed pytest 9.2.0 (it was missing from the environment: `python -m pytest`
  failed with "No module named pytest") via `python -m pip install pytest`
  (user install) so the card's check command could run.

## What I did not do
- Did not touch `morse.py`, `nato.py`, any other test file, `team/**` of other
  processes, `.github/**`, or any file outside my scope.
- Did not add package directories or CLI entry points.
- Did not commit or push.
- Did not run the full suite `python -m pytest -q` (it covers other processes'
  modules, executed in parallel by them; per card note, my file-level verification
  is the checks command).

## Checks I ran and results
1. `python -m pytest tests/test_luhn.py -q` — first run: **2 failed, 3 passed**
   (my own test fixtures `1234567890123456` / `...3452` were hand-picked and
   wrong: the former fails Luhn, the latter passes; algorithm itself was correct
   — both Visa examples passed with their +1 variants failing).
2. Fixed the two fixtures to a correct valid/invalid pair (`1234567890123452` valid,
   `1234567890123456` invalid).
3. `python -m pytest tests/test_luhn.py -q` — **5 passed in 0.01s** (final, exit 0).

## Notes for the validator
- The check command in my status file is verbatim the card's checks entry:
  `python -m pytest tests/test_luhn.py -q`.
- pytest had to be pip-installed in this environment; if the validator re-runs the
  check in a fresh env, it may need the same install.
- Known-valid fixtures independently verify the algorithm: `79927398713` and
  `4532015112830366` (Luhn-valid), and their single-digit variants are invalid.
- The full-suite run `python -m pytest -q` is the work order's acceptance gate and
  depends on the other two modules' tests landing from their own processes.
