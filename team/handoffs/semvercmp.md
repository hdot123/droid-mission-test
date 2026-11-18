# Handoff: semvercmp (sub-issue #303)

## What was requested
Implement `semvercmp.py` with `compare(a: str, b: str) -> int` for the round-36 foreman work order (#299), plus `tests/test_semvercmp.py`. Scope was strictly the two deliverable files; no other process files, no touching existing files, no cross-module imports.

Spec (verbatim from the card):
- Version format is exactly three non-negative integer segments separated by `.`; leading zeros allowed and compared numerically; returns `-1` / `0` / `1`.
- Malformed input (wrong segment count, non-digit, minus sign, empty string) raises `ValueError`.
- Pre-release/build suffixes are not handled: any `-` or `+` makes the format invalid and raises `ValueError`.

## What I did
- Created `semvercmp.py`: a module docstring, `__all__ = ["compare"]`, a private `_parse()` helper that rejects non-strings, any `-`/`+`, wrong segment count, empty segments, and non-digit segments (using `str.isdigit()`), returning a tuple of three ints; and `compare()` which parses both sides and returns `-1`/`0`/`1` via tuple ordering. Standard library only, zero imports from other deliverable modules.
- Created `tests/test_semvercmp.py`: 13 test functions, each a single acceptance requirement. Covers every acceptance example from the card plus the explicit error categories the spec names.

Test coverage map (acceptance examples):
- `compare("1.2.3", "1.2.10") == -1` → `test_numerical_not_lexical`
- `compare("2.0.0", "1.999.999") == 1` → `test_major_bump_wins`
- `compare("1.02.3", "1.2.3") == 0` → `test_leading_zeros_allowed`
- `compare("0.0.9", "0.0.10") == -1` → `test_patch_numerical_order`
- `compare("1.2", "1.2.0")` raises → `test_segment_count_mismatch_raises`
- `compare("1.2.3-alpha", "1.2.3")` raises → `test_prerelease_suffix_raises`

Extra coverage beyond the card: equal versions, `+build` suffix, negative segment, non-digit segment, empty segment, empty string, extra (4th) segment.

## What I did NOT do
- Did not touch any pre-existing file (`roman.py`, `legacy_stringkit.py`, `README.md`, existing tests, or anything else).
- Did not implement `base64url` or `isbn10` (owned by sibling process cards).
- Did not import from, or add, any other deliverable module.
- Did not commit or push (workflow owns that).
- Did not add `team/` content other than my own two required files.

## Checks run and results
Environment note: `pytest` was not installed in the runner image, so I installed it with `python3 -m pip install --user --break-system-packages pytest` (installed pytest 9.2.0). This touched only the user site-packages, not the repo.

1. `python3 -m pytest tests/test_semvercmp.py -q` → exit 0, `13 passed in 0.02s`
2. `python3 -m pytest tests/ -q` → exit 0, `24 passed in 0.03s` (13 mine + 11 pre-existing baseline tests, all green)

## What the validator must pay attention to
- `str.isdigit()` returns `True` for some non-ASCII digits (e.g. superscript `²`). This means `compare("1.2.³", ...)` would parse `³` as an int rather than raising. This is out of the card's stated scope (the spec says "non-digit" without an ASCII restriction) and no acceptance example covers it, so I left it as-is. If the validator wants strict ASCII-only digits, the fix is to check each char against `"0123456789"` instead of `isdigit()` — a one-line change in `_parse`.
- Pre-release/build detection is a substring check for `-`/`+` anywhere, per the card's wording ("any '-' or '+' makes the format invalid"). Note this also rejects a hypothetical negative number like `-1.2.3`, which is consistent with the "minus sign" rejection rule.
- `compare()` raises `ValueError` for both malformed arguments; it never returns anything other than `-1`, `0`, or `1`.
- Only two repo files were added: `semvercmp.py` and `tests/test_semvercmp.py`.
