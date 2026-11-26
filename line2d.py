"""line2d: 二维无限直线几何（单位法向量方程、点线距离、交点）。

本模块处理的是无限直线 Ax + By + C = 0（方程/距离/交点），与线段距离
（segdist）、布尔相交/包含判定（segintersect、pointinpoly）不同。

约定：
- 点为 (x, y) 数对，坐标接受 int/float；bool 与非数值抛 TypeError，
  形状坏（非数对或长度 != 2）抛 TypeError。
- 线为 (A, B, C) 三元组；``line_from_points`` 返回单位法向量形
  （A^2 + B^2 = 1）且符号钉死：A > 0，或 A = 0 且 B > 0。
"""

import math

__all__ = ["line_from_points", "point_line_distance", "lines_intersection"]

# 平行判定相对阈值（相对两线法向量长度之积）。
_PARALLEL_RTOL = 1e-12


def _coerce_number(value, what):
    """校验单个坐标/系数：只收 int/float，bool 与其它类型抛 TypeError。"""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("%s must be a real number (int/float), got %r" % (what, value))
    return float(value)


def _coerce_point(point, what="point"):
    """把入参校验成 (x, y) float 数对；形状坏或非数值抛 TypeError。"""
    if isinstance(point, (str, bytes)):
        raise TypeError("%s must be a (x, y) pair, got %r" % (what, point))
    try:
        length = len(point)
    except TypeError:
        raise TypeError("%s must be a (x, y) pair, got %r" % (what, point)) from None
    if length != 2:
        raise TypeError("%s must have length 2, got length %d" % (what, length))
    try:
        x = point[0]
        y = point[1]
    except TypeError:
        raise TypeError("%s must be an indexable (x, y) pair, got %r" % (what, point)) from None
    return (
        _coerce_number(x, "%s[0]" % what),
        _coerce_number(y, "%s[1]" % what),
    )


def _coerce_line(line, what="line"):
    """把入参校验成 (A, B, C) float 三元组；形状坏或非数值抛 TypeError。"""
    if isinstance(line, (str, bytes)):
        raise TypeError("%s must be an (A, B, C) triple, got %r" % (what, line))
    try:
        length = len(line)
    except TypeError:
        raise TypeError("%s must be an (A, B, C) triple, got %r" % (what, line)) from None
    if length != 3:
        raise TypeError("%s must have length 3, got length %d" % (what, length))
    try:
        a = line[0]
        b = line[1]
        c = line[2]
    except TypeError:
        raise TypeError("%s must be an indexable (A, B, C) triple, got %r" % (what, line)) from None
    return (
        _coerce_number(a, "%s[0]" % what),
        _coerce_number(b, "%s[1]" % what),
        _coerce_number(c, "%s[2]" % what),
    )


def _clean_zero(value):
    """把 -0.0 归一成 0.0（-0.0 == 0.0 为真，但输出更干净）。"""
    return 0.0 if value == 0.0 else value


def line_from_points(p, q):
    """过两点的直线，返回单位法向量形 (A, B, C)，满足 Ax + By + C = 0。

    A^2 + B^2 == 1，符号钉死：A > 0，或 A = 0 且 B > 0。
    两点重合抛 ValueError；点不合法（形状/类型）抛 TypeError。
    """
    x1, y1 = _coerce_point(p, "p")
    x2, y2 = _coerce_point(q, "q")
    if x1 == x2 and y1 == y2:
        raise ValueError("line_from_points requires two distinct points, got %r and %r" % (p, q))
    dx = x2 - x1
    dy = y2 - y1
    norm = math.hypot(dx, dy)
    # 与 (dx, dy) 垂直的法向量 (dy, -dx)，再单位化。
    a = dy / norm
    b = -dx / norm
    c = -(a * x1 + b * y1)
    # 符号钉死：A > 0；A == 0 时 B > 0。
    if a < 0.0 or (a == 0.0 and b < 0.0):
        a, b, c = -a, -b, -c
    return (_clean_zero(a), _clean_zero(b), _clean_zero(c))


def point_line_distance(p, line):
    """点到直线的距离；line 为任意 (A, B, C) 三元组，不要求归一化。"""
    x, y = _coerce_point(p)
    a, b, c = _coerce_line(line)
    norm = math.hypot(a, b)
    if norm == 0.0:
        raise ValueError("degenerate line: A and B are both zero")
    return abs(a * x + b * y + c) / norm


def lines_intersection(l1, l2):
    """两直线交点 (x, y)；平行或重合返回 None。"""
    a1, b1, c1 = _coerce_line(l1, "l1")
    a2, b2, c2 = _coerce_line(l2, "l2")
    det = a1 * b2 - a2 * b1
    scale = math.hypot(a1, b1) * math.hypot(a2, b2)
    if scale == 0.0:
        raise ValueError("degenerate line: A and B are both zero")
    if abs(det) <= _PARALLEL_RTOL * scale:
        return None
    x = (b1 * c2 - b2 * c1) / det
    y = (c1 * a2 - c2 * a1) / det
    return (_clean_zero(x), _clean_zero(y))
