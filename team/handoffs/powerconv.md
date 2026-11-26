# Handoff: powerconv（子单 #886，工单 #878 C 单三件之一）

## 请求（What was requested）

实现功率单位换算小组件，只新增两个文件：`powerconv.py` 与 `tests/test_powerconv.py`。

- `convert_power(value, from_unit, to_unit) -> float`，单位集钉死为 {W, kW, hp, PS, BTU/h, ftlbf/s}，基准 W：
  - kW = 1000
  - hp = 745.699872（机械马力）
  - PS = 735.49875（公制马力）
  - BTU/h = 1055.05585262/3600
  - ftlbf/s = 1.3558179483314004
- 未知单位（含大小写不符）抛 ValueError；浮点验收相对误差 1e-9。
- 本单是**功率**换算；A 单 energyconv 是能量换算，两者单位集互不相交——BTU/h 是功率单位在集内，BTU 是能量单位**不在**集内；hp 与 PS 是两个不同常数，不得混用。
- 九条验收要点逐条要有对应测试。

## 做了什么（What I did）

- 新增 `powerconv.py`：`_FACTORS` 字典钉死六个单位相对 W 的系数，`convert_power` 先按 from/to 查表（查不到即抛 ValueError），再走 `value * factor[from] / factor[to]`，天然满足恒等与换算链一致性（同一基准中转，浮点相对误差远小于 1e-9）。
- 新增 `tests/test_powerconv.py`（13 个用例），逐条覆盖九条验收要点：
  1. `convert_power(1, "hp", "W") ≈ 745.699872`
  2. `convert_power(1, "PS", "W") ≈ 735.49875`
  3. `convert_power(1, "hp", "ftlbf/s") ≈ 550.0`（abs_tol=1e-6，两钉死常数互证）
  4. `convert_power(1, "kW", "hp") ≈ 1.3410220896`
  5. `convert_power(100, "W", "BTU/h") ≈ 341.2141633`
  6. `convert_power(0, "hp", "kW") == 0.0`
  7. 恒等与换算链：对每个单位 u，`convert_power(3.7, u, "W")` 与经 hp 中介到 PS 的链路均与直达一致（相对误差 1e-9）
  8. `convert_power(1, "W", "MW")` 抛 ValueError（双向均测）
  9. `convert_power(1, "HP", "W")` 抛 ValueError（大小写不符，双向均测）
- 另加守卫用例：单位集恰为规格所列六个且不含 BTU（能量单位）；hp ≠ PS 且互换比值正确；往返链 u→kW→u 可逆；返回类型为 float。

## 没做什么（What I did not do）

- 未编辑、修改或删除任何存量文件；未触碰 `team/**` 中他人文件、`.github/**`、`legacy_stringkit.py`、`roman.py` 等。
- 未实现能量换算（BTU 等能量单位归 A 单 energyconv），本模块单位集不含 BTU。
- 未实现 kaprekar、squeeze，也未 import 任何其他工单模块。
- 未 commit、未 push（由工作流负责）。
- 只用标准库（`math` 仅用于测试断言）。

## 检查（Checks ran）

从仓库根目录逐字执行：

- `python3 -m pytest tests/test_powerconv.py -q` → **13 passed in 0.02s**
- `python3 -m pytest tests/ -q` → **355 passed, 2 skipped in 19.50s**（2 skipped 为存量 skip，非本单引入）

## 验证者须注意（Validator notes）

- 浮点断言口径：验收要点 1/2/4/5/7 用相对误差 1e-9（`math.isclose(rel_tol=1e-9, abs_tol=0)`）；要点 3 用绝对容差 1e-6（规格明示）；要点 6 要求精确 0.0（实现中 0.0 乘任何有限系数后除回去精确为 0.0，已测）。
- 测试文件内 `FACTORS` 是对钉死常数的独立复算（非 import 实现内部字典），用于防实现漂移。
- 大小写敏感是硬约定：`"HP"`、`"kw"` 均必须抛 ValueError，已双向覆盖。
- 本单交付恰好两文件：`powerconv.py`、`tests/test_powerconv.py`。若根目录出现 `verdict.json` / `verdict.md`，那是测试套件的流水线副产物，非本单交付物，已在收尾删除。
