# Handoff: aggregate-log-stats (sub-issue #236)

## What was requested
Process card `aggregate-log-stats` from work order #232 (实现一组日志分析小工具 · 第三十一轮). This card owns only the STATISTICS/AGGREGATION capability: a single module at the repository root plus its dedicated test file. Four independent modules were split from the order (parse, filter, aggregate, format); this card delivers only aggregation. Constraints: Python standard library only, no package directories, no CLI, do not import or edit the parser module (consume duck-typed records).

Required aggregations:
1. Per-level counts — every one of DEBUG/INFO/WARN/ERROR present, including zero counts.
2. ERROR frequency over a time window — ERROR count with inclusive boundaries, plus a way to express frequency over the window duration.
3. Top messages — most frequent messages, descending count, deterministic tie-break, configurable limit.

## What I did
- Created `log_stats.py` at the repository root with the public API:
  - `LEVELS` — tuple of the four level names.
  - `count_by_level(records)` → dict of all four levels to counts (unknown levels ignored).
  - `error_frequency(records, start, end)` → ERROR count inside `[start, end]`, boundaries inclusive.
  - `error_rate(records, start, end)` → ERROR count divided by window duration in hours; returns 0.0 for zero/negative-length windows.
  - `top_messages(records, limit=10)` → `[(message, count)]` sorted by descending count, ties broken by ascending message text; `limit <= 0` returns `[]`.
  - Every public function has a docstring stating its behavior.
- Created `tests/test_log_stats.py` covering: zero-count levels, per-level counts, unknown-level handling, error frequency inside/outside/inclusive-boundary, error rate over window duration, top-message ordering, deterministic tie-break, limit respected (including 0), default limit of 10, and empty input. Records are hand-built stubs inside the test file; the parser module is never imported.

## What I did not do
- Did not create, edit, or import the parser (`log_parse`), filter, or format modules — those are owned by other cards.
- Did not add a CLI, package directories, or any non-standard-library dependency.
- Did not commit or push.

## Checks run
- `python -m unittest discover -s tests -p "test_log_stats.py" -v` from the repository root → 13 tests, all `OK` (exit code 0).

## Notes for the validator
- Level vocabulary is exactly DEBUG/INFO/WARN/ERROR; no other formats are accepted.
- `error_frequency` counts only ERROR records with a non-`None` timestamp inside the inclusive window; non-ERROR records in the window are excluded.
- `error_rate` returns a float (errors per hour); the zero-length window case returns 0.0 rather than raising, as documented.
- `top_messages` tie-break is ascending message text, so ordering is deterministic for equal counts.
- Tests in `tests/test_log_stats.py` test `log_stats.py` only, per the card's constraint.
