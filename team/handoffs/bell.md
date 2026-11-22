# Handoff: bell（子任务 #770 · 第52轮并发 C 单）

## 请求内容

按工单 #763 / 流程卡 #770 实现 Bell 数组件，只新增两个文件：`bell.py` 与 `tests/test_bell.py`。

- `bell_number(n: int) -> int`：返回第 n 个 Bell 数 B_n（n 元集合划分数），B_0 = 1。
- 校验：n 非 int（含 bool，bool 拒）抛 TypeError；n < 0 抛 ValueError。
- 验收要点 14 个取值（B_0..B_10、B_15、B_20）+ 4 个错误用例（-1 → ValueError；2.5 / "5" / True → TypeError）。

## 已完成

- `bell.py`：标准库实现，Bell 三角（Aitken 三角）精确整数算法，无任何 import。
- `tests/test_bell.py`：pytest 参数化覆盖全部 13 个取值要点 + 4 个错误要点（共 17 个用例）。
- 未触碰任何存量文件；未 import tapcode / decimaltime。

## 未做（不在本卡范围）

- 未实现 tapcode.py、decimaltime.py 及其测试（并发 C 单其他流程卡负责）。
- 未 commit / push（工作流负责）。

## 检查与结果

1. `python3 -m pytest tests/test_bell.py -q` → 17 passed
2. `python3 -m pytest tests/ -q` → 154 passed, 1 skipped（skip 为存量用例，与本卡无关）

（注：环境初始无 pytest，按 requirements-dev.txt 安装了 pytest>=7.4.0 后执行；未改任何仓库文件。）

## 验证者须注意

- `bell_number(True)` 必须抛 TypeError（bool 是 int 子类，已用 `isinstance(n, bool)` 前置拒绝）。
- B_20 = 51724158235372 为大整数精确值，算法须用精确整数运算（本实现无浮点）。
- 错误类型顺序：先查类型（TypeError），再查负数（ValueError）。
