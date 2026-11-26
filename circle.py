"""circle: 圆、扇形与弓形面积计算（第五十七轮 C 单）。

- `circle_area(r)` 圆面积 πr²；`circle_circumference(r)` 周长 2πr。
- `sector_area(r, angle_deg)` 扇形面积，角度口径为度：πr²·a/360。
- `segment_area(r, angle_deg)` 弓形面积 = 扇形 − 等腰三角形
  = (θ − sinθ)·r²/2，其中 θ 为弧度。180° 弓形恰为半圆，360° 弓形恰为整圆。

入参约定：r < 0 抛 ValueError（r = 0 合法、面积为 0）；角度不在 [0, 360]
抛 ValueError；非数值（含 bool）抛 TypeError。
"""

import math


def _check_number(value, name):
    """数值校验：bool 与非数值抛 TypeError。"""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("%s must be a number, got %r" % (name, value))
    return float(value)


def _check_radius(r):
    """半径校验：数值（非 bool），且 r >= 0。"""
    r = _check_number(r, "r")
    if r < 0:
        raise ValueError("radius must be >= 0, got %r" % (r,))
    return r


def _check_angle(angle_deg):
    """角度校验：数值（非 bool），且 0 <= angle_deg <= 360。"""
    angle_deg = _check_number(angle_deg, "angle_deg")
    if not 0.0 <= angle_deg <= 360.0:
        raise ValueError("angle_deg must be in [0, 360], got %r" % (angle_deg,))
    return angle_deg


def circle_area(r) -> float:
    """圆面积 πr²；r = 0 合法，面积为 0。"""
    r = _check_radius(r)
    return math.pi * r * r


def circle_circumference(r) -> float:
    """圆周长 2πr；r = 0 合法，周长为 0。"""
    r = _check_radius(r)
    return 2.0 * math.pi * r


def sector_area(r, angle_deg) -> float:
    """扇形面积 πr²·a/360，角度 a 以度为单位。"""
    r = _check_radius(r)
    angle_deg = _check_angle(angle_deg)
    return math.pi * r * r * angle_deg / 360.0


def segment_area(r, angle_deg) -> float:
    """弓形面积 = 扇形 − 等腰三角形 = (θ − sinθ)·r²/2，θ 为弧度。"""
    r = _check_radius(r)
    angle_deg = _check_angle(angle_deg)
    theta = math.radians(angle_deg)
    return (theta - math.sin(theta)) * r * r / 2.0
