# Validator Report (squad-leader acceptance style)

Judged processes: **ellipse**, **issn**, **pluralize** — all judged from the pre-packed evidence in this directory only. Evidence relied on per process: `packs/<id>/process-card.json`, `handoff.md`, `status.json`, `diff.patch`, `checks-output.txt`, `checks-exit.json` (and the absence of `checks-failed.marker`).

---

## ellipse — PASS

**Evidence relied on:**
- `packs/ellipse/checks-failed.marker`: **absent**.
- `packs/ellipse/checks-exit.json`: both mandated checks exit 0 — `python3 -m pytest tests/test_ellipse.py -q` (exit 0), `python3 -m pytest tests/ -q` (exit 0).
- `packs/ellipse/checks-output.txt`: `27 passed in 0.02s` for the card-scoped run; `256 passed, 2 skipped in 15.28s` for the full suite.
- `packs/ellipse/diff.patch`: new `ellipse.py` implements all three functions with the pinned formulas verbatim — `ellipse_area` = `pi * a * b`; `ellipse_perimeter` = Ramanujan II exactly (`h = ((a-b)/(a+b))**2`, `pi*(a+b)*(1 + 3h/(10+sqrt(4-3h)))`); `ellipse_eccentricity` uses `max/min` so axis swap is symmetric and `a == b` yields `0.0`. Shared `_validate` rejects `bool` (TypeError), non-numeric (TypeError), and `<= 0` (ValueError), as the card requires.
- `packs/ellipse/diff.patch` (tests): a dedicated case for all 19 numeric acceptance values (tolerance `abs < 1e-9`), both ValueError items (`ellipse_area(0, 1)`, `ellipse_perimeter(-2, 1)`), and both TypeError items (`ellipse_area("2", 1)`, `ellipse_eccentricity(2, True)`).
- `packs/ellipse/handoff.md` and `status.json` state `done`, own only `ellipse.py` + `tests/test_ellipse.py` (plus whitelisted `team/**` protocol files), no cross-imports, no modification of pre-existing files — consistent with the card scope.

**Notes:**
- `status.json`/`handoff.md` report "214 passed" for the full suite while `checks-output.txt` shows "256 passed, 2 skipped". Per the rules this pre-merge-report count difference is bookkeeping, not a conflict; the check output is what gates.
- The implementation additionally requires finite values (NaN/inf → ValueError). The card does not specify NaN behavior, so this is an extra strictness beyond the card, not a contradiction; it is tested as an extra case and does not alter any card-mandated behavior.

**Verdict: pass** (card, handoff, status, diff, and check outputs line up; no red mandated check).

---

## issn — PASS

**Evidence relied on:**
- `packs/issn/checks-failed.marker`: **absent**.
- `packs/issn/checks-exit.json`: both mandated checks exit 0 — `python3 -m pytest tests/test_issn.py -q` (exit 0), `python3 -m pytest tests/ -q` (exit 0).
- `packs/issn/checks-output.txt`: `7 passed in 0.01s` for the card-scoped run; `256 passed, 2 skipped in 15.27s` for the full suite.
- `packs/issn/diff.patch`: `issn_check_digit` implements the pinned algorithm (weights 8,7,6,5,4,3,2; `check = (11 - (sum % 11)) % 11`; 10 → "X"), TypeError on non-str, ValueError unless exactly 7 ASCII digits (`isdigit()` + `isascii()`). `issn_validate` handles the 8-char form, the 9-char form requiring `code[4] == '-'`, returns False (no raise) for every malformed shape (wrong length, wrong hyphen position, non-digit first 7, lowercase x or any other final char), and compares the last character against the computed check digit.
- Hand verification of the acceptance values from the pinned formula: "0378595" → 160 % 11 = 6 → "5" ✓; "2049363" → 121 % 11 = 0 → "0" ✓; "1234567" → 112 % 11 = 2 → "9" ✓; "0000000" → "0" ✓; "9999999" → 315 % 11 = 7 → "4" ✓; "1000002" → 12 % 11 = 1 → "X" ✓.
- `packs/issn/diff.patch` (tests): every acceptance item has an assertion — 6 check-digit values, 4 True validate forms ("03785955", "0378-5955", "1000002X", "1000-002X"), 5 False validate forms ("03785954", "1000002x", "0378595", "0378-595", "abcdefgh"), both TypeErrors, and all three ValueErrors.
- `packs/issn/handoff.md` and `status.json` state `done`, standard library only, no imports of ellipse/pluralize, no modification of pre-existing files — consistent with the card scope.

