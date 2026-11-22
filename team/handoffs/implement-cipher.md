# Handoff: implement-cipher (sub-issue #79)

## What was requested

Implement `cipher.py` at the repository root with a single function
`shift_text(text, n)`:

- Shift every English letter Caesar-fashion by `n` positions.
- `n` may be negative or exceed 26 in magnitude; reduce with `n % 26`.
- Case is preserved (lowercase stays lowercase, uppercase stays uppercase).
- Non-letter characters pass through unchanged.
- MUST build alphabets from stdlib `string.ascii_lowercase` and
  `string.ascii_uppercase` (no hardcoded letter literals).
- Exact examples that must hold:
  - `shift_text("Abc XyZ!", 2) == "Cde ZaB!"`
  - `shift_text("Hello", -3) == "Ebiil"`
  - `shift_text("Zebra", 26) == "Zebra"`
- Also write `test_cipher.py` covering those three examples plus extra cases
  (`n=0`, `n=27`, mixed punctuation/digits, empty string).
- Guard the import against a root-level `string.py` shadowing the stdlib
  `string` module: try `from string import ...`, on `ImportError` load the
  stdlib `string` via `importlib` from `sysconfig.get_paths()['stdlib']`.
- `cipher.py` must be dependency-free beyond the stdlib.

## What I did

- Created `cipher.py` implementing `shift_text(text, n)` using
  `str.translate` + `str.maketrans` over alphabets sliced by `k = n % 26`.
  Alphabets come exclusively from `ascii_lowercase` / `ascii_uppercase`.
- Added a defensive import with an ImportError fallback that loads the real
  stdlib `string` module by path. The fallback handles three layouts:
  1. the already-imported cached stdlib module (if it has the constants),
  2. `<stdlib>/string.py` (single-file layout),
  3. `<stdlib>/string/__init__.py` (package layout, which is what this
     environment uses — Python 3.14: `/usr/lib/python3.14/string/__init__.py`),
  4. last resort: `importlib.machinery.PathFinder.find_spec("string", clean_path)`
     with `sys.path` entries that contain a shadowing `string.py` filtered out.
- Created `test_cipher.py` with 9 pytest cases: the three required examples
  plus `n=0`, `n=27`, large negative (`-27`), mixed punctuation/digits,
  alphabet-edge case preservation (`XYZ`/`xyz` +3), and empty string.

## What I did NOT do

- Did not create or modify `slugify.py`, `string.py`, or any other process's
  files.
- Did not run the merged/full pytest across all three modules (out of scope
  for this process card).
- Did not commit or push.

## Checks I ran and results

1. `python -m pytest test_cipher.py -q` (from repository root)
   → **9 passed**.
2. Fallback verification: copied `cipher.py` into a temp dir alongside a
   shadowing root-level `string.py` (containing only `reverse_words`,
   `count_vowels`, `title_case`, i.e. no `ascii_lowercase`), ran the three
   required assertions → **rc=0, "fallback ok: abc ABC"**.
   The fallback path works exactly as specified in the work order.

## Things the validator must pay attention to

1. **The required check passes.** `python -m pytest test_cipher.py -q` from
   the repository root reports `9 passed`.

2. **Shadowed-string.py caveat (environment, not my code):** if the
   root-level `string.py` created by the other process does NOT define
   `Template` (or the other constants), then *pytest itself* can fail at
   import time, because stdlib `logging` does `from string import Template`
   and picks up the shadowing file when the test runs with the repo root on
   `sys.path`. This affects any test run from the repo root and is not
   fixable from `cipher.py` (I do not own `string.py`). If the merged full
   pytest fails with
   `ImportError: cannot import name 'Template' from 'string'`, the root cause
   is the shadow file's contents, not `cipher.py`.

3. **Verified behavior of the fallback under that same condition:** loading
   `cipher.py` directly (e.g. `import cipher` in a subprocess) works fine
   even when `string.py` is missing `ascii_lowercase`, because the fallback
   finds the real stdlib module. Only pytest's own import chain is affected.

4. **No hardcoded letters:** the only letter literals in `cipher.py` are
   inside the module docstring/comment. The alphabet constants come from the
   stdlib `string` module as required.

5. Files owned by this process: `cipher.py`, `test_cipher.py`,
   `team/handoffs/implement-cipher.md`, `team/status/implement-cipher.json`.
