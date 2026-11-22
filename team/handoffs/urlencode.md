# Handoff: urlencode (sub-issue #69)

## What was requested
Implement `urlencode.py` in the repository root (no package dir, no CLI) with exactly four functions, plus `tests/test_urlencode.py`:

- `quote(s, safe="/")` — percent-encode: UTF-8 bytes, uppercase hex, unreserved chars `A–Z a–z 0–9 -_.~` and chars in `safe` stay literal, space becomes `%20`. Required: `quote("a b/中") == "a%20b/%E4%B8%AD"`.
- `unquote(s)` — `%XX` sequences become bytes, assembled result decoded as UTF-8; invalid percent sequences (`%zz`, trailing `%`) kept literally; valid `%XX` bytes failing UTF-8 decode raise `ValueError`. Required: `unquote("a%20b%zz") == "a b%zz"`.
- `quote_plus(s)` — form encoding: space → `+`, `safe` defaults to `""`. Required: `quote_plus("a b") == "a+b"`.
- `unquote_plus(s)` — replace `+` with spaces, then apply `unquote`. Required: `unquote_plus("a+b") == "a b"`.

Constraints: Python standard library only; must not import `ini_parse` or `glob_match`; tests cover only `urlencode`.

## What I did
- Created `urlencode.py` with the four functions. `quote` builds from `s.encode("utf-8")`, uses a frozenset of unreserved ASCII bytes plus the `safe` bytes, and emits `%%%02X`. `unquote` scans char-by-char, consumes well-formed `%XX` pairs into a `bytearray`, copies everything else (including malformed `%` runs and trailing `%`) as UTF-8 literal bytes, then decodes the whole buffer as UTF-8, converting `UnicodeDecodeError` to `ValueError`. `quote_plus` is `quote(s, safe="")` with `%20` → `+`; `unquote_plus` is `unquote(s.replace("+", " "))`.
- Created `tests/test_urlencode.py` with 25 tests across four test classes covering: every required example, multi-byte UTF-8 (BMP `é`/`中` and astral `😀`), invalid percent sequences (`%zz`, `50%`, `%a`, mixed valid/invalid), empty strings, custom `safe` values (including the fact that a custom `safe` replaces the default `/` rather than adding to it), the `ValueError` path (`%FF`, `a%E0%A4`), and `quote_plus`/`unquote_plus` round trips.

Two implementation bugs were found and fixed during the run, and one test expectation was corrected:
1. The first `quote_plus` implementation replaced spaces with `+` *before* encoding, so the `+` itself was encoded to `%2B`. Fixed by encoding first, then replacing `%20` with `+`.
2. My initial `test_custom_safe` expected `safe="?"` to keep `/` as well; the spec says `safe` holds the characters to leave unencoded (default `"/"`), so a custom `safe` replaces the default. Test corrected to `quote("a/b?c", safe="?") == "a%2Fb?c"` and added `safe="/?"` to show the additive case.

## What I did not do
- Did not create or touch `ini_parse.py`, `glob_match.py`, or any other repository file.
- Did not add a CLI, package directory, or any non-standard-library dependency (pytest was installed into the environment to run the required check; it is not imported by the module).
- Did not commit or push.

## Checks run (from repository root)
1. `python -m pytest -q tests/test_urlencode.py`
   - First run: `4 failed, 21 passed` (the two bugs above plus the test expectation).
   - After fixes: `......................... [100%]` / `25 passed in 0.04s` (exit 0).
2. Spec-example script (`python -c` asserting all four required examples) → `spec examples OK` (exit 0).

Note: `pytest` was not present initially (`No module named pytest`); installed with `pip install pytest` (pytest 9.2.0).

## What the validator must pay attention to
- The process check is exactly `python -m pytest -q tests/test_urlencode.py`; it passes with `25 passed`.
- The spec's required examples are asserted verbatim in the test file and were re-verified in a separate script.
- `unquote` keeps malformed percent sequences literally (byte-wise) while only *valid* `%XX` bytes go through UTF-8 decoding; a valid `%XX` run that decodes to invalid UTF-8 raises `ValueError` as specified.
- Custom `safe` in `quote` replaces the default `/` (spec: "leave ... any character in safe unencoded", default `safe="/"`) — do not "fix" it to be additive.
