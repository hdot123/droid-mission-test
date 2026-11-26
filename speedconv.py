"""speedconv: 速度单位换算。

单位集 {m/s, km/h, mph, kn, ft/s}，经基准 m/s 中转换算。
各系数为「每单位等于多少 m/s」，全精度钉死。
"""

# 每单位等于多少 m/s（全精度钉死）。
_FACTORS = {
    "m/s": 1.0,
    "km/h": 1 / 3.6,
    "mph": 1609.344 / 3600,
    "kn": 1852 / 3600,
    "ft/s": 0.3048,
}


def convert_speed(value, from_unit, to_unit) -> float:
    """把 value 从 from_unit 换算为 to_unit，返回 float。

    未知单位（含大小写不符，如 "MS"、"knots"、"fps"）抛 ValueError。
    """
    if from_unit not in _FACTORS:
        raise ValueError("unknown speed unit: %r" % (from_unit,))
    if to_unit not in _FACTORS:
        raise ValueError("unknown speed unit: %r" % (to_unit,))
    return value * _FACTORS[from_unit] / _FACTORS[to_unit]
