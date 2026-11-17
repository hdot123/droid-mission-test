# Handoff: glob-match (sub-issue #70)

## What was requested
Process card `glob-match` for work order #66 (领班制 v2.6.2, 第十四轮): implement exactly two files.

- `glob_match.py` in the repository root (no package directory, no CLI), exposing `match(pattern, name)` implementing a Unix wildcard subset:
  - `*` matches any character sequence including empty
  - `?` matches exactly one character
  - `[seq]` character class with ranges (e.g. `a-c`)
  - `[!seq]` negated character class
  - all other characters match literally
  - case-sensitive matching
  - empty pattern matches only the empty string
  - unclosed `[` raises `ValueError`
  - Required examples: `match("*.py", "a.py")` → True, `match("*.py", "a.pyc")` → False, `match("a?c", "abc")` → True, `match("[!a-c]x", "dx")` → True, `match("[!a-c]x", "bx")` → False
- `tests/test_glob_match.py` covering every rule, all five examples, case sensitivity, empty pattern/name combinations, character classes with ranges and negation, and the `ValueError` for unclosed `[`. The test file must only test `glob_match`.
- Constraints: Python standard library only; must not import `ini_parse` or `urlencode`.
- Then write `team/handoffs/glob-match.md` (this file) and `team/status/glob-match.json`.

## What I did
- Created `glob_match.py`:
  - Tokenizer parses `*`, `?`, and `[...]` classes (with optional leading `!`, ranges, literal `-` just before `]`), raising `ValueError` with a message containing the position of an unclosed `[`.
  - Matching uses an iterative position-set algorithm: `*` advances to every reachable position, other tokens advance exactly one consumed character. Case-sensitive comparison; result is True iff the full name length is reachable after all tokens.
  - Only public function is `match(pattern, name)`; no package, no CLI, no imports of other repo modules.
- Created `tests/test_glob_match.py`: 40 tests covering the five required examples, literals, `*` (including empty-sequence and full-name cases), `?` (exactly-one semantics), classes (membership, ranges, multiple ranges, negation, literal trailing `-`, classes under `*`), case sensitivity (literal, star pattern, class), empty pattern/name combinations, and four unclosed-`[` `ValueError` cases. Imports only `pytest` and `glob_match`.
- One iteration: the first test run failed because I wrote an incorrect expectation (`match("a*b*c", "ac")` should be False, since the pattern contains a literal `b`). The implementation was correct; I corrected the test expectation and reran. No implementation defect was found.

## What I did not do
- Did not create or modify `ini_parse.py`, `urlencode.py`, their tests, or any other repository file.
- Did not create a package directory or CLI.
- Did not commit or push.
- Did not run the full-repo `python -m pytest -q` (owned by the wider workflow); only this process's own check was run, per the process card.

## Checks ran and results
From the repository root:

```
$ python -m pytest -q tests/test_glob_match.py
........................................                                 [100%]
40 passed in 0.04s
```

Exit code 0. (pytest was not preinstalled in the environment; it was installed via `python -m pip install pytest -q` before running — an environment setup step, not a repository change.)

## Notes for the validator
- `tests/test_glob_match.py` is the only test file I touched; it imports only `glob_match`.
- Behavior matches the spec, including: `[a-]` treats the trailing `-` as a literal member; a range with reversed bounds is normalized; `*` never matches across a required prefix/suffix mismatch because matching is full-string (anchored at both ends).
- Expected final state: `state: "done"`, files `["glob_match.py", "tests/test_glob_match.py"]`, check `python -m pytest -q tests/test_glob_match.py` → 40 passed.