**Notes:**
- `status.json`/`handoff.md` report "194 passed" for the full suite while `checks-output.txt` shows "256 passed, 2 skipped" — pre-merge-report count bookkeeping, not a conflict.
- Worker installed pytest from `requirements-dev.txt` before running checks (environment setup, disclosed in handoff); the recorded check commands are the card's verbatim commands and both passed.

**Verdict: pass** (card, handoff, status, diff, and check outputs line up; no red mandated check).

---

## pluralize — PASS

**Evidence relied on:**
- `packs/pluralize/checks-failed.marker`: **absent**.
- `packs/pluralize/checks-exit.json`: both mandated checks exit 0 — `python3 -m pytest tests/test_pluralize.py -q` (exit 0), `python3 -m pytest tests/ -q` (exit 0).
- `packs/pluralize/checks-output.txt`: `35 passed in 0.02s` for the card-scoped run; `256 passed, 2 skipped in 15.34s` for the full suite.
- `packs/pluralize/diff.patch`: `pluralize.py` implements the pinned rule order verbatim, first match wins:
  1. uncountable set `{sheep, fish, deer, species, series, aircraft}` returned unchanged (so `sheep`/`fish` do not fall through to the sibilant rule);
  2. irregular table with all 11 entries including `quiz -> quizzes`;
  3. f/fe list of exactly the 10 pinned words (fe → drop `fe` + `ves`, f → drop `f` + `ves`), `roof` correctly falls through to the default rule → `roofs`;
  4. o→es list of exactly the 6 pinned words (`photo`, `piano` fall through → `photos`, `pianos`);
  5. consonant + y → `ies`, vowel + y skipped (`day`, `boy`, `toy`, `key` keep `y`);
  6. s/x/z/ch/sh → `es`;
  7. default → `s`.
  Validation raises TypeError for non-str, ValueError for empty or any char outside lowercase a-z (`"Cat"`, `"cat!"` → ValueError) before any rule runs.
- `packs/pluralize/diff.patch` (tests): 35 test functions — all 31 positive acceptance cases each have a dedicated test, plus `""`/`"Cat"`/`"cat!"` → ValueError and `None`/`3` → TypeError.
- `packs/pluralize/handoff.md` and `status.json` state `done`, standard library only, no imports of ellipse/issn, no modification of pre-existing files — consistent with the card scope.

**Notes:**
- `status.json`/`handoff.md` report "222 passed" for the full suite while `checks-output.txt` shows "256 passed, 2 skipped" — pre-merge-report count bookkeeping, not a conflict.
- Handoff discloses a bare-`"y"` guard (`len(word) >= 2` before the consonant+y rule) to keep the function total; the card defines no behavior for bare `"y"`, so this is an out-of-acceptance safety addition, not a contradiction of the card. It is not escalated as a conflict because nothing in the card or work order is contradicted.

**Verdict: pass** (card, handoff, status, diff, and check outputs line up; no red mandated check).

---

## Conflicts

None. No status.json or handoff.md flagged any conflict outside its card or inside the work order (no body-vs-acceptance mismatch found). All three processes were judged pass, and no verdict carries an escalated conflict.

## Summary

| Process | Verdict | Card-scoped checks | Full-suite checks |
|---------|---------|--------------------|-------------------|
| ellipse | pass | exit 0, 27 passed | exit 0, 256 passed, 2 skipped |
| issn | pass | exit 0, 7 passed | exit 0, 256 passed, 2 skipped |
| pluralize | pass | exit 0, 35 passed | exit 0, 256 passed, 2 skipped |

All verdicts recorded via `salvage_verdict` (ellipse, issn, pluralize) and sealed with `--final` on the last recorded process.
