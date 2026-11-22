# Handoff: morse-module (sub-issue #14)

## What was requested
- Implement `morse.py` at repo root, Python standard library only:
  - `encode(text)`: encode English letters (case-insensitive) and digits to Morse code; character codes separated by a single space, words separated by ` / `. Examples: `encode("SOS") == "... --- ..."`, `encode("A B") == ".- / -..."`.
  - `decode(code)`: reverse mapping; returns uppercase letters and digits joined by single spaces, e.g. `decode("... --- ...") == "SOS"`.
  - `encode` raises `ValueError` on any character that is not a letter/digit/space; `decode` raises `ValueError` on any unknown code group.
- Write `tests/test_morse.py` covering only morse behavior: mixed case letters, digits, word separator, given examples, empty strings, both `ValueError` cases.
- Also write `team/handoffs/morse-module.md` and `team/status/morse-module.json`.
- Constraints: no package directory, no CLI, no import of `brackets`/`wordfreq`, do not edit other processes' files, no commit/push.

## What I did
- Created `morse.py` with a full A-Z / 0-9 Morse table (built bidirectionally from one source dict) and `encode`/`decode` per spec.
  - `encode` splits words on the literal space character; non-space whitespace (tab/newline) and any non-letter/digit char raise `ValueError`; runs of multiple spaces are tolerated (only allowed characters present).
  - `decode` splits on `/`, then whitespace; any token not in the table (or an empty word between separators) raises `ValueError`.
  - Empty input round-trips to `""` in both directions.
- Created `tests/test_morse.py` with 12 tests: given examples, case-insensitivity, digits, empty strings, round trip, and both error classes.

## What I did NOT do
- Did not touch `brackets.py`, `wordfreq.py`, their tests, or any other repo file.
- Did not create a package directory, CLI, or cross-module imports.
- Did not commit or push (left for the workflow).

## Checks run and results
- `python -m pytest -q tests/test_morse.py` → **12 passed** (exit 0).
- Note: pytest was not preinstalled; I installed it with `python -m pip install --user pytest` (pytest 9.2.0) so the check could run. The workflow's prep stage is expected to do the deterministic install with hash pinning; no source files depend on this.

## Things the validator must pay attention to
- Spec ambiguity resolved: "遇到字母数字与空格之外的字符抛 ValueError" means only characters other than letter/digit/space raise; consecutive spaces therefore do **not** raise (space is an allowed character), but `\t`/`\n` and punctuation do.
- `decode("")` and `decode("   ")` return `""` (treated as empty input, not an unknown group).
- Round-trip property holds: `decode(encode(x)) == x.upper()` for inputs of letters/digits/single spaces.
- Two earlier test iterations failed on **my test data** (I had used valid Morse groups as "unknown" examples); the fixture strings were corrected, module code was never the failure cause.
