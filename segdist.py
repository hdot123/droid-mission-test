"""segdist: 点到线段的最短距离与最近点（第五十六轮 B 单）。

连续几何量：返回距离值与最近点坐标，不是布尔相交／包含判定。
仅用标准库，不 import 项目内其它模块。
"""

__all__ = ["point_segment_distance", "closest_point_on_segment"]


def closest_point_on_segment(px, py, ax, ay, bx, by):
    """线段 (ax, ay)-(bx, by) 上离点 (px, py) 最近的点。

    投影参数 t = ((p-a)·(b-a)) / |b-a|^2 钳制于 [0, 1]；
    退化线段（a == b）按点处理，返回 (ax, ay)。
    """
    dx = bx - ax
    dy = by - ay
    denom = dx * dx + dy * dy
    if denom == 0:
        return (float(ax), float(ay))
    t = ((px - ax) * dx + (py - ay) * dy) / denom
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    return (ax + t * dx, ay + t * dy)


def point_segment_distance(px, py, ax, ay, bx, by):
    """点 (px, py) 到线段 (ax, ay)-(bx, by) 的最短距离。

    投影参数钳制于 [0, 1]（垂足越界取端点距离）；
    退化线段（a == b）按点到点距离处理。
    """
    cx, cy = closest_point_on_segment(px, py, ax, ay, bx, by)
    ex = px - cx
    ey = py - cy
    return (ex * ex + ey * ey) ** 0.5
