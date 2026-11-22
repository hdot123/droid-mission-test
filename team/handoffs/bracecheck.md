# Handoff: bracecheck (sub-issue #273, process card `bracecheck`)

## What was requested

Implement the bracket-balancing utility of work order #269 (round 34), scoped to this process card only:

- `bracecheck.py` exposing `is_balanced(text)` that decides whether round parentheses, square brackets, and braces in the text are correctly paired and nested, ignoring all non-bracket characters.
- `tests/test_bracecheck.py` asserting the four acceptance examples verbatim plus nesting/error cases consistent with the spec.
- Constraints: Python standard library only; no package directory, no CLI; `bracecheck.py` must NOT import `codecbox`, `codec_rle`, or `codec_flip` (no dependency on the codec directory at all); `tests/test_bracecheck.py` must test only `bracecheck`'s behavior.
- The stock files `codecbox.py` and `tests/test_codecbox.py` must remain untouched (存量两文件原样未动).
- 归因禁令: attribute any failure only from in-process evidence (failure output, failing test file, source text). Forbidden: `codecbox.reset()`, `importlib.reload` or any re-import trick, delete-then-re-register, clearing shared state before asserting.

## What I did

- Created `bracecheck.py`: a single public function `is_balanced(text)` backed by two module-level constant tables (`_OPEN_TO_CLOSE`, `_CLOSE_TO_OPEN`). It walks the string once with a stack: openers push their expected closer, closers must match the stack top (empty stack or mismatch returns `False`), non-bracket characters are skipped, and the result is `True` iff the stack is empty at the end. No imports at all, so there is no dependency on the codec directory by construction.
- Created `tests/test_bracecheck.py`: 9 tests covering the four acceptance examples verbatim (`"a(b[c]d)e"` → `True`, `"(]"` → `False`, `""` → `True`, `"((("` → `False`), plus plain-text/empty-string `True` cases, mismatched closers, wrong nesting (`"([)]"`, `"({)}"`, `"[(])"`), unbalanced leftovers (`")"`, `"a(b[c"`, `"((())"`), and correctly nested `True` cases. Imports only `bracecheck`; contains no `reset()`, no `importlib.reload`, no re-import trick, no shared-state manipulation of any kind.

## What I did not do

- Did not touch `codecbox.py`, `tests/test_codecbox.py`, or any other repository file.
- Did not create or modify `codec_rle.py`, `codec_flip.py`, `tests/test_codec_rle.py`, `tests/test_codec_flip.py` (owned by sibling processes).
- Did not add any package directory, CLI, or non-standard-library dependency.
- Did not commit or push anything.

## Checks I ran and results

1. `python -m pytest -q tests/test_bracecheck.py` → `9 passed in 0.02s` (exit code 0).
2. `git diff --exit-code -- codecbox.py tests/test_codecbox.py` → no output, exit code 0 (stock files unmodified).

Environment note: this image shipped without pytest (`python -m pytest` initially failed with `No module named pytest`), so I ran `python3 -m pip install --quiet pytest` (pytest 9.2.0) to make the card's mandated check command executable. This installs a tool into the environment only; it does not modify any repository file.

## What the validator must pay attention to

- The card's check commands must be run verbatim from the repo root: `python -m pytest -q tests/test_bracecheck.py` and `git diff --exit-code -- codecbox.py tests/test_codecbox.py`. Both pass as recorded above.
- My tests assert only `bracecheck` behavior. The 归因禁令 applies: no `reset()`, no `importlib.reload`, no delete-then-re-register, no clearing shared state appears in my test code, so this test file cannot pollute round-34 attribution.
- `bracecheck.py` has zero imports, so it cannot be affected by, nor affect, the codec plugins' import/registration order. Any post-merge failure in `tests/test_codecbox.py`, `tests/test_codec_rle.py`, or `tests/test_codec_flip.py` cannot originate from these two files.
- The stock files `codecbox.py` and `tests/test_codecbox.py` are byte-for-byte unchanged (verified by check 2).
