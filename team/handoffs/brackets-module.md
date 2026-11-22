# Handoff: brackets-module (sub-issue #15)

## What was requested
Implement `brackets.py` with `is_balanced(text)` in the repo root (Python standard library only):
- Checks whether `()`, `[]`, `{}` are correctly paired and nested.
- Content inside single or double quotes is ignored entirely (brackets inside quotes never count).
- A quote is closed only by the same kind of quote; if a quote is never closed, everything after it is treated as inside the quote.
- Non-bracket characters outside quotes are ignored.
- Empty string returns `True`.
Plus `tests/test_brackets.py` covering: correct nesting, mismatched/reversed pairs, brackets ignored inside single and double quotes, multiline/multiple quoted regions, unclosed quote swallowing the rest, non-bracket characters outside quotes ignored, empty string. No package directory, no CLI, no importing the other two modules, no editing other files.

## What I did
- Created `brackets.py`: a stack-based scanner with a quote-state variable. Inside a quote only the matching same-kind quote ends the quote; brackets are never touched. Outside quotes, open brackets push, a closer pops only if it matches the top of the stack (mismatch/empty stack → `False`), and any other character is ignored. Unclosed quote at end of text simply leaves quote state active (rest swallowed); leftover stack entries make the result `False`.
- Created `tests/test_brackets.py` with 11 tests using only `from brackets import is_balanced`, covering every scenario listed in the card.

## What I did NOT do
- Did not create `morse.py`, `wordfreq.py`, or their tests (owned by other process cards).
- Did not create a package directory, no CLI, no cross-module imports.
- Did not edit any file outside `brackets.py`, `tests/test_brackets.py`, and my two team files.
- Did not commit or push.
- Did not create a conftest.py or modify pytest configuration; plain root-level `python -m pytest` picks up `brackets.py` because tests run with the repo root on `sys.path`.

## Checks I ran and results
- `python -m pytest -q tests/test_brackets.py` → `11 passed in 0.01s` (exit 0).
- Environment note: pytest was not installed at session start; I installed it with `pip3 install pytest` (pytest 9.2.0) to run the check. If the workflow's prep step reinstalls it, that is harmless/idempotent.

## Things the validator must pay attention to
1. Quote semantics are "same kind closes"; a `'` inside a `"..."` region does not close it (tested in `test_cross_quote_kind_does_not_close`).
2. `is_balanced("('")` is `False`: the `(` opened *before* the unclosed quote still counts; the quote only swallows what follows it. `is_balanced("'(")` is `True` because the `(` is inside the swallowed region. Both directions are tested.
3. Quotes inside quotes of a different kind do not nest and do not terminate the outer region (e.g. `"it's ("` → `True`).
4. Two of my initial test expectations were wrong about rule 2; I corrected the *tests* to match the spec, not the implementation. The implementation has not changed since it was written.
5. Only this card's two source files plus `team/handoffs/brackets-module.md` and `team/status/brackets-module.json` were touched.
