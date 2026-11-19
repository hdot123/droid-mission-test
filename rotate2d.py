"""rotate2d: 二维点绕中心的逆时针旋转（标准库实现）。"""

import math

__all__ = ["rotate_point", "rotate_points"]


def _is_number(value):
    """仅接受 int/float 数值，拒绝 bool 及其他类型。"""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check_number(value, name):
    if not _is_number(value):
        raise TypeError("%s must be a number, got %r" % (name, value))
    return value


def _check_center(center):
    if not isinstance(center, (list, tuple)):
        raise TypeError("center must be a list or tuple, got %r" % (center,))
    if len(center) != 2:
        raise TypeError("center must have length 2, got length %d" % len(center))
    cx = _check_number(center[0], "center[0]")
    cy = _check_number(center[1], "center[1]")
    return cx, cy


def rotate_point(x, y, degrees, center=(0, 0)):
    """把点 (x, y) 绕 center 逆时针旋转 degrees 度，返回浮点二元组。

    x／y／degrees 必须是数值（int/float，bool 拒），center 必须是长度 2 且
    元素为数值的 list/tuple，否则抛 TypeError。浮点容差 1e-9。
    """
    _check_number(x, "x")
    _check_number(y, "y")
    _check_number(degrees, "degrees")
    cx, cy = _check_center(center)
    theta = math.radians(degrees)
    dx = x - cx
    dy = y - cy
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    rx = cx + dx * cos_t - dy * sin_t
    ry = cy + dx * sin_t + dy * cos_t
    return (float(rx), float(ry))


def rotate_points(points, degrees, center=(0, 0)):
    """按 rotate_point 逐点旋转，保序返回浮点二元组列表。

    points 须为 list/tuple，且每个元素为长度 2 的 list/tuple，否则抛
    TypeError。degrees／center 的校验与 rotate_point 相同。
    """
    if not isinstance(points, (list, tuple)):
        raise TypeError("points must be a list or tuple, got %r" % (points,))
    result = []
    for index, point in enumerate(points):
        if not isinstance(point, (list, tuple)):
            raise TypeError(
                "points[%d] must be a list or tuple, got %r" % (index, point)
            )
        if len(point) != 2:
            raise TypeError(
                "points[%d] must have length 2, got length %d" % (index, len(point))
            )
        result.append(rotate_point(point[0], point[1], degrees, center))
    return result
