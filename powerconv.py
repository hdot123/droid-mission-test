"""powerconv: 功率单位换算工具。

单位集（钉死，基准 W）：
    W      = 1
    kW     = 1000
    hp     = 745.699872        （机械马力）
    PS     = 735.49875         （公制马力）
    BTU/h  = 1055.05585262/3600
    ftlbf/s = 1.3558179483314004

未知单位（含大小写不符）抛 ValueError；hp 与 PS 是两个不同常数，不得混用。
本模块只做功率换算（BTU/h 是功率单位）；BTU 是能量单位，不在本单位集内。
"""

# 每个单位相对基准 W 的换算系数（钉死常数）。
_FACTORS = {
    "W": 1.0,
    "kW": 1000.0,
    "hp": 745.699872,
    "PS": 735.49875,
    "BTU/h": 1055.05585262 / 3600.0,
    "ftlbf/s": 1.3558179483314004,
}


def convert_power(value, from_unit, to_unit):
    """把功率值从 from_unit 换算到 to_unit。

    value 参与浮点换算；单位必须精确匹配（区分大小写），
    未知单位（含大小写不符）抛 ValueError。
    """
    if from_unit not in _FACTORS:
        raise ValueError("unknown power unit: %r" % (from_unit,))
    if to_unit not in _FACTORS:
        raise ValueError("unknown power unit: %r" % (to_unit,))
    watts = float(value) * _FACTORS[from_unit]
    return watts / _FACTORS[to_unit]
