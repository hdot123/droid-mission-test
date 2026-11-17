# Handoff: hexcolor (sub-issue #99)

## What was requested
Process card #99 for the hexcolor 十六进制颜色模块 (work order #95, 领班制 v2.6.4 round):

- Own only `hexcolor.py` and `tests/test_hexcolor.py`.
- Implement `parse(s)`, `to_hex(r, g, b)`, `is_valid(s)`:
  - `parse(s)` accepts `"#RGB"` or `"#RRGGBB"` (case-insensitive), returns an `(r, g, b)` int tuple; short form expands each digit by doubling; invalid format (missing `#`, wrong length, non-hex chars) raises `ValueError`.
  - `to_hex(r, g, b)` returns uppercase `"#RRGGBB"`; components must be `int` in 0–255, else `ValueError`.
  - `is_valid(s)` is the boolean version and never raises.
- Hard requirements written verbatim into tests/checks: `parse("#f80")` → `(255, 136, 0)`, `parse("#FF8800")` → `(255, 136, 0)`, `to_hex(255, 136, 0)` → `"#FF8800"`.
- Constraints: Python standard library only; no imports of wordscore/caesar; no package directory; no CLI.
- Checks come verbatim from this card's checks column; status/handoff aligned item-by-item to actual execution evidence.

## What I did
- Created `hexcolor.py` with the three functions matching the spec and signatures: `parse(s)`, `to_hex(r, g, b)`, `is_valid(s)`.
- Created `tests/test_hexcolor.py` covering only this module: the three required examples verbatim, case-insensitivity, short-form doubling, missing `#` / wrong length / non-hex `ValueError` cases, `to_hex` roundtrip, `to_hex` range/type `ValueError` cases (including `bool` and `float` rejection), and `is_valid` true/false/never-raises behavior.
- Installed `pytest` (was not present in the environment: `/usr/bin/python: No module named pytest`) to be able to run the checks. This is an environment tool install, not a repo change.
- Ran the four card checks verbatim; all pass (see below).
- Wrote `team/handoffs/hexcolor.md` and `team/status/hexcolor.json`.

## What I did not do
- Did not touch `wordscore.py`, `caesar.py`, or any other process's tests/files.
- Did not commit or push (left to the workflow).
- Did not modify the wordscore spec contradiction (`score("abc")` 6 vs 7); that belongs to the wordscore process, not this card.

## Checks run and results
All four commands executed verbatim from the card's checks column, at repo root:

1. `python -m pytest -q tests/test_hexcolor.py` → **PASS** (exit 0): `14 passed`.
2. `python -m pytest -q` → **PASS** (exit 0): `14 passed`.
3. `python -c "from hexcolor import parse, to_hex, is_valid; assert parse('#f80') == (255, 136, 0); assert parse('#FF8800') == (255, 136, 0); assert to_hex(255, 136, 0) == '#FF8800'; assert is_valid('#f80') is True; assert is_valid('f80') is False; print('hexcolor examples ok')"` → **PASS** (exit 0): printed `hexcolor examples ok`.
4. `python -c "import hexcolor, inspect; print(inspect.signature(hexcolor.parse)); print(inspect.signature(hexcolor.to_hex)); print(inspect.signature(hexcolor.is_valid))"` → **PASS** (exit 0): printed `(s)`, `(r, g, b)`, `(s)`.

## What the validator must pay attention to
- Check 2 (`python -m pytest -q`) currently passes with 14 tests, all mine. If other processes (wordscore, caesar) add tests, a failure there would be theirs, not hexcolor's; my module's own check is check 1.
- `pytest` was missing and I installed it via pip; if the validator's environment is fresh, it may need the same install before the checks can run.
- Signatures are exactly `(s)`, `(r, g, b)`, `(s)` as required.
- The three required examples are asserted verbatim in `tests/test_hexcolor.py` (`test_parse_short_form_example`, `test_parse_long_form_example`, `test_to_hex_example`).
- `is_valid` catches all exceptions (including non-string input like `None`/`123`) and returns `False` without raising, per "布尔版，不抛错".
- State: `done`; files: `hexcolor.py`, `tests/test_hexcolor.py`, plus this handoff and `team/status/hexcolor.json`.
