# Handoff: lensarea（双圆交叠 / 透镜面积）——子单 #933

工单：#927 第58轮 B 单（kmpsearch / farey / lensarea 并发），本单只负责 lensarea 两件。

## 要求（requested）

- `lensarea.py` 提供 `lens_area(r1, r2, d) -> float`：半径 r1、r2、圆心距 d 的两圆交叠（透镜）面积。
- 入参约定：任一入参为负抛 `ValueError`；非数值（含 `bool`）抛 `TypeError`；半径为 0 合法，返 0.0。
- 浮点验收相对误差 1e-9。
- 边界钉死：
  - 外切（`d == r1 + r2`）与分离：**恰返 0.0**；
  - 内切/包含（`d <= |r1 - r2|`）：**恰返小圆全面积 `π·min(r1, r2)²`**，边界处不得出近似小量或 NaN；
  - 两圆互换（r1 ↔ r2）结果不变。
- 验收要点每项都要有对应测试；随机重叠三元组上须与两弓形（扇形 − 三角）合成、Simpson 数值积分两路一致（积分路容差 1e-4）。
- 只新增 `lensarea.py`、`tests/test_lensarea.py` 两文件；不改任何存量文件；仅标准库；不 import kmpsearch / farey。

## 我做了什么（did）

- `lensarea.py`（新增，纯标准库，仅 import math）：
  - `_as_float`：拒 `bool` 与非 `int`/`float`，其余转 `float`，否则 `TypeError`。
  - 顺序：校验非负（`ValueError`）→ 任一半径为 0 返 `0.0` → `d >= r1 + r2` 返 `0.0`（先判边界，避免通用式在边界出 NaN）→ `d <= |r1 - r2|` 返 `π·small²` → 严格交叠走闭式 `r1²·acos(cos1) + r2²·acos(cos2) − ½√Heron`。
  - 闭式细节：cos 先截到 [-1,1]；Heron 项下截 0；结果下截 0（防 -0.0 / 负零漂移）。r1↔r2 对称由公式本身保证。
- `tests/test_lensarea.py`（新增，16 个用例，覆盖全部验收要点）：
  - 具体数值：等边交叠 `2π/3 − √3/2`、同心 4π、包含 π、内切 π、外切 `== 0.0`、分离 `== 0.0`、`lens_area(0,5,1)`、`lens_area(5,0,0)`。
  - 对称性：40 组随机三元组 r1↔r2 一致。
  - 两路一致：独立 `_segments`（扇形 − 等腰三角，每侧独立，与被测闭式不同写法）60 组；独立 `_simpson`（竖直条带高度 `2·min(√(r1²−x²), √(r2²−(x−d)²))` 复合 Simpson，8000 面板）15 组，容差 1e-4。
  - 入参约定：负 r1 / 负 d / 负 r2 → ValueError；`"1"`、`True`、`None`、`"x"`、`[1]` → TypeError。
  - 随机种子固定 `random.Random(5803)`，可复现。

## 我没有做什么（not done）

- 没有碰 `kmpsearch.py`、`farey.py`、任何存量文件，没有碰 `team/` 里别人的目录。
- 没有 commit / push。
- 没有跨模块 import；没有第三方依赖。
- 没有改动测试套件、fixtures、schemas、scripts。

## 跑过的 checks

- `python3 -m pytest tests/test_lensarea.py -q` → **16 passed**（0.04s）。
- `python3 -m pytest tests/ -q` → **358 passed, 2 skipped**（17.82s，exit 0）。skip 是存量用例自带的，与本单无关。
- 跑完后仓库根**没有**生成 `verdict.json` / `verdict.md`（已确认 `ls` 不存在），无需清理。

## 验证方须注意（validator）

1. 边界必须是**恰等**：`lens_area(1,1,2) == 0.0`、`lens_area(3,1,2.0) == math.pi`（不是 `approx`）。实现里 `d >= r1+r2` 与 `d <= |r1−r2|` 两个分支都走精确返回，通用闭式只在严格交叠区执行。
2. `bool` 必须被拒：`isinstance(True, int)` 在 Python 里为真，`_as_float` 显式先拦 `bool`，所以 `lens_area(1, True, 1)` 抛 TypeError 而非当 1 处理。
3. 测试里的 `_segments` / `_simpson` 是**测试侧独立参考实现**，不是从 lensarea import 的；若你改用被测实现自证，会失去独立性。
4. Simpson 路容差 1e-4（`abs`，非相对）；面板数 8000 在实测随机样本上最大绝对误差约 2.4e-5，留有余量。面板数是测试常量 `SIMPSON_PANELS`，不是实现的一部分。
5. 本单不负责工单里的 (a)–(j) 汇总验收、落账、单三顺延等条目——那些归领班/其他单。
