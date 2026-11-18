# Handoff: wordwrap-module (sub-issue #325)

## What was requested
Process card `wordwrap-module` for work order #315 (第三十八轮 · 并发 D 单): create exactly two new files, `wordwrap.py` and `tests/test_wordwrap.py`, implementing `wrap(text: str, width: int) -> list[str]` — greedy word wrapping split on whitespace (runs of whitespace = one separator), one space between words per line, line length ≤ width, an over-long word gets its own line untruncated, empty/all-whitespace input returns `[]`, `width < 1` raises `ValueError`. Standard library only; must not import csvfield/slugify; every acceptance example covered by a test.

## What I did
- Created `wordwrap.py` with `wrap()`:
  - `width < 1` → `ValueError` (checked before anything else).
  - `text.split()` handles both requirements at once: splits on any whitespace and collapses consecutive whitespace runs to a single separator; empty/all-whitespace input yields `[]` via the `not words` early return.
  - Greedy fill: start a line with the first word, append the next word when `len(current) + 1 + len(word) <= width`, otherwise close the line and start a new one with that word. A word longer than `width` never satisfies the fit test, so it becomes its own line and is never truncated. Final line is appended at the end.
  - Only stdlib (none needed beyond builtins); no imports of csvfield or slugify.
- Created `tests/test_wordwrap.py` with 9 test functions covering:
  - All five acceptance examples verbatim: `wrap("the quick brown fox", 10) == ["the quick", "brown fox"]`; `wrap("", 10) == []`; `wrap("hello", 10) == ["hello"]`; `wrap("a verylongword here", 5) == ["a", "verylongword", "here"]`; `wrap("x", 0)` raises `ValueError`.
  - Negative width (`wrap("x", -3)`) also raises `ValueError`.
  - Full-whitespace input (`"   "`, `"\t\n  \r\n"`) returns `[]`.
  - Consecutive whitespace acts as a single separator (`"a  \t\n   b"` with a tight width collapses to one space, `"one    two"` with width 6 splits to `["one", "two"]`).
  - Property-style check: for widths 1–19, any line longer than `width` must be a single unbroken word (no spaces in it), i.e. only the over-long-word rule may exceed the width.

## What I did not do
- Did not touch any existing file (`README.md`, `legacy_stringkit.py`, `roman.py`, existing tests, etc.).
- Did not create or edit `csvfield.py`, `slugify.py`, or their tests (owned by other processes).
- Did not create or edit anything else in `team/` besides my two assigned files.
- Did not commit or push.
- Did not add third-party dependencies; the environment lacked pytest, so I ran `python3 -m pip install pytest` (pytest 9.2.0) to be able to run the mandated checks. This does not add any project file or dependency.

## Checks run and results
From repository root:
- `python3 -m pytest tests/test_wordwrap.py -q` → **9 passed**.
- `python3 -m pytest tests/ -q` → **20 passed** (9 mine + 11 pre-existing baseline tests).

Note: the first run of both checks failed because one of my own test expectations was wrong (`wrap("a  \t\n   b", 10)` correctly returns `["a b"]` since the words fit at width 10). I fixed the test (not the implementation) to assert whitespace collapsing at a width where it matters; both checks then passed as shown above. The `wordwrap.py` implementation was not changed after that.

## What the validator must pay attention to
- The spec's acceptance example `wrap("the quick brown fox", 10)` implies greedy filling where a word is added only if the *resulting* line (with one space) fits — my implementation matches this; do not "fix" it to fit the raw cumulative width.
- Over-long words: line may exceed `width` only when it is a single word, untruncated; all other lines are ≤ `width`.
- Empty/all-whitespace input returns `[]`, not `[""]`.
- `width < 1` (including negative) raises `ValueError` before any other processing.
- Only two files were added by this process: `wordwrap.py`, `tests/test_wordwrap.py` (plus `team/handoffs/wordwrap-module.md` and `team/status/wordwrap-module.json`). No existing file was modified; nothing was committed.
