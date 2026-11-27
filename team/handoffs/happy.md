# Handoff: happy（sub-issue #968，#954 第59轮 D 单 · happy 件）

## 请求内容（Requested）

进程卡 #968：实现快乐数小组件，只创建两个新文件 `happy.py` 与 `tests/test_happy.py`：

- `is_happy(n: int) -> bool`：各位平方和迭代是否到达 1（快乐数达 1，不快乐数入 4-环）。
- `happy_numbers(limit: int) -> list[int]`：[1, limit] 内全部快乐数升序列表。
- 入参契约：`n < 1` 或 `limit < 1` 抛 `ValueError`；非 int（含 bool）抛 `TypeError`。
- 必须做环检测（见证集或 Floyd），不许固定步数猜测。
- 只用标准库；不 import huffman/natsort；不改任何存量文件。

## 我做了什么（Did）

- 创建 `happy.py`：
  - `_check_int` 统一入参校验（bool 按 TypeError 拒绝，< 1 按 ValueError 拒绝）。
  - `_digit_square_sum` 数位平方和。
  - `_is_happy_visited`：见证集环检测（`is_happy` / `happy_numbers` 使用）。
  - `_is_happy_floyd`：Floyd 龟兔判环（供性质测试对照，两个实现独立）。
  - `is_happy`、`happy_numbers` 对外 API。
- 创建 `tests/test_happy.py`：20 个测试，覆盖全部验收要点：
  - `is_happy(19)==True`、`is_happy(4)==False`、`is_happy(2)==False`、边界 `is_happy(1)==True`。
  - `happy_numbers(100)` 逐个列明 20 个、`len(happy_numbers(1000))==143`、升序且在界内。
  - 性质：[1, 2000] 见证集与 Floyd 逐个一致；`happy_numbers(2000)` 与共享记忆分类逐个一致。
  - ValueError：`is_happy(0)`、`happy_numbers(0)`（另加负数两个用例）。
  - TypeError：`is_happy(1.5)`、`is_happy(True)`（另加 `is_happy(None)`、`happy_numbers(10.0)`、`happy_numbers(False)`、`happy_numbers("100")`）。

## 我没做什么（Not done）

- 没有修改、删除任何存量文件。
- 没有触碰 `huffman.py`、`natsort.py` 及其测试（其他进程卡所有）。
- 没有创建任何 diff 文件（diff 由 prep 从分支生成，非工人交付物）。
- 没有 commit、没有 push（按指令由 workflow 执行）。
- 除本 handoff 与 `team/status/happy.json` 外未创建其他 team 文件。

## 检查与结果（Checks）

在仓库根目录运行：

1. `python3 -m pytest tests/test_happy.py -q` → **20 passed**（0.05s）。
2. `python3 -m pytest tests/ -q` → **362 passed, 2 skipped**（21.78s，全量通过）。

（2 个 skip 是仓库既有测试自身的跳过，与本件无关。）

## 验证者须知（Validator attention）

- 分支按 `branch_suffix: -r2` 派发；round-1 从未推送分支，非缺文件——本卡交付物仅 2 个源/测试文件 + 2 个 team 文件。
- 测试套件可能在仓库根生成 `verdict.json` / `verdict.md`，属流水线副产物，我已在收尾时删除，不应计入交付。
- `happy.py` 中 `_is_happy_floyd` 仅被性质测试引用，属验收要求的对照实现，不算多余文件。
- 两个实现（见证集与 Floyd）相互独立，性质测试在 [1, 2000] 逐个对照，结果全部一致。
