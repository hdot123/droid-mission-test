# Handoff: monthgrid（子单 #858 · 工单 #849 第55轮并发 B 单）

## 要求（Requested）

实现月历网格生成组件，只新增两个文件：`monthgrid.py` 与 `tests/test_monthgrid.py`。
不改任何存量文件；只用标准库；不 import 同单的 `deque.py`、`sdbmhash.py`。
规格逐字要点：

1. `days_in_month(year: int, month: int) -> int`：格里高利闰年规则的月天数。
2. `month_grid(year, month, first_weekday: int = 0)`：周行 × 7 网格，当月日期填数字、
   月外填 `None`；`first_weekday` 0=周一 … 6=周日。
3. `month` 超出 1..12 或 `first_weekday` 超出 0..6 抛 `ValueError`。

## 我做了什么（Did）

- `monthgrid.py`：`_is_leap()` 实现格里高利规则（被 4 整除且不被 100 整除，或被 400 整除）；
  `days_in_month()` 校验 month 后返回天数；`month_grid()` 用 Sakamoto 公式求当月 1 号的
  星期（0=周一…6=周日），按 `first_weekday` 求偏移填 `None`，补齐 7 的倍数后切行。
- `tests/test_monthgrid.py`：9 个测试逐字覆盖全部验收要点——
  7 个 days_in_month 字面值（2024/2023/2000/1900/2100/2026-1/2026-4）、
  1999–2031 对照 `calendar.monthrange`、
  `month_grid(2026, 2, 0)` 整格、`month_grid(2024, 2, 6)` 首行与末行、
  1999–2031 对照 `calendar.monthcalendar`（0 换 None 逐格）、
  任意 first_weekday（0..6，1999–2031 全年）结构不变量（每行 7 格、展平非 None 恰为 1..天数）、
  4 个 ValueError（month 13/0、first_weekday 7/-1，另加 month 0/13 经 month_grid 触发）。

## 我没做什么（Not done）

- 未创建或修改 `deque.py`、`sdbmhash.py` 及其测试（并发 B 单其他子单所有）。
- 未改动任何存量文件；未 commit / push（由工作流负责）。
- 未写 `verdict.json`/`verdict.md`（若测试套件产生则为流水线副产物，已删除）。

## 我跑过的检查（Checks）

1. `python3 -m pytest tests/test_monthgrid.py -q` → **9 passed**（全绿）。
2. `python3 -m pytest tests/ -q` → **349 passed, 2 skipped, 1 failed**。
   唯一失败 `tests/test_check_summary_focused_counts.py::test_summary_block_on_r54_pack_produces_real_focused_counts`，
   原因是 `FileNotFoundError: /tmp/r54-audit/a/evidence/packs/damm/checks-output.txt`——
   该测试依赖环境外部 fixture `/tmp/r54-audit`（本机不存在）。
   **已验证为存量失败**：stash 掉我的两个文件后重跑该测试同样失败（1 failed, 4 passed），
   与本单交付物无关。

## 验证者须注意（Validator）

- 本单两个文件仅新增，`git status` 应显示 `?? monthgrid.py`、`?? tests/test_monthgrid.py`。
- 全量测试中 `test_check_summary_focused_counts` 的失败是环境缺外部 fixture 所致，
  请对照基线 `1b38090`（或 stash 本单文件）判定，勿归因于 monthgrid。
- 所有验收要点均有对应测试；`month_grid` 返回值类型标注按规范语义实现
  （返回 `list[list[int | None]]` 结构，注释声明规格）。
