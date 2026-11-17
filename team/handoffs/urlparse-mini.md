# Handoff: urlparse-mini (sub-issue #55)

## What was requested
Implement `urlparse_mini.py` exposing `parse(url)` that splits a simple http/https URL into a dict with keys `scheme`, `host`, `port`, `path`, `query`, plus `tests/test_urlparse_mini.py`. Rules:

- Default port: 80 for http, 443 for https; explicit port in URL overrides.
- Path defaults to `"/"` when absent.
- Query is the raw query string without the leading `"?"`, defaulting to `""`.
- Any url containing `"@"` or `"#"` raises `ValueError` (no userinfo/fragments).
- Scheme not http/https, or empty host, raises `ValueError`.
- Only the Python standard library; no imports of the other two modules; no package directory, no CLI.
- Scope: only `urlparse_mini.py` and `tests/test_urlparse_mini.py` (plus these team files).

## What I did
- Created `urlparse_mini.py` with `parse(url)` implementing all rules above, including rejection of a missing scheme and malformed ports (both `ValueError`).
- Created `tests/test_urlparse_mini.py` with 15 tests covering: both spec examples, default ports for http/https, explicit port override, missing path → `"/"`, trailing-slash path preserved, empty query default, query without path, raw query string, and each `ValueError` case (`@`, `#`, bad scheme, missing scheme, empty host).

## What I did not do
- Did not touch `temperature.py`, `stack.py`, any other test file, or shared config.
- Did not add a CLI, package directory, or any cross-module imports.
- Did not commit or push.

## Checks run and results
1. `python -m pytest -q tests/test_urlparse_mini.py` → `15 passed in 0.02s` (exit 0).
2. `python -c "from urlparse_mini import parse; assert parse('https://example.com/a/b?x=1') == {...}; assert parse('http://h.io:8080') == {...}; print('ok')"` → `ok`.

Note: pytest was not preinstalled in this environment; I installed it via `python -m pip install pytest` (pytest 9.2.0) so the required check could run. This is an environment setup step, not a repository change.

## For the validator
- Behavior matches the spec examples exactly; port and path defaults verified by tests.
- `parse` also rejects a URL with no `scheme://` prefix (e.g. `parse("example.com/path")`) with `ValueError` — this is stricter than the letter of the spec but consistent with "invalid URL".
- Port parsing is strict: a non-numeric port raises `ValueError`.
- Only the two owned files plus the two team files were created/modified.
