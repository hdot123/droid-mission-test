"""speedconv: 速度单位换算（第五十五轮并发 C 单）。

单位集 {m/s, km/h, mph, kn, ft/s}，经基准 m/s 中转换算。
各单位「每单位等于多少 m/s」的系数全精度钉死：
    m/s  = 1
    km/h = 1/3.6
    mph  = 1609.344/3600
    kn   = 1852/3600
    ft/s = 0.3048
未知单位（含大小写不符，如 "MS"、"knots"、"fps"）抛 ValueError。
浮点验收相对误差 1e-9。
"""

__all__ = ["convert_speed"]

# 每单位等于多少 m/s；键必须逐字精确（大小写敏感）。
_TO_METERS_PER_SECOND = {
    "m/s": 1,
    "km/h": 1 / 3.6,
    "mph": 1609.344 / 3600,
    "kn": 1852 / 3600,
    "ft/s": 0.3048,
}


def convert_speed(value, from_unit, to_unit):
    """把 value 从 from_unit 换算到 to_unit，返回 float。

    未知单位（含大小写不符）抛 ValueError。
    """
    try:
        factor_from = _TO_METERS_PER_SECOND[from_unit]
    except (KeyError, TypeError):
        raise ValueError("unknown speed unit: %r" % (from_unit,)) from None
    try:
        factor_to = _TO_METERS_PER_SECOND[to_unit]
    except (KeyError, TypeError):
        raise ValueError("unknown speed unit: %r" % (to_unit,)) from None
    return float(value) * factor_from / factor_to
