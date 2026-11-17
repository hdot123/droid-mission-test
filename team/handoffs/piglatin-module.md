# Handoff: piglatin-module (sub-issue #39)

## What was requested
Implement `piglatin.py` with `translate(word)` and `translate_sentence(s)` per work order #36 / process card #39:
- Input treated as lowercase, output always lowercase.
- Vowel start (a/e/i/o/u): append `"way"` (`translate("apple") == "appleway"`).
- Consonant start: move the entire leading consonant cluster to the end and add `"ay"` (`translate("string") == "ingstray"`, `translate("cat") == "atcay"`).
- Empty string returns `""`.
- `translate_sentence(s)` splits on single spaces, translates each word, joins with a single space (`translate_sentence("hello world") == "ellohay orldway"`).
- Standard library only, no package directory, no CLI, plus `tests/test_piglatin.py`.

## What I did
- Created `piglatin.py` with `translate` and `translate_sentence` implementing the spec exactly (lowercasing inside `translate`, cluster scan over non-vowels, split on single space `" "`).
- Created `tests/test_piglatin.py` covering: all four spec examples, vowel starts (`elephant`, `orange`, `igloo`), consonant clusters (`strong`, `chair`, `three`, `rhythm`), mixed-case inputs (`Apple`, `String`, `CAT`, `HeLLo`), single-letter words (`a` → `away`, `b` → `bay`), and empty string / empty sentence / single-word sentence.

## What I did NOT do
- Did not touch `b64url.py`, `collatz.py`, or any other module/test files.
- Did not create package directories, CLI entry points, or any imports between modules.
- Did not commit or push.

## Checks run and results
1. `python -m pytest -q tests/test_piglatin.py` → **10 passed in 0.02s**
2. `python -c "from piglatin import translate, translate_sentence; assert translate('apple')=='appleway'; ... assert translate_sentence('hello world')=='ellohay orldway'"` → **passed** (`checks passed`)

Note: `pytest` was not present in the environment; I installed it with `python3 -m pip install pytest` (pytest 9.2.0) to run the checks.

## What the validator must pay attention to
- `translate_sentence` splits on the single space character (`s.split(" ")`), per the spec's "以空格分隔" wording, not `str.split()` with arbitrary whitespace. Multi-space input therefore yields empty tokens that map to empty strings, which the join preserves.
- `translate` lowercases its input internally, so mixed-case input behaves as lowercase; tests assert this.
- `translate("rhythm")` → `"rhythmay"`: `y` is not treated as a vowel, so `rhythm` contains no vowels at all. The cluster scan runs to the end of the word, the whole word moves, and the result is `rhythm` + `ay`. The test asserts `translate("rhythm") == "rhythmay"` and passes; validator should not "fix" this to a different value.
- Repo-root acceptance (`python -m pytest -q` for all three modules) is owned by the foreman/validator; this worker only ran the scoped `tests/test_piglatin.py`.
