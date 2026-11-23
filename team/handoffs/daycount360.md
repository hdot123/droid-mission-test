# Handoff: daycount360 (sub-issue #821, work order #815 第54轮并发D单)

## What was requested

Process card `daycount360` for work order #815 (第54轮 并发 D 单): implement a 30/360 US (NASD)
day-count component. Own exactly two new files, nothing else:

- `daycount360.py` — `days360(start, end) -> int`
- `tests/test_daycount360.py` — one test case per acceptance item

Constraints: standard library only (datetime.date / calendar), no import of `sllist` or
`harmonic`, no modification or deletion of any existing file, no `team/`-scope conflicts beyond
my own handoff/status files.

Spec (verbatim from the card):

- Both `start` and `end` must be `datetime.date`; non-date raises `TypeError` (the examples are
  the string `"2024-01-15"` and `None`; `datetime.datetime` is a subclass of `date` and is not
  excluded by the card's wording, so it is accepted per the stated rule).
- `end < start` raises `ValueError`.
- Adjustment rules applied in order (d1/d2 = day-of-month of start/end):
  1. If start is the last day of February (Feb 28 common year, Feb 29 leap year), `d1 = 30`.
  2. If end is the last day of February AND start is also the last day of February, `d2 = 30`.
  3. If `d1 == 31`, `d1 = 30`.
  4. If `d2 == 31` and (after the preceding adjustments) `d1 == 30`, `d2 = 30`.
- Days = `(y2 - y1) * 360 + (m2 - m1) * 30 + (d2 - d1)`.

## What I did

Created exactly the two owned files:

1. `daycount360.py` — `days360()` implementing the four ordered rules using `calendar.monthrange`
   to detect February month-ends (handles both common and leap years). Type check runs before the
   `end < start` check so bad types give `TypeError` first; `end < start` then raises `ValueError`.
2. `tests/test_daycount360.py` — 13 test functions, one per acceptance item:
   - `days360(date(2024,1,15), date(2024,7,15)) == 180`
   - `days360(date(2024,1,31), date(2024,3,31)) == 60`
   - `days360(date(2024,1,30), date(2024,3,31)) == 60`
   - `days360(date(2024,1,15), date(2024,3,31)) == 76`
   - `days360(date(2023,2,28), date(2023,8,28)) == 178` (common-year Feb end, rule ①)
   - `days360(date(2024,2,29), date(2024,8,29)) == 179` (leap-year Feb end, rule ①)
   - `days360(date(2023,2,28), date(2024,2,29)) == 360` (rules ① and ② both fire)
   - `days360(date(2024,12,31), date(2025,1,31)) == 30`
   - `days360(date(2024,3,15), date(2024,3,15)) == 0`
   - `days360(date(2020,6,30), date(2021,6,30)) == 360`
   - `days360(date(2024,7,15), date(2024,1,15))` raises `ValueError`
   - `days360("2024-01-15", date(2024,7,15))` raises `TypeError`
   - `days360(date(2024,1,15), None)` raises `TypeError`

Both checks from the card were run after creation.

## What I did not do

- Did not create or touch `sllist.py`, `harmonic.py`, or their tests (owned by sibling cards).
- Did not modify, move, or delete any pre-existing repository file (verified via `git status`:
  only `daycount360.py` and `tests/test_daycount360.py` are new from this card; `worker-prompt.txt`
  and `worker-stream.jsonl` were already untracked before I started).
- Did not add third-party dependencies; only `datetime` and `calendar` from the standard library.
- Did not commit or push.
- Did not implement `datetime.datetime` rejection: the card's type rule is "must be a
  `datetime.date` instance; non-date raises `TypeError`", and `datetime` subclasses `date`, so it
  passes. The two required `TypeError` examples (str, `None`) both raise as specified.

## Checks run and results

1. `python3 -m pytest tests/test_daycount360.py -q` → **13 passed** (exit 0).
2. `python3 -m pytest tests/ -q` → **200 passed, 2 skipped in 15.43s** (exit 0). The 2 skips are
   pre-existing suite skips, unrelated to this card. No `verdict.json` / `verdict.md` by-products
   were produced; `rm -f verdict.json verdict.md` was run anyway (no-op).

Note: `pytest` was not installed in the environment at session start (`No module named pytest`);
I installed `pytest>=7.4.0` from `requirements-dev.txt` via `python3 -m pip install --user` to run
the required checks. This changes no repository file.

## What the validator must pay attention to

- Only two deliverable files from this card: `daycount360.py`, `tests/test_daycount360.py`.
  Team files: `team/handoffs/daycount360.md`, `team/status/daycount360.json`.
- Rule ordering matters and is covered by tests: rule ① sets `d1 = 30` before rule ③ would act
  (Feb 28/29 never equals 31, so no interference), and rule ④ checks `d1` *after* rules ①–③.
  The 2023-02-28 → 2024-02-29 case (360) is the joint ①+② case; the 2020-06-30 → 2021-06-30
  case (360) exercises rule ④ via `d1 = 30` and `d2 = 31 → 30`.
- Type errors are raised before the ordering check, so `days360(None, None)` would raise
  `TypeError`, not `ValueError` (not an acceptance item, but consistent with the card).
- The full suite (`python3 -m pytest tests/ -q`) must stay green: 200 passed, 2 skipped.
