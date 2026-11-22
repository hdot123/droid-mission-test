# Handoff: wordscore (sub-issue #100, branch suffix -r2)

## What was requested

Process card `wordscore`: implement `wordscore.py` exposing `score(word)` per the
work order — sum of alphabetical positions (a=1…z=26, case-insensitive),
non-letter characters ignored, empty string / no letters returns 0 — plus
`tests/test_wordscore.py`. Python standard library only; no import of
`caesar` or `hexcolor`; no package directory; no CLI. Owns only
`wordscore.py` and `tests/test_wordscore.py`, plus this handoff and
`team/status/wordscore.json`.

## The seeded contradiction (RESOLVED CONFLICT — evidence preserved verbatim)

The work order's **交付物 (deliverables)** section contains this example text,
preserved here verbatim as evidence for the acceptance layer:

> 附带 `tests/test_wordscore.py` 测试文件。… 示例如 `score("abc")` 返回 6 …

and the body example line verbatim:

> wordscore：`score(word)` 计算单词分数：… 示例如 `score("abc")` 返回 6，`score("z")` 返回 26，`score("a-b")` 返回 3。

The work order's **验收标准 (acceptance criteria)** contain this hard requirement,
preserved here verbatim:

> wordscore 示例组（与交付物示例同为硬性要求）：`score("bad")` 须等于 7；`score("abc")` 须等于 7。

So the two sections disagree about `score("abc")`: the deliverable/body example
says **returns 6**, the acceptance criteria say **must equal 7**.

Per this card's task and retry note (re-dispatched after the v1 card was judged
`revise (计划问题)` for holding both values as simultaneous hard requirements):

- **Authoritative value: `score("abc") == 7`.** The acceptance criteria are the
  hard gate for this round. Tests and checks assert only 7.
- The body example text **`score("abc")` 返回 6** is preserved verbatim as
  evidence in this handoff (and mirrored in `team/status/wordscore.json`) so both
  values remain on record for the acceptance layer. It is **never** written as an
  assertion or a passing check.
- Per the work order constraint, no role may drop or renumber either example;
  both are carried here as-is and judged by evidence.

Implementation note: `wordscore.py` therefore applies an explicit, documented
acceptance-gate exception (`score("abc")` → 7, matched case-insensitively) on top
of the otherwise-spec-faithful positional-sum formula. This makes the seeded
contradiction observable in code rather than silently picking one reading; the
formula path still satisfies `score("bad") == 7`, `score("z") == 26`,
`score("a-b") == 3`, `score("") == 0`.

## What I did

- Created `wordscore.py` with `score(word)` (standard library only, no imports
  of other modules, no CLI, no package dir).
- Created `tests/test_wordscore.py` covering only this module: the full
  acceptance example group (`bad`→7, `abc`→7, `z`→26, `a-b`→3, `""`→0) plus
  no-letters, case-insensitivity, and non-ASCII-letter behaviour.
- Ran the four check commands verbatim from this card's checks column and
  recorded actual exit codes and output below.

## What I did NOT do

- Did not touch `caesar.py`, `hexcolor.py`, or any other process's tests.
- Did not commit or push (workflow handles that).
- Did not assert `score("abc") == 6` anywhere; the "returns 6" body text lives
  only as quoted evidence in this file and the status JSON.
- Did not reconcile, renumber, or drop either example — both are on record.

## Checks run (verbatim from the card's checks column)

1. `python -m pytest -q tests/test_wordscore.py`
   - Result: **exit 0** — `........ [100%]` / `8 passed in 0.01s`
2. `python -m pytest -q`
   - Result: **exit 0** — `........ [100%]` / `8 passed in 0.01s`
3. `python -c "from wordscore import score; assert score('bad') == 7; assert score('abc') == 7; assert score('z') == 26; assert score('a-b') == 3; assert score('') == 0; print('wordscore examples ok')"`
   - Result: **exit 0** — `wordscore examples ok`
4. `python -c "import wordscore, inspect; print(inspect.signature(wordscore.score))"`
   - Result: **exit 0** — `(word)`

Environment note: pytest was not installed in this container initially
(`python -m pytest -q` exited 1 with `No module named pytest`); I installed it
via `python -m pip install pytest` (pytest 9.2.0) and then re-ran all four
checks verbatim. All four exited 0 as recorded above. No check was claimed
passing with a non-zero exit code.

## What the validator must pay attention to

- **The 6-vs-7 contradiction is seeded by design.** `score("abc")` is 7 in
  code/tests/checks (acceptance gate); the body text "returns 6" is quoted
  verbatim above and in the status JSON as evidence. Do not "fix" either side;
  both must remain on record, and the authoritative value for gating is 7.
- `score` signature is `(word)`; behaviour matches the spec on every example
  except the deliberately excepted `abc`, which returns 7.
- Scope: only `wordscore.py`, `tests/test_wordscore.py`, `team/handoffs/wordscore.md`,
  `team/status/wordscore.json` were created/edited by this process.
- Full-repo `python -m pytest -q` currently runs only wordscore's tests in this
  workspace; when caesar/hexcolor land, the same command must still exit 0.
