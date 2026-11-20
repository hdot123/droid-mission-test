"""rotate2d: 二维点绕任意中心的逆时针旋转（第五十轮 C 单 · 本单新增）。

本模块只依赖标准库，不 import 仓库内其它模块。
"""

import math

__all__ = ["rotate_point", "rotate_points"]


def _is_number(value):
    """数值判定：int/float，bool 拒。"""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _require_number(value, name):
    if not _is_number(value):
        raise TypeError("%s must be a real number, got %r" % (name, value))
    return value


def _require_center(center):
    """center 须为长度 2 的 list/tuple 且元素为数值，返回 (cx, cy)。"""
    if not isinstance(center, (list, tuple)) or len(center) != 2:
        raise TypeError(
            "center must be a list or tuple of length 2, got %r" % (center,)
        )
    cx, cy = center
    _require_number(cx, "center[0]")
    _require_number(cy, "center[1]")
    return cx, cy


def rotate_point(x, y, degrees, center=(0, 0)):
    """点 (x, y) 绕 center 逆时针旋转 degrees 度（数学正向），返回浮点二元组。

    以 c=(cx, cy)、θ 为弧度，dx = x-cx、dy = y-cy，结果 =
    (cx + dx·cosθ − dy·sinθ, cy + dx·sinθ + dy·cosθ)。

    校验：x／y／degrees 须为数值（int/float，bool 拒），否则 TypeError；
    center 须为长度 2 的 list/tuple 且元素为数值，否则 TypeError。
    """
    _require_number(x, "x")
    _require_number(y, "y")
    _require_number(degrees, "degrees")
    cx, cy = _require_center(center)
    theta = math.radians(degrees)
    dx = x - cx
    dy = y - cy
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    return (
        cx + dx * cos_theta - dy * sin_theta,
        cy + dx * sin_theta + dy * cos_theta,
    )


def rotate_points(points, degrees, center=(0, 0)):
    """逐点按 rotate_point 旋转，保序返回 list[tuple[float, float]]。

    points 须为 list/tuple，且每个元素为长度 2 的 list/tuple，否则 TypeError。
    """
    if not isinstance(points, (list, tuple)):
        raise TypeError(
            "points must be a list or tuple, got %r" % (type(points).__name__,)
        )
    _require_number(degrees, "degrees")
    _require_center(center)
    rotated = []
    for point in points:
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise TypeError(
                "each point must be a list or tuple of length 2, got %r" % (point,)
            )
        px, py = point
        rotated.append(rotate_point(px, py, degrees, center))
    return rotated
