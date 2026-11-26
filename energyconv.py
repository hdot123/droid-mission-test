"""energyconv: 能量单位换算（第五十六轮 A 单）。

单位集 {J, kJ, cal, kcal, kWh, BTU}，基准单位为 J，换算因子钉死：

- kJ  = 1000
- cal = 4.184（热化学卡）
- kcal = 4184
- kWh = 3.6e6
- BTU = 1055.05585262（国际表）

本模块只做能量换算；BTU/h 等功率单位不在单位集内。
未知单位（含大小写不符，如 "j"）抛 ValueError；负值允许。
"""

# 单位 -> 相对 J 的换算因子（基准单位 J 自身为 1.0）。
_FACTORS_TO_J = {
    "J": 1.0,
    "kJ": 1000.0,
    "cal": 4.184,
    "kcal": 4184.0,
    "kWh": 3.6e6,
    "BTU": 1055.05585262,
}


def convert_energy(value, from_unit, to_unit) -> float:
    """把 value 从 from_unit 换算到 to_unit。

    参数：
        value: 数值（允许负值与 0）。
        from_unit: 源单位，必须是 {J, kJ, cal, kcal, kWh, BTU} 之一（大小写敏感）。
        to_unit: 目标单位，同上。

    返回换算后的浮点值。未知单位（含大小写不符）抛 ValueError。
    """
    try:
        factor_from = _FACTORS_TO_J[from_unit]
    except (KeyError, TypeError):
        raise ValueError(f"unknown unit: {from_unit!r}") from None
    try:
        factor_to = _FACTORS_TO_J[to_unit]
    except (KeyError, TypeError):
        raise ValueError(f"unknown unit: {to_unit!r}") from None
    return float(value) * factor_from / factor_to
