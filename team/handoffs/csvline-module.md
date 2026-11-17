# Handoff: csvline-module (sub-issue #21)

## What was requested
Implement `csvline.py` at the repository root with two functions, using only the Python standard library, without importing the `csv` module or any other project module:
- `parse(line)` — parse one line of CSV text into `list[str]`. Fields separated by commas; a double-quoted field may contain commas; a doubled double quote `""` inside a quoted field decodes to a single `"`. Example: `parse('a,"b,c","d""e"')` → `['a', 'b,c', 'd"e']`.
- `join(fields)` — inverse generation: wrap a field in double quotes when it contains a comma, double quote, or newline; double any double quotes inside such a quoted field; otherwise emit bare.

Plus `tests/test_csvline.py` covering: the given parse example, simple unquoted fields, quoted fields containing commas, doubled-quote decoding, join quoting rules for comma/quote/newline, and a round-trip check. Each test file tests only this module.

## What I did
- Created `csvline.py` with a hand-written single-pass parser (quote-run state machine) and a `join` generator. No `csv` import, no other imports.
- Created `tests/test_csvline.py` with 11 tests covering all required cases plus unicode and empty-field cases.

## What I did NOT do
- Did not touch `roman.py`, `median.py`, or their tests (other processes own those).
- Did not create package directories, CLI, or any other functions.
- Did not commit or push.

## Checks run
- `python -m pytest -q tests/test_csvline.py` → **11 passed in 0.02s** (exit 0).
- Note: `pytest` was not installed in the environment; I installed it via `pip3 install pytest` (pytest 9.2.0) so the required check could run.

## Things the validator must pay attention to
1. **Known CSV ambiguity**: `join([])` (empty list) and `join([""])` (one empty field) both produce the empty string `""`, and `parse("")` returns `['']` (standard CSV convention: an empty line is one empty field). The round-trip property therefore holds for all field lists *except* the empty list `[]`. I removed `[]` from the round-trip test cases for this reason; the test still covers `[""]` and `["", "empty"]`. If the validator requires literal `parse(join([])) == []`, that conflicts with `parse("") == ['']` and the spec's unquoted-field semantics — it is a spec-level ambiguity, not an implementation bug.
2. `parse` treats any `"` as opening a quoted run (no strict validation of quote position), which matches the spec's examples; malformed-input strictness beyond the given examples was not required by this process card.
3. `join` quoting check order: fields containing `"` are always quoted (a bare quote can never appear unquoted); newline and comma fields are quoted; everything else is bare.
