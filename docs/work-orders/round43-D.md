## 目标
实现三个独立的度量与换算小组件（第四十三轮 · 并发 D 单：领班制 v2.6.5）。三件彼此独立、无依赖。

## 交付物
dms.py、bytefmt.py、kelvin.py 与 tests/test_dms.py、tests/test_bytefmt.py、tests/test_kelvin.py（只新增，不改任何存量文件）。

## 验收标准
验收以合并后全量测试为准；逐模块规格、验收要点与 checks 如下，逐字为准。

一、dms.py —— 十进制度数与度分秒
- `to_dms(deg: float) -> tuple[int, int, float]`：将十进制度数转为 `(度, 分, 秒)`；度的符号写入度分量（南纬／西经为负度、分和秒为非负）；秒保留最多 6 位小数并四舍五入，四舍五入后进位到分／度。
- `from_dms(d: int, m: int, s: float) -> float`：`d + m/60 + s/3600`；要求 m∈[0,59]、s∈[0,60)（秒可取 60.0 表示进位）、否则抛 ValueError。
- 验收要点：`to_dms(48.8584) == (48, 51, 30.24)`；`to_dms(-118.2437) == (-118, 14, 37.32)`；`to_dms(0) == (0, 0, 0.0)`；`from_dms(48, 51, 30.24) == 48.8584`；`from_dms(-118, 14, 37.32) == -118.2437`；`from_dms(0, 0, 0) == 0.0`；`from_dms(0, 60, 0)`、`from_dms(1, -1, 0)` 抛 ValueError；对 `48.8584`、`-118.2437` 做往返恒等（容差 `abs(...) < 1e-9`）。
- checks（逐字）：`python3 -m pytest tests/test_dms.py -q`、`python3 -m pytest tests/ -q`

二、bytefmt.py —— 字节可读格式（IEC 1024）
- `format_bytes(n: int) -> str`：n 为非负整数，输出 `"{值} {单位}"`；单位序列为 `B`、`KiB`、`MiB`、`GiB`、`TiB`（每项 1024 倍）；小于 1024 时用整数 B；否则保留一位小数。n 为负数抛 ValueError。
- 验收要点：`format_bytes(0) == "0 B"`；`format_bytes(512) == "512 B"`；`format_bytes(1536) == "1.5 KiB"`；`format_bytes(1048576) == "1.0 MiB"`；`format_bytes(1536 * 1024) == "1.5 MiB"`；`format_bytes(-1)` 抛 ValueError。
- checks（逐字）：`python3 -m pytest tests/test_bytefmt.py -q`、`python3 -m pytest tests/ -q`

三、kelvin.py —— 温标换算
- `c_to_k(c: float) -> float`：摄氏转开尔文，`c + 273.15`。
- `k_to_c(k: float) -> float`：开尔文转摄氏，`k - 273.15`；k 小于 0 抛 ValueError。
- `c_to_f(c: float) -> float`：`c * 9/5 + 32`。
- `f_to_c(f: float) -> float`：`(f - 32) * 5/9`。
- 验收要点（浮点容差 `1e-9`）：`abs(c_to_k(0) - 273.15) < 1e-9`；`abs(c_to_k(100) - 373.15) < 1e-9`；`abs(k_to_c(273.15) - 0.0) < 1e-9`；`abs(c_to_f(0) - 32.0) < 1e-9`；`abs(c_to_f(100) - 212.0) < 1e-9`；`abs(f_to_c(32) - 0.0) < 1e-9`；`abs(f_to_c(212) - 100.0) < 1e-9`；`k_to_c(-1)` 抛 ValueError；`c_to_f` 与 `f_to_c` 在 37.0℃ 往返恒等。
- checks（逐字）：`python3 -m pytest tests/test_kelvin.py -q`、`python3 -m pytest tests/ -q`

## 约束
只新增上述六个文件；不改任何存量文件；三件实现只用标准库、不互相 import；每个验收要点都要有对应测试用例。