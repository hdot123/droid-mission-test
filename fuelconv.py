"""fuelconv: 燃油消耗换算（倒数式）。

单位集 {L/100km, mpgUS, mpgImp, km/L}。本族是换算族中唯一的**倒数式**关系：
油耗数值越大越费油、mpg 越大越省油，两侧互为倒数，不是线性缩放
（与 speedconv 等线性换算函数不同）；mpgUS 与 mpgImp 因子不同（加仑定义不同），
不得混用。

因子由三个定义值导出：美制加仑 = 3.785411784 L、英制加仑 = 4.54609 L、
英里 = 1.609344 km：
    mpgUS  = 100 * 3.785411784 / 1.609344 = 235.214583… / (L/100km)
    mpgImp = 100 * 4.54609 / 1.609344     = 282.480936… / (L/100km)
    km/L   = 100 / (L/100km)
"""

from numbers import Real

US_GALLON_L = 3.785411784
IMPERIAL_GALLON_L = 4.54609
MILE_KM = 1.609344

# 倒数式因子（相对规范单位 L/100km）。L/100km 自身为恒等（不走倒数）。
_MPG_US = 100.0 * US_GALLON_L / MILE_KM  # 235.214583…
_MPG_IMP = 100.0 * IMPERIAL_GALLON_L / MILE_KM  # 282.480936…
_KM_PER_L = 100.0

_UNITS = ("L/100km", "mpgUS", "mpgImp", "km/L")


def _to_canonical(value, unit):
    """把某单位数值折算到规范单位 L/100km（倒数式一侧走除法）。"""
    if unit == "L/100km":
        return value
    if unit == "mpgUS":
        return _MPG_US / value
    if unit == "mpgImp":
        return _MPG_IMP / value
    if unit == "km/L":
        return _KM_PER_L / value
    raise ValueError("unknown fuel unit: %r" % (unit,))


def _from_canonical(value, unit):
    """把规范单位 L/100km 折算到目标单位（倒数式一侧走除法）。"""
    if unit == "L/100km":
        return value
    if unit == "mpgUS":
        return _MPG_US / value
    if unit == "mpgImp":
        return _MPG_IMP / value
    if unit == "km/L":
        return _KM_PER_L / value
    raise ValueError("unknown fuel unit: %r" % (unit,))


def convert_fuel(value, from_unit, to_unit):
    """把油耗/油效数值从 from_unit 换算到 to_unit，返回 float。

    - value <= 0 抛 ValueError；value 非数值（含 bool）抛 TypeError；
      未知单位抛 ValueError。
    - 倒数式换算：先折算到规范单位 L/100km，再从规范单位折算到目标单位。
    """
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(
            "value must be a real number, got %s" % type(value).__name__
        )
    if value <= 0:
        raise ValueError("value must be > 0, got %r" % (value,))
    canonical = _to_canonical(value, from_unit)
    return float(_from_canonical(canonical, to_unit))
