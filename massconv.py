"""massconv: 质量单位换算（千克为中介）。

单位与千克的换算因子（1 单位 = 因子 千克）：
mg=1e-6, g=1e-3, kg=1, t=1000, oz=0.028349523125, lb=0.45359237, st=6.35029318。
未知单位抛 ValueError；value 非数值（含 bool）抛 TypeError。
"""

_KG_FACTORS = {
    "mg": 1e-6,
    "g": 1e-3,
    "kg": 1,
    "t": 1000,
    "oz": 0.028349523125,
    "lb": 0.45359237,
    "st": 6.35029318,
}


def mass_convert(value, from_unit: str, to_unit: str) -> float:
    """把 value 从 from_unit 换算为 to_unit，以千克为中介。

    value 必须是数值（int/float，bool 拒绝）；单位必须是已知单位。
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("value must be a real number, got %r" % (type(value).__name__,))
    if from_unit not in _KG_FACTORS:
        raise ValueError("unknown unit: %r" % (from_unit,))
    if to_unit not in _KG_FACTORS:
        raise ValueError("unknown unit: %r" % (to_unit,))
    kg = value * _KG_FACTORS[from_unit]
    return float(kg / _KG_FACTORS[to_unit])
