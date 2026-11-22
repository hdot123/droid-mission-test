"""windscale: 蒲福风级（按 km/h 风速分级）。

阈值钉死（单位 km/h，下限含、上限为下一级下限）：
0 级 <1；1 级 1–5；2 级 6–11；3 级 12–19；4 级 20–28；5 级 29–38；
6 级 39–49；7 级 50–61；8 级 62–74；9 级 75–88；10 级 89–102；
11 级 103–117；12 级 ≥118。
"""

#: 各级下限（km/h，含），索引即级数 0–12。
_THRESHOLDS = (0, 1, 6, 12, 20, 29, 39, 50, 62, 75, 89, 103, 118)

#: 0–12 级中文名。
_LABELS = (
    "无风",
    "软风",
    "轻风",
    "微风",
    "和风",
    "清风",
    "强风",
    "疾风",
    "大风",
    "烈风",
    "狂风",
    "暴风",
    "飓风",
)


def _validate_speed(speed_kmh):
    """校验入参：须为 int/float（bool 拒），负数抛 ValueError；返回数值。"""
    if isinstance(speed_kmh, bool) or not isinstance(speed_kmh, (int, float)):
        raise TypeError("speed_kmh must be int or float, got %r" % (speed_kmh,))
    if speed_kmh < 0:
        raise ValueError("speed_kmh must be non-negative, got %r" % (speed_kmh,))
    return speed_kmh


def beaufort(speed_kmh) -> int:
    """按 km/h 风速返回蒲福风级 0–12。

    speed 须为 int/float（bool 拒）；非数值抛 TypeError；负数抛 ValueError。
    """
    speed = _validate_speed(speed_kmh)
    level = 0
    for index, lower in enumerate(_THRESHOLDS):
        if speed >= lower:
            level = index
        else:
            break
    return level


def beaufort_label(speed_kmh) -> str:
    """按 km/h 风速返回蒲福风级中文名（0–12 级依次为 无风…飓风）。

    入参校验同 beaufort。
    """
    return _LABELS[beaufort(speed_kmh)]
