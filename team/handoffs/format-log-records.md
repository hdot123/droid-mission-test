# Handoff: format-log-records (sub-issue #237)

## What was requested
Process card `format-log-records` for work order #232 (第三十一轮 日志分析小工具). This card owns only the FORMATTING capability (格式化输出) as one root-level Python module plus its dedicated test file:
- `log_format.py` at the repository root: public API formatting log records back into the uniform line shape `2026-11-18 12:03:22 INFO service started` (「日期 时间 级别 消息」), including formatting an iterable of records into an ordered list of lines, as the exact inverse of the line format. Only Python standard library; no CLI, no package directories.
- `tests/test_log_format.py`: covers this module only — exact single-record line shape, multi-record order preservation, round-trip identity via a hand-built record stub (no parser import), and verbatim message-with-spaces preservation.
- Docstrings must agree with implementation (behavior self-consistency).

## What I did
- Created `log_format.py` with two public functions, both documented:
  - `format_record(record) -> str` — renders one record as `YYYY-MM-DD HH:MM:SS LEVEL message` from `record.timestamp` (must be a `datetime.datetime`, else `TypeError`), `record.level`, `record.message`; message preserved verbatim; raises `AttributeError` if an attribute is missing; no trailing newline.
  - `format_records(records) -> list` — list comprehension over the iterable, preserving order exactly, delegating each item to `format_record`.
- Created `tests/test_log_format.py` (unittest style, stdlib only) with a local `Record` stub class (`timestamp`/`level`/`message`) and 4 tests across two classes:
  - `test_single_record_matches_uniform_line_shape`
  - `test_message_with_spaces_preserved_verbatim`
  - `test_round_trip_identity` (parses a well-formed line into the stub, formats it back, asserts equality)
  - `test_multi_record_formatting_preserves_order`

## What I did NOT do
- Did not create or touch the parser, filter, or statistics modules (owned by other cards); `log_format.py` does not import any of them.
- Did not add any other module, package directory, or CLI.
- Did not modify `legacy_stringkit.py`, `tests/test_legacy_stringkit.py`, `README.md`, `worker-prompt.txt`, `worker-stream.jsonl`, or any file outside my two deliverables plus this handoff and the status file.
- Did not commit or push.

## Checks run
From the repository root, exactly the card's check command:

```
python -m unittest discover -s tests -p "test_log_format.py" -v
```

Result: **OK — 4 tests ran, all passed** (exit code 0):
- `test_message_with_spaces_preserved_verbatim ... ok`
- `test_round_trip_identity ... ok`
- `test_single_record_matches_uniform_line_shape ... ok`
- `test_multi_record_formatting_preserves_order ... ok`

I did not run the full-repository suite (other cards' modules may not exist yet in my working tree); the card scoped my check to this one test file.

## Notes for the validator
- Format contract: single space separators between date, time, level, and message; timestamp rendered as `%Y-%m-%d %H:%M:%S` (second precision, matching the parse format); message is everything after the third space and is never rewritten, so messages containing spaces (including runs of spaces) round-trip exactly.
- `format_record` validates only that `record.timestamp` is a `datetime` instance; it deliberately does not restrict `level` values (level validation belongs to the parser card). Docstrings state this exception behavior explicitly — implementation and docstrings agree.
- Tests import only `log_format` and the stdlib; the record stub is defined inside the test file, so this test file does not depend on the parser module existing.
- Round-trip identity is guaranteed for well-formed lines of the one supported format: `line -> (split into date/time/level/message) -> stub -> format_record == line`.
