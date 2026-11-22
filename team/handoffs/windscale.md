# Handoff: windscale（子问题 #768 / 工单 #762 并发 B 单）

## 请求内容

按工单 #762 逐字规格实现蒲福风级组件，只交付两个新文件：

- `windscale.py`
- `tests/test_windscale.py`

约束：只新增，不改任何存量文件；仅标准库；不与 dijkstra、nthprime 互 import；每个验收要点都要有对应测试用例。

## 我做了什么

1. `windscale.py`（新文件）：
   - `_THRESHOLDS` 钉死各级下限（km/h，下限含、上限为下一级下限）：0/1/6/12/20/29/39/50/62/75/89/103/118。
   - `_LABELS` 0–12 级中文名：无风、软风、轻风、微风、和风、清风、强风、疾风、大风、烈风、狂风、暴风、飓风。
   - `_validate_speed`：bool 拒（`isinstance(x, bool)` 先判）、非 int/float 抛 TypeError、负数抛 ValueError。
   - `beaufort(speed_kmh) -> int`：按阈值表线性扫描返回 0–12。
   - `beaufort_label(speed_kmh) -> str`：复用 `beaufort` 校验与分级后查表返回中文名。
2. `tests/test_windscale.py`（新文件）：parametrize 覆盖全部 27 个分级验收点、6 个标签验收点、`beaufort(-1)` 抛 ValueError、`beaufort("50"/True/None)` 抛 TypeError；另加 `beaufort_label` 同款负数与 TypeError 校验（规格要求入参校验同 `beaufort`），保证 label 路径不绕过校验。
3. 运行了工单要求的两条 checks（见下）。

## 我没有做什么

- 未触碰 `dijkstra.py`、`nthprime.py` 或任何存量文件；未改 `team/` 下他人路径。
- 未 commit / push。
- 未实现工单中另两件（dijkstra、nthprime）——归并发 A/C 单。
- 未做任何验收要点之外的扩展（如风速区间字符串、单位换算等）。

## 检查与结果

| 命令 | 结果 |
| --- | --- |
| `python3 -m pytest tests/test_windscale.py -q` | `41 passed in 0.02s` |
| `python3 -m pytest tests/ -q` | `178 passed, 1 skipped in 14.80s`（全量，退出码 0） |

说明：环境初始无 pytest，已按 `requirements-dev.txt` 用 `pip3 install --user -r requirements-dev.txt` 装齐（pytest 9.2.0）；这是环境准备，未改任何仓库文件。

## 验证者须注意

- 全量套件里那个 `1 skipped` 是存量跳过项，与本单无关；判据应以“无 failed/error、退出码 0”为准。
- 分级边界是**下限含、上限含**（如 5→1 级、6→2 级、117→11 级、118→12 级）；`beaufort(0.9) == 0`、`beaufort(32.5) == 5` 证明浮点路径也走同一阈值表。
- `bool` 是严格拒绝的（`True` 抛 TypeError 而非按 1 处理）——校验里 bool 判断必须在 int 判断之前，因为 `bool` 是 `int` 子类。
- `beaufort_label` 的入参校验与 `beaufort` 完全一致（规格要求），已用测试覆盖。
- 本单文件清单应恰为 4 个新增路径：`windscale.py`、`tests/test_windscale.py`、`team/handoffs/windscale.md`、`team/status/windscale.json`。
