# Handoff: unixpath (sub-issue #340)

## What was requested

Process card #340 under work order #337 (第三十九轮 · fractionx／unixpath／money).

Scope owned by this process, verbatim from the card:

- Create `unixpath.py` and `tests/test_unixpath.py` (both new files; do not modify any existing file).
- Implement POSIX path lexical normalization from scratch; `posixpath` and `os.path` must NOT be imported or used anywhere in `unixpath.py`.
- `normalize(path: str) -> str`: purely lexical processing (no filesystem access): collapse consecutive `/`; drop `.` segments; `..` cancels the previous segment (absolute paths stop at the root; relative paths keep leading `..` that cannot be cancelled); drop trailing `/` (except root `/`); empty string returns `.`. Semantics aligned with `posixpath.normpath`.
- Every acceptance point must have a corresponding test case:
  - `normalize("/a/b/../c") == "/a/c"`
  - `normalize("a//b/./c/") == "a/b/c"`
  - `normalize("/../../x") == "/x"`
  - `normalize("a/../../b") == "../b"`
  - `normalize("./") == "."`
  - `normalize("/") == "/"`
  - `normalize("") == "."`
  - `normalize("../a") == "../a"`
- Also cover: repeated `..` beyond the root on absolute paths, relative paths retaining multiple leading `..`, `.` in the middle of a path, and no trailing slash except root.
- Checks (verbatim): `python3 -m pytest tests/test_unixpath.py -q`, `python3 -m pytest tests/ -q`.

## What I did

- Created `unixpath.py` with a single function `normalize(path: str) -> str`. The implementation is a from-scratch lexical algorithm: split on `/`, walk the segments with a stack, drop empty/`.` segments, pop the stack on `..` (with the absolute-root clamp and relative leading-`..` retention rules), then rejoin. No filesystem access; no `posixpath`/`os.path`/`os` imports anywhere in the file (the only textual matches for those names are two docstring comments explaining what is NOT used).
- Created `tests/test_unixpath.py` with 17 test functions: one per acceptance point (8), plus the four remaining stated requirements (repeated `..` beyond root, multiple leading `..` in relative paths, `.` mid-path, no trailing slash except root), plus extra coverage (`a/.. -> "."`, `..` stacking, slash collapsing, `./.` and `./a`, result type is `str`).
- Removed an unused `import pytest` from the test file (no `pytest.raises` cases are needed for this module; the work order specifies no error cases for `normalize`).
- Note on environment: `python3 -m pytest` initially failed with `No module named pytest`. There was no project venv. I installed pytest with `python3 -m pip install --user pytest` (pytest 9.2.0) so the mandated checks could run. No repository files were changed by this.

## What I did not do

- Did not touch `fractionx.py`, `money.py`, any test file other than `tests/test_unixpath.py`, or any existing file.
- Did not import or use `posixpath`, `os.path`, or `os` in `unixpath.py`.
- Did not add or modify any of the other four deliverables of work order #337 (they belong to other processes).
- Did not commit or push anything; workflow owns that.
- Did not add error-raising behavior to `normalize` (the work order specifies none; only the empty-string `-> "."` case exists).

## Checks run and results

Both process checks were run from the repository root, after implementing and after the final edit:

1. `python3 -m pytest tests/test_unixpath.py -q` -> **17 passed in 0.02s** (exit 0)
2. `python3 -m pytest tests/ -q` -> **28 passed in 0.03s** (exit 0)

The full-suite run covers the pre-existing `test_roman.py` and `test_legacy_stringkit.py` as well, confirming no regression to existing files.

Additional verification:

- `grep -nE "posixpath|os\.path|import os|import posixpath" unixpath.py` -> only two docstring comment matches (lines 3 and 9), no import statements (grep exit 0 due to those comment matches; no code match).
- `git status --short` -> only `?? unixpath.py`, `?? tests/test_unixpath.py` (plus pre-existing untracked `worker-prompt.txt`, `worker-stream.jsonl` and `__pycache__/` artifacts). No tracked file modified.

## What the validator must pay attention to

- `normalize` is a module-level function, not a method on a class; there is no `Path` class. The work order for unixpath specifies only `normalize(path: str) -> str`.
- Semantics are aligned with `posixpath.normpath`, so e.g. `normalize("a/..") == "."`, `normalize("a/b/../..") == "."`, `normalize("/a/../../..") == "/"`, `normalize("/") == "/"`, `normalize("") == "."`.
- The empty string is the only input that returns `"."` by special case; otherwise `"."` also arises naturally when a relative path cancels out entirely.
- The test file has no `pytest.raises` usage because the spec defines no exceptions for `normalize`.
- pytest was installed into the user site-packages of the runner environment (`python3 -m pip install --user pytest`) because it was absent; that is an environment change, not a repo change.
