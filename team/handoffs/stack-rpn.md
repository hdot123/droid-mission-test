# Handoff: stack-rpn (sub-issue #57)

## What was requested
Process card `stack-rpn` under work order #53 (第十二轮 · v2.6.2 收官复跑): implement the `stack.py` module and its tests, owning only `stack.py` and `tests/test_stack.py`.

Required behavior:
- Class `Stack` with `push(x)`, `pop()` (raises `IndexError` when empty), `peek()` (raises `IndexError` when empty), `is_empty()`, and `__len__`.
- Module function `eval_rpn(tokens)` that evaluates reverse-Polish expressions using `Stack`. Each token is a string that is an integer or one of `"+-*/"`. Division is integer division truncating toward zero (`int(a / b)`, not `//`, so `-7 2 /` is `-3`). Division by zero raises `ZeroDivisionError`. Empty tokens or invalid expressions (not enough operands, leftover operands, invalid token) raise `ValueError`. Results are `int`.
- Stdlib only; no imports of the other two modules; no package directory; no CLI.
- Tests cover: Stack push/pop/peek/is_empty/__len__, pop and peek `IndexError` on empty, the three spec examples (`["2","1","+","3","*"]` → 9, `["4","13","5","/","+"]` → 6, `["-7","2","/"]` → -3), negative operands, truncation toward zero, `ZeroDivisionError`, empty-tokens `ValueError`, and malformed-expression `ValueError`s. Tests only exercise this module.

## What I did
- Created `stack.py`:
  - `Stack` backed by a list; `pop`/`peek` raise `IndexError("...empty stack")` on an empty stack; `is_empty()` returns a bool; `__len__` delegates to the list.
  - `eval_rpn(tokens)` raises `ValueError` for empty tokens; for each operator token requires at least 2 operands on the stack (else `ValueError("not enough operands...")`); computes `+ - *` normally; for `/` raises `ZeroDivisionError` when the divisor is `0` and otherwise pushes `int(a / b)` (true truncation toward zero); non-integer, non-operator tokens raise `ValueError`. At the end, anything other than exactly one stack item raises `ValueError("invalid expression: leftover operands")`. Returns an `int`.
- Created `tests/test_stack.py` (17 tests) covering every case listed in the task, including all three spec examples, negative operands, `7 / -2 == -3` and `-8 / 3 == -2` truncation cases, `int` result type, three `ZeroDivisionError` cases, empty tokens, not-enough-operands, leftover-operands, and an invalid token (`%`).

## What I did not do
- Did not touch `urlparse_mini.py`, `temperature.py`, any other test file, or shared config (none of those exist in this repo yet; other processes own them).
- Did not create a package directory, CLI, or any imports beyond the standard library (`pytest` used only in tests).
- Did not commit or push anything.

## Checks run and results
1. `python -m pytest -q tests/test_stack.py` → **17 passed in 0.02s** (first attempt failed with "No module named pytest"; installed pytest into the environment, then the run passed).
2. `python -c "from stack import eval_rpn; assert eval_rpn(['2','1','+','3','*']) == 9 and eval_rpn(['4','13','5','/','+']) == 6 and eval_rpn(['-7','2','/']) == -3; print('ok')"` → **ok**

## What the validator must pay attention to
- `eval_rpn` division must truncate toward zero: I used `int(a / b)`, not `//`. Note `int(a / b)` converts via float; for the integer magnitudes this task specifies that is exact, and it is the form the process card explicitly permits. `//` would give the wrong answer for negative operands (`-7 // 2 == -4`).
- `ValueError` is raised both mid-expression (not enough operands / bad token) and after the loop (leftover operands). Empty input also raises `ValueError`.
- `ZeroDivisionError` is raised only when a `/` operator sees a `0` divisor, and it is not swallowed by the `ValueError` paths.
- `Stack.pop`/`peek` raise `IndexError`, distinct from the `ValueError`s raised by `eval_rpn`.
- The full repo suite (`python -m pytest -q`) was not run by me, because sibling modules (`urlparse_mini.py`, `temperature.py`, etc.) are owned by other processes and may not exist yet; my scope check was `tests/test_stack.py` only.
