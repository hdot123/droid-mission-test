# Handoff: centroid（子工单 #779，工作单 #761 并发 A 单）

## 领到的请求

实现 `centroid.py`（多边形带符号面积与重心）与 `tests/test_centroid.py`，逐字按工作单 #761 第三节规格：

- `polygon_area(vertices) -> float`：鞋带公式带符号面积（逆时针为正、顺时针为负）；共线退化返回 0.0。
- `polygon_centroid(vertices) -> tuple[float, float]`：面积加权重心，用带符号面积计算，顺/逆时针一致；面积为 0 抛 ValueError。
- 入参校验：容器非 list/tuple、顶点非二元数对、坐标非数值（bool 拒）抛 TypeError；顶点少于 3 抛 ValueError。
- 只新增 `centroid.py` 与 `tests/test_centroid.py` 两个文件；只用标准库；不 import chaocipher/base62；每个验收要点都要有对应测试用例。

## 实际做了什么

- 新增 `centroid.py`：私有 `_validate` 统一做容器/顶点/坐标（含 bool 拒）校验；`polygon_area` 用鞋带公式（首尾环绕）带符号求和；`polygon_centroid` 用 `cross = x1*y2 - x2*y1` 累加，返回 `(Σ(x1+x2)*cross / (3*Σcross), Σ(y1+y2)*cross / (3*Σcross))`（带符号，故顺/逆时针一致），`Σcross == 0` 抛 ValueError。
- 新增 `tests/test_centroid.py`：23 个用例，覆盖全部逐字验收要点（正方形顺/逆时针、三角形、长方形、L 形 1e-9、房屋形 1e-9、共线 0.0、ValueError 三条、TypeError 四条），另补 tuple 容器接受、polygon_area 的容器/顶点/坐标 TypeError 补测。
- 跑了 pip install -r requirements-dev.txt（环境原无 pytest，只装到 user site，未改任何仓内文件）。

## 没有做什么

- 未改任何存量文件；未碰 `chaocipher.py`、`base62.py` 及其测试；未碰 `team/` 以外的他人产物（team 下两个文件按工作流指令写）。
- 未 commit / push。
- 未实现 chaocipher、base62（属并发其他工单）。

## 跑过的 checks 及结果

1. `python3 -m pytest tests/test_centroid.py -q` → **23 passed in 0.02s**
2. `python3 -m pytest tests/ -q` → **160 passed, 1 skipped in 14.37s**（全量无回归）

## 验证者需注意

- 等值断言用 `==` 精确比较（如 `(1.0, 1.0)`、`4.5`、`8.0`），仅 L 形与房屋形重心按规格用 1e-9 容差；实现里除以 `3*Σcross` 而非 `6*A` 是浮点等价形式，结果与验收值逐位一致（已由 `==` 断言验证）。
- bool 作为坐标必须 TypeError（`isinstance(True, int)` 为真，已显式排除）；顶点二元用 `len(vertex) != 2` 判定，`(2,)` 抛 TypeError 而非 ValueError。
- `polygon_centroid` 对共线（面积 0）抛 ValueError，与「顶点 < 3 抛 ValueError」是两条独立路径，测试分别覆盖。
- 全量 1 skip 来自存量测试，与本单无关。
