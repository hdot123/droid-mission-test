"""lensarea：双圆交叠（透镜）面积计算。

两圆半径 r1、r2、圆心距 d 的交叠面积。边界归属钉死：
- 外切（d == r1 + r2）与分离：恰返 0.0；
- 内切/包含（d <= |r1 - r2|）：恰返小圆全面积 π·min(r1, r2)²，
  不得在边界处返回近似小量或 NaN；
- 两圆互换（r1 ↔ r2）结果不变。

入参约定：任一入参为负抛 ValueError；非数值（含 bool）抛 TypeError；
半径为 0 合法（面积 0.0）。只用标准库。
"""

import math

__all__ = ["lens_area"]


def _as_float(value, name):
    """把入参收敛为 float；非数值（含 bool）抛 TypeError。"""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("%s must be a real number, got %r" % (name, value))
    return float(value)


def lens_area(r1, r2, d):
    """Return the overlap (lens) area of two circles.

    r1、r2 为两圆半径，d 为圆心距，均须为非负实数（bool 拒收）。
    两圆分离或外切恰返 0.0；内切或包含恰返 math.pi * min(r1, r2) ** 2；
    半径为 0 合法，返 0.0。浮点验收相对误差 1e-9。
    """
    r1 = _as_float(r1, "r1")
    r2 = _as_float(r2, "r2")
    d = _as_float(d, "d")
    if r1 < 0.0 or r2 < 0.0 or d < 0.0:
        raise ValueError(
            "arguments must be non-negative, got r1=%r r2=%r d=%r" % (r1, r2, d)
        )
    if r1 == 0.0 or r2 == 0.0:
        return 0.0
    if d >= r1 + r2:
        # 外切与分离：恰 0.0（先判边界，避免通用式在边界处出 NaN）
        return 0.0
    if d <= abs(r1 - r2):
        # 内切与包含：恰为小圆全面积
        small = r1 if r1 < r2 else r2
        return math.pi * small * small
    # 严格交叠：两弓形（扇形 − 三角）合成的闭式
    d2 = d * d
    r1sq = r1 * r1
    r2sq = r2 * r2
    cos1 = (d2 + r1sq - r2sq) / (2.0 * d * r1)
    cos2 = (d2 + r2sq - r1sq) / (2.0 * d * r2)
    if cos1 > 1.0:
        cos1 = 1.0
    elif cos1 < -1.0:
        cos1 = -1.0
    if cos2 > 1.0:
        cos2 = 1.0
    elif cos2 < -1.0:
        cos2 = -1.0
    # 共弦两三角形面积之和的两倍（Heron 形式），浮点漂移时下截 0
    tri_sq = (r1 + r2 - d) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2)
    if tri_sq < 0.0:
        tri_sq = 0.0
    area = r1sq * math.acos(cos1) + r2sq * math.acos(cos2) - 0.5 * math.sqrt(tri_sq)
    if area < 0.0:
        return 0.0
    return area
