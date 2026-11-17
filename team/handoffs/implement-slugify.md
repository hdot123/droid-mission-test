# Handoff: implement-slugify (sub-issue #80)

## What was requested
Process card `implement-slugify` under work order #77 (三个文本工具模块 · 第十六轮):
- Create `slugify.py` at the repository root with a single function `slugify(text)` implementing this ordered pipeline:
  1. lowercase the text;
  2. replace spaces and underscores with hyphens;
  3. delete every remaining character that is not a letter, digit, or hyphen;
  4. collapse runs of consecutive hyphens into one;
  5. strip leading and trailing hyphens.
- Required exact examples: `slugify("Hello World!") == "hello-world"`; `slugify("a__b  c") == "a-b-c"`; `slugify("--Hi--") == "hi"`.
- Write `test_slugify.py` with pytest cases covering all three examples plus extras (empty string, only punctuation, unicode/punctuation-heavy input, digits, repeated spaces).
- Keep `slugify.py` stdlib-only and independent of the other modules.
- Run `python -m pytest test_slugify.py -q` from the repository root and make it pass.

## What I did
- Created `slugify.py` (stdlib only, uses `re`) with the five-step pipeline in the required order.
- Created `test_slugify.py` with 11 test cases: the three required examples, empty string, only punctuation, unicode/punctuation-heavy input (`"Café — Déjà Vu!"`, `"a @ b # c $ d"`), digits (`"Version 2.0 Release!"`, `"42"`), repeated spaces, mixed case + underscores, only hyphens, and mixed spaces/underscores.
- Installed `pytest` (it was not present in the environment) and ran the check.

## What I did not do
- Did not create or modify `cipher.py`, `string.py`, or any other process's files.
- Did not commit or push anything.
- Did not touch any files outside my scope (`slugify.py`, `test_slugify.py`, and these team files).

## Checks run and results
- `python -m pytest test_slugify.py -q` → **11 passed in 0.02s** (exit code 0).

## Notes for the validator
- `slugify.py` deliberately uses only `re` from the stdlib; it does not import from `cipher.py`, `string.py`, or any other local module, so it cannot be affected by other processes' work.
- Note that the repository will also contain a root-level `string.py` (owned by another process) shadowing the stdlib `string` module; `slugify.py` does not depend on `string` at all, so this shadowing has no effect on slugify.
- The unicode test expectation `"Café — Déjà Vu!" → "caf-dj-vu"` follows step 3 literally: non-ASCII letters such as `é`/`à` are deleted (the spec says "letters" via the alphanumeric/hyphen filter, and the pipeline deletes anything not a letter, digit, or hyphen — implemented as ASCII `[a-z0-9-]` after lowercasing, matching the ASCII-oriented examples). If the validator expects full Unicode letter retention, that would be a spec interpretation difference to flag.
- All three required examples are asserted verbatim in `test_hello_world`, `test_underscores_and_repeated_spaces`, and `test_leading_trailing_hyphens`.
