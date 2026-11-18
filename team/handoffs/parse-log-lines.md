# Handoff: parse-log-lines (sub-issue #234)

## What was requested

Deliver the **parsing (解析)** capability for the log-analysis tool set (work order #232, process card `parse-log-lines`):

- One module at the repository root, `log_parser.py`, that turns a single raw log line into a structured record (timestamp, level, message) and explicitly signals malformed lines instead of silently swallowing them.
- Only the one required format: `2026-11-18 12:03:22 INFO service started` = date (YYYY-MM-DD), time (HH:MM:SS), level, message. Levels are exactly DEBUG / INFO / WARN / ERROR. No other log formats.
- Malformed categories that MUST be recognized as errors: wrong field count, bad date/time shape, unknown level (e.g. FATAL/TRACE), and no message after the level.
- A dedicated test file covering this module only; standard library only; docstrings that agree with the implementation.
- Owned files only: `log_parser.py`, `tests/test_log_parser.py`, plus this handoff and `team/status/parse-log-lines.json`.

## What I did

- Created `log_parser.py` at the repo root with:
  - `LEVELS = ("DEBUG", "INFO", "WARN", "ERROR")`.
  - `LogRecord` (frozen dataclass): `timestamp: datetime`, `level: str`, `message: str`.
  - `ParseError` (frozen dataclass): `line: str`, `reason: str` — the explicit error type; callers distinguish results with `isinstance`.
  - `parse_line(line) -> LogRecord | ParseError` — parses one line; never swallows a bad line.
  - `parse_lines(lines) -> list` — parses many lines in order, keeping every result (record or error), nothing dropped.
- Malformed detection implemented:
  - wrong field count (fewer than three fields, or three fields with no message text after the level);
  - bad date/time shape (not `YYYY-MM-DD HH:MM:SS` or not a real date/time, via `datetime.strptime`);
  - unknown level (anything outside the four values, e.g. FATAL/TRACE);
  - missing/blank message after the level; also empty/blank lines.
- Documented all public functions/types with docstrings stating behavior.
- Created `tests/test_log_parser.py` (unittest) covering: correct parse of a well-formed line (timestamp/level/message each in place), all four levels, multi-word message, `parse_lines` ordering, and an explicit error assertion for each malformed category above (plus blank lines and a `ParseError`-is-not-`LogRecord` check).

## What I did NOT do

- No filtering, statistics/aggregation, or formatting code — those belong to the other three cards.
- No other modules, no package directories, no CLI, no dependencies beyond the Python standard library.
- No edits to any file owned by other processes (e.g. `legacy_stringkit.py`, `tests/test_legacy_stringkit.py`, README, worker files).
- No commits, no pushes.

## Checks run

From the repository root, exactly the card's check:

```
python -m unittest discover -s tests -p "test_log_parser.py" -v
```

Result: **PASS** — 12 tests, all `ok`, `Ran 12 tests ... OK` (exit code 0).

## Notes for the validator

- `parse_line` returns a union type: `LogRecord` on success, `ParseError` on failure. Success/failure must be distinguished by `isinstance`, not by exceptions.
- Scope check: only `log_parser.py` and `tests/test_log_parser.py` were added by this card (plus these two team files). No other capability module appears from this card; the four capabilities are split across four cards.
- Tests import `log_parser` as a top-level module (repo root on `sys.path` via `unittest discover`), consistent with the existing test layout.
