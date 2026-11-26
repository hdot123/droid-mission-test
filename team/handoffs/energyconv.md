# Handoff: energyconv（#892）

## 请求

子工单 #892（工单 #876 第56轮 A 单）：只新增两个文件——`energyconv.py`（能量单位换算实现）与 `tests/test_energyconv.py`（其测试）。不改任何存量文件；只用标准库；不 import kruskal/unaccent。单位集 {J, kJ, cal, kcal, kWh, BTU}，基准 J，因子钉死：kJ=1000、cal=4.184、kcal=4184、kWh=3.6e6、BTU=1055.05585262。未知单位（含大小写不符如 "j"）抛 ValueError；负值允许。浮点验收相对误差 1e-9（kWh→BTU 点容差 5×10⁻⁵）。这是能量换算；C 单 powerconv（功率换算）单位集不相交，不在本单范围。

## 做了什么

- 新增 `energyconv.py`：`convert_energy(value, from_unit, to_unit) -> float`，`_FACTORS_TO_J` 因子表按上述钉死值；未知单位或非字符串单位用 `KeyError`/`TypeError` 捕获后统一抛 `ValueError`；换算走 `value * factor_from / factor_to`，负值与 0 天然支持。
- 新增 `tests/test_energyconv.py`：11 个测试，覆盖全部验收要点——cal→J、kcal→kJ、kWh→kJ、kWh→BTU（5×10⁻⁵ 容差）、BTU→kJ(100)、负值 -5 kJ→J、0 BTU→cal、六单位恒等 `convert_energy(1,u,u)≈1`、经 kWh 中介的换算链一致性（相对误差 1e-9）、"J"→"erg" 与 "j"→"J" 抛 ValueError。

## 没做什么

- 未修改任何存量文件；未创建/修改 kruskal.py、unaccent.py 或其测试；未 commit/push；未触碰 verdict.json/verdict.md（全量测试运行后本就不存在，已确认无残留）。

## checks

- `python3 -m pytest tests/test_energyconv.py -q` → 11 passed
- `python3 -m pytest tests/ -q` → 353 passed, 2 skipped（跳过为存量 suite 自带，与本单无关）

## 验证者注意

- 单位大小写敏感："j" 必须抛 ValueError（已在测试覆盖）。
- kWh→BTU 点用 5×10⁻⁵ 容差（不是 1e-9），其余点均 1e-9。
- 测试里的 `close()` 对 expected==0 用绝对相等，其余用相对误差。
- `tests/` 全量里有两个存量 skip，非本单引入。
