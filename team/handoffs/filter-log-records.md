# Handoff: filter-log-records (sub-issue #235)

## What was requested

Work order #232 (第三十一轮, 拆解观察组) asked for a set of four log-analysis
modules (parsing, filtering, statistics, formatting) at the repository root
plus one dedicated test file per module, stdlib only, no package dirs, no CLI.

This card owns ONLY the filtering share:

- Create `log_filter.py` at the repository root exposing a public filtering API:
  - Level filter: keep records at a given level AND ABOVE (e.g. WARN keeps
    WARN+ERROR, drops INFO/DEBUG).
  - Time-window filter: keep records inside a given interval, boundaries
    inclusive, comparing datetimes.
  - Both filters usable together; input order preserved in every result.
- Consume parser-produced records duck-typed (`datetime`+`level` attributes or
  plain sequences of them); expose small internal level-severity constants
  (DEBUG=0 … ERROR=3). Must NOT import or edit the parser module.
- Create `tests/test_log_filter.py` covering only this module: level
  thresholds at each boundary (DEBUG keeps all; ERROR keeps only ERROR; WARN
  drops INFO/DEBUG), time-window cases including both endpoints and an outside
  record, combined level+time filtering, and order preservation, using
  hand-built record stubs.

## What I did

- Created `log_filter.py`:
  - Module docstring documents duck-typed record contract and the no-CLI /
    stdlib-only constraints.
  - Severity constants `DEBUG=0, INFO=1, WARN=2, ERROR=3` (public module
    constants; level vocabulary is exactly DEBUG/INFO/WARN/ERROR).
  - `filter_by_level(records, min_level)` — keeps records with severity >=
    threshold; `min_level` may be a constant or a level-name string; raises
    `ValueError` on unknown threshold or unknown record level; returns a new
    list, order preserved, input not mutated.
  - `filter_by_time(records, start, end)` — keeps records with
    `start <= timestamp <= end` (both endpoints inclusive); `start`/`end` may
    be `None` for an unbounded side; inverted window returns `[]`; reads the
    `timestamp` attribute, falling back to `datetime`; raises `AttributeError`
    if neither exists; returns a new list, order preserved, input not mutated.
  - Both functions have docstrings stating exactly this behavior.
- Created `tests/test_log_filter.py` with 23 tests (unittest):
  - `SeverityConstantsTest`: constants equal 0/1/2/3 and ordered DEBUG < INFO <
    WARN < ERROR.
  - `FilterByLevelTest`: DEBUG threshold keeps all; ERROR keeps only ERROR;
    WARN drops INFO/DEBUG; INFO keeps info-and-above; string thresholds;
    record-level-as-constant; ValueError on unknown threshold and unknown
    record level; order preservation; new-list/no-mutation; plain sequences.
  - `FilterByTimeTest`: both endpoints inclusive; outside records dropped;
    `None` start/end unbounded; inverted window returns `[]`; order
    preservation; missing-timestamp AttributeError; `datetime` attribute
    fallback; new-list/no-mutation.
  - `CombinedFilterTest`: level-then-time and time-then-level give the same
    members in the same order.

## What I did NOT do

- Did not create or edit any other module (no parser, statistics, or
  formatting module; those belong to other cards).
- Did not modify `legacy_stringkit.py`, `tests/test_legacy_stringkit.py`, the
  README, or any other pre-existing file.
- Did not import the parser module anywhere (tests use local stubs only).
- Did not add a package directory, `__init__.py`, or any CLI.
- Did not commit or push.

## Checks run and results

From the repository root (exactly the card's check command):

```
python -m unittest discover -s tests -p "test_log_filter.py" -v
```

Result: PASSED — 23 tests ran, all `ok`, exit code 0
(`Ran 23 tests in 0.001s / OK`).

Note: the card's acceptance line also says "三件交付合并进主仓后，仓库全部测试
须同时通过" (all repo tests must pass after merge). The full-repository run is
not this card's check command, so I ran only my card's check. The only other
pre-existing test file is `tests/test_legacy_stringkit.py`, which is untouched
by my changes (I added only new files), so it is unaffected by this card.

## What the validator must pay attention to

- My card's scope is filtering only; the other three capabilities are on other
  cards. After all cards merge, the four modules together must cover
  解析/过滤/统计聚合/格式化 with no extra module — I added exactly
  `log_filter.py` and `tests/test_log_filter.py`.
- Duck-typing contract: records expose `timestamp` (preferred) or `datetime`
  plus `level`. My tests intentionally do NOT import the parser, so the
  parser's attribute names should match this contract (`timestamp` and/or
  `datetime`) for the combined system to work end to end. The time filter
  accepts either attribute name.
- Level vocabulary is exactly DEBUG/INFO/WARN/ERROR; unknown levels raise
  `ValueError` rather than being silently kept or dropped.
- Time-window boundaries are inclusive on both ends (verified by a test where
  start/end exactly equal a record's timestamp).
- Docstrings and tests describe the same behavior as the implementation; no
  behavior exists in code that is undocumented, and vice versa.
