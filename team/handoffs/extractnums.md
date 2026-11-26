# Handoff: extractnums (sub-issue #910, work order #902 第57轮 B 单)

## What was requested

Implement `extractnums.py` exposing `extract_numbers(text: str) -> list`, plus
`tests/test_extractnums.py`, under a **pinned token grammar**:

- token = `\d+(\.\d+)?` or `\.\d+`, scanned left to right with **maximal munch**
  (longest integer part + optional fractional part first);
- after a token ends, a following `.` whose next character is a digit forms a
  **new standalone** `\.\d+` token (does NOT merge with the previous token);
- top-priority example, verbatim: `"v2.0.1 build 45"` → `[2.0, 0.1, 45]`;
  same shape: `"3.14.15"` → `[3.14, 0.15]`;
- no signs (`"-5"` → `[5]`), no exponent/thousands (`"1e5"` → `[1, 5]`,
  `"1,000"` → `[1, 0]`); lone `.` forms no token;
- tokens containing `.` → `float`, otherwise `int`; non-`str` input →
  `TypeError`.

Only two implementation files owned by this card: `extractnums.py`,
`tests/test_extractnums.py`.

## What I did

- Created `extractnums.py`: a single-pass left-to-right scanner implementing
  the pinned grammar exactly (integer-part munch, optional `.` + digit
  fractional part, standalone `\.\d+` branch, lone-`.` skip). Standard library
  only; no imports from `motzkin`/`line2d` or anything else.
- Created `tests/test_extractnums.py` covering **every** acceptance item from
  the work order: 20 value assertions (empty, `abc`, `a1b2`, `3.14`, `.5`,
  `5.`, `007`, `1e5`, `-5`, `1,000`, `3.14.15`, `price 12.50 and 3 items`,
  `..7..`, `0.0.0`, `v2.0.1 build 45`, `1000000`, `9.`, `.`, `a.b`,
  `x0.25y`), per-item type assertions (float vs int, incl. `45` being `int`
  in the key example), and `TypeError` tests for `extract_numbers(12)` and
  `extract_numbers(None)`.

## What I did NOT do

- Did not touch any existing file (verified: `git status` shows only the two
  new files; pre-existing untracked `worker-prompt.txt` / `worker-stream.jsonl`
  are not mine and were left alone).
- Did not implement `motzkin` or `line2d` (other cards).
- Did not commit or push.
- No `verdict.json` / `verdict.md` by-products existed after the runs; nothing
  to delete (checked).

## Checks run and results

1. `python3 -m pytest tests/test_extractnums.py -q` → **24 passed**
2. `python3 -m pytest tests/ -q` → **366 passed, 2 skipped** (full suite green)

## Validator notes

- The decisive behavior is the standalone-dot rule: after `2.0` ends, the
  following `.1` is a separate token → `[2.0, 0.1, 45]`, NOT `[2.0, 1, 45]`
  and NOT a whole version string; `3.14.15` → `[3.14, 0.15]`.
- Trailing dot with no digit (`"5."`, `"9."`) yields an **int**, while a
  leading/embedded dot fraction yields **float**; verify per-item types, not
  just equality of values (list equality alone would not distinguish `1` vs
  `1.0`… actually `[1.0] == [1]` is True in Python, so type checks matter).
- `extract_numbers(12)` and `extract_numbers(None)` must raise `TypeError`.
- Tests import the module by inserting the repo root on `sys.path`, matching
  the flat layout of `roman.py`/`legacy_stringkit.py`.
