# Handoff: ISSN 校验位（issn.py）

Sub-issue: #826（工作单 #814 第54轮并发 C 单 ·领班制 v2.8.0＋M4 修复，基线 d7b183a）

## What was requested

实现两个函数，只新增 `issn.py` 与 `tests/test_issn.py` 两个文件，只用标准库，不 import 其他仓库模块（ellipse、pluralize 等），不改任何存量文件：

1. `issn_check_digit(seven) -> str`：非 str 抛 TypeError；非恰好 7 位 ASCII 数字抛 ValueError。算法钉死：前 7 位依次乘权重 8、7、6、5、4、3、2 求和，`check = (11 − (sum % 11)) % 11`；`check == 10` 返回 `"X"`，否则返回该数字的一位字符串。
2. `issn_validate(code) -> bool`：非 str 抛 TypeError。接受两种形态：8 位无分隔（前 7 位数字＋末位数字或大写 X），或 9 位带连字符（第 5 个字符为 `-`，去掉后同前）。其余形态（长度不对、连字符位置不对、前 7 位含非数字、末位小写 x 或其他字符）一律返回 False、不抛错；形态合则与 `issn_check_digit` 核对末位，一致 True、否则 False。

验收要点（逐条对应测试）：`"0378595"→"5"`、`"2049363"→"0"`、`"1234567"→"9"`、`"0000000"→"0"`、`"9999999"→"4"`、`"1000002"→"X"`；validate 真值 `"03785955"`、`"0378-5955"`、`"1000002X"`、`"1000-002X"`；假值 `"03785954"`、`"1000002x"`、`"0378595"`、`"0378-595"`、`"abcdefgh"`；`issn_check_digit(378595)` 与 `issn_validate(None)` 抛 TypeError；`issn_check_digit("037859")`、`issn_check_digit("03785955")`、`issn_check_digit("0378a95")` 抛 ValueError。

## What I did

- 新建 `issn.py`：`issn_check_digit` 按钉死算法实现（`zip(digits, (8,7,6,5,4,3,2))` 加权求和，`(11 - sum % 11) % 11`，10 → `"X"`）；输入校验为 `isinstance(str)` → TypeError，`len != 7 or not isdigit or not isascii` → ValueError。`issn_validate` 先做类型检查，再按长度分流（9 位要求 `code[4] == "-"` 后拼接去连字符；8 位直接用），任何形态不符返回 False；形态合法才调用 `issn_check_digit` 比对末位。仅标准库、无跨模块 import。
- 新建 `tests/test_issn.py`：7 个测试函数覆盖全部验收要点（真实 ISSN 前缀、6 个 check_digit 已知值、4 个 validate 真值、5 个 validate 假值、两处 TypeError、三处 ValueError）。每条验收要点均有断言。
- 未修改任何存量文件。

## What I did not do

- 未触碰 `ellipse.py`、`pluralize.py` 及其测试（并发 C 单其他件，其他 worker 负责）。
- 未修改任何存量文件、未 commit/push（工作流负责）。
- 未写 `verdict.json`/`verdict.md`（全量测试运行后确认仓库根目录无此类产物，无需清理）。
- 未做 spec 之外的任何扩展（如大小写不敏感、连字符其他位置、Unicode 数字等一律按 spec 拒绝/返回 False）。

## Checks run and results

环境说明：系统 `python3`（3.14.4）初始无 pytest，按仓库 `requirements-dev.txt` 安装（pytest 9.2.0）后运行检查。

- `python3 -m pytest tests/test_issn.py -q` → **7 passed in 0.02s**（exit 0）
- `python3 -m pytest tests/ -q` → **194 passed, 2 skipped in 16.37s**（exit 0）

两个检查均为逐字命令，均通过。

## Notes for the validator

- 两个文件均为新增，与并发 C 单其他件（ellipse、pluralize）无 import 关系，合并时三件互不冲突。
- `issn_validate` 对 9 位形态只认第 5 个字符为 `-`；`"0378-595"`（8 位）与 `"0378595"`（7 位）按 spec 返回 False 而非抛错——测试已覆盖。
- 末位小写 `x` 被判 False（不 raise），大写 `X` 参与校验；`issn_check_digit` 输入校验用 `isascii()` 排除 Unicode 数字。
- `tests/` 中有 2 个既有 skip，与本单无关。
