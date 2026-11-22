"""angle: 角度换算工具（第四十二轮 · 并发 D 单）。

仅依赖标准库，不依赖仓库内其他模块。
"""

import math


def deg2rad(d: float) -> float:
    """角度转弧度，等价于 math.radians。"""
    return math.radians(d)


def rad2deg(r: float) -> float:
    """弧度转角度，等价于 math.degrees。"""
    return math.degrees(r)


def normalize_deg(d: float) -> float:
    """把角度规范到 [0, 360) 区间，等价于 d % 360，返回浮点数。"""
    return float(d % 360)
