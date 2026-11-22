# Handoff: decimaltime（子工单 #771，第52轮并发 C 单）

## 请求了什么

实现十进制时间互转组件，只新增两个文件：`decimaltime.py` 与 `tests/test_decimaltime.py`。
规格逐字来自工单 #763 第52轮并发 C 单：

- 十进制时间钉死：一日 = 10 十进制时；每十进制时 = 100 十进制分；每十进制分 = 100 十进制秒；全日 100000 十进制秒对应常规 86400 秒。换算一律截断（向下取整），不四舍五入。
- `to_decimal(h, m, s) -> tuple[int, int, int]`：入参须为数值（int/float，bool 拒），非数值抛 TypeError；范围 0 ≤ h < 24、0 ≤ m < 60、0 ≤ s < 60，越界抛 ValueError。
- `from_decimal(dh, dm, ds) -> tuple[int, int, int]`：入参须为 int（bool 拒），非 int 抛 TypeError；范围 0 ≤ dh < 10、0 ≤ dm < 100、0 ≤ ds < 100，越界抛 ValueError。
- 验收要点：工单列出的全部 value 例、往返例、ValueError 例、TypeError 例，每条都要有对应测试。

## 做了什么

- 新建 `decimaltime.py`（仅标准库：`fractions.Fraction`；不 import bell/tapcode/任何其他模块）。
  - 核心算法：常规秒 → 十进制秒乘 125/108 后向下取整；十进制秒 → 常规秒乘 108/125 后向下取整（86400/100000 约分为 108/125）。
  - 用 `fractions.Fraction` 做精确有理数乘法再 `//` 截断，避免浮点 `int(...)` 在边界处的取整偏差（例如 `to_decimal(1, 0, 0)` 需要精确 4166，而非浮点误差下的 4165.999…）。
  - 类型/范围校验与规格逐字对应，bool 一律按非目标类型拒绝。
- 新建 `tests/test_decimaltime.py`：工单列出的每一条验收要点都有独立测试用例（value 8 条 + from_decimal value 6 条 + 往返 3 条 + ValueError 7 条 + TypeError 3 条），另加少量规格内补充用例（其余参数位的类型/范围拒绝、float 入参接受），共 32 个用例。
- 未修改任何存量文件；未新建或改动 bell.py / tapcode.py / tests/test_bell.py / tests/test_tapcode.py（属并发 A/B 单）。
- 未 commit、未 push（按流程留待工作流处理）。
- 环境说明：容器初始无 pytest，已按 `requirements-dev.txt` 安装 pytest 9.2.0（`python3 -m pip install --user pytest`）以便运行 checks。

## 没做什么

- 未实现 bell、tapcode 任何内容。
- 未修改任何存量文件（`git status` 中本单相关新增仅 decimaltime.py、tests/test_decimaltime.py、team/handoffs/decimaltime.md、team/status/decimaltime.json）。
- 未提交、未推送。
- 不对三件之外的验收面（写板新判据、装配单源面、链路落账）负责；本单只对 decimaltime 实现本身负责。

## 跑了哪些检查与结果

均在仓库根目录运行：

1. `python3 -m pytest tests/test_decimaltime.py -q` → **32 passed in 0.03s**
2. `python3 -m pytest tests/ -q` → **169 passed, 1 skipped in 14.82s**（该 1 skip 为存量用例，与本单无关）

## 验证者须注意

- 逐字验收：工单验收要点的每一条在 `tests/test_decimaltime.py` 中都有对应用例，值与异常类型逐字一致。
- 截断语义：`to_decimal(0, 0, 1) == (0, 0, 1)`、`from_decimal(0, 0, 1) == (0, 0, 0)` 体现双向截断；实现用精确有理数截断，不依赖浮点。
- 类型边界：`bool` 在两个函数中都被拒绝（`to_decimal(True, 0, 0)` 抛 TypeError；`from_decimal(True, 0, 0)` 同样抛 TypeError）；`from_decimal` 严格拒 float（含 `1.5`）。
- 范围边界：上下界均按下界闭、上界开（h=24、m=60、s=60、dh=10、dm=100 均抛 ValueError；负数同抛 ValueError）。
- 全量套件中的 1 个 skip 是存量用例的既有跳过，非本单引入。
