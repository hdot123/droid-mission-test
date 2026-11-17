# Handoff: nato-module (sub-issue #124)

## What was requested

Process card `nato-module` under work order #121 (第二十三轮 B 单 · v2.6.5 并发重考):

- Create `nato.py` at the repository root implementing `spell(word)`:
  - converts an English word letter by letter to NATO phonetic alphabet names (Alfa, Bravo, Charlie, ...), joined by hyphens;
  - case-insensitive input, output normalized to initial-capital form (Charlie-Alfa-Tango style);
  - raises `ValueError` on any non-letter character;
  - must satisfy `spell("cat") == "Charlie-Alfa-Tango"` and `spell("Go") == "Golf-Oscar"`.
- Create `tests/test_nato.py` testing only `nato.py`: the two worked examples, case-insensitivity, hyphen joining, and `ValueError` on non-letter input.
- Constraints: Python standard library only; no package directory; no CLI; no cross-module imports; do not touch `morse.py`, `luhn.py`, or their tests.

Scope: owns only `nato.py` and `tests/test_nato.py` (plus this handoff and `team/status/nato-module.json`).

## What I did

- Wrote `nato.py` with a module-level tuple of the 26 NATO phonetic names (ICAO spellings: Alfa, Juliett, Xray, etc.) and `spell(word)`:
  - non-`str` input or any non-letter character raises `ValueError`;
  - each letter is uppercased and mapped via `ord(ch) - ord("A")` to its NATO name;
  - names are joined with `"-"`.
- Wrote `tests/test_nato.py` with 10 test cases: both worked examples, case-insensitivity (`CAT`/`cAt` vs `cat`), hyphen-joining checks (count and split on `hello`), and parametrized `ValueError` cases (`"c4t"`, `"hi you"`, `"a-b"`, `""`, `"a!"`, `"cat."`).
- Installed `pytest` into the environment (it was not preinstalled) so the required check could run.

## What I did not do

- Did not create or modify `morse.py`, `luhn.py`, `tests/test_morse.py`, `tests/test_luhn.py`, or any other process's files.
- Did not add any cross-module imports, package directories, or CLI entry points.
- Did not create a package `__init__.py`; `tests/test_nato.py` imports `nato` as a root-level module (rootdir is added to `sys.path` by pytest's rootdir/conftest behavior — verified by the passing run).
- Did not commit or push.

## Checks run and results

Verbatim checks column command from the process card:

```
python -m pytest tests/test_nato.py -q
```

Result: `10 passed in 0.02s` (exit code 0).

## Notes for the validator

- The full-suite command `python -m pytest -q` also passes locally for this module; other processes' tests are executed in parallel by them.
- `pytest 9.2.0` was installed via `pip` during this run because the environment had no pytest module; no project files were changed by that install.
- The spec's two worked examples are asserted directly in `test_worked_example_cat` and `test_worked_example_go`.
