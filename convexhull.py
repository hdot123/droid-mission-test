"""convexhull: 二维凸包（单调链法 / Andrew monotone chain）。

`convex_hull(points)` 接受 (x, y) 数值对的 list/tuple，返回凸包顶点，
按逆时针排列，起点为 x 最小（x 相同取 y 最小）的点；边上共线点只保留
端点；重复点先去重。去重点少于 3 个时返回去重排序后的点。
"""

from numbers import Number


def _is_number(value):
    """坐标须为数值；bool 虽是 int 子类，但按规范拒绝。"""
    return isinstance(value, Number) and not isinstance(value, bool)


def _cross(origin, a, b):
    """向量 oa 与 ob 的二维叉积（z 分量）。"""
    return (a[0] - origin[0]) * (b[1] - origin[1]) - (
        a[1] - origin[1]
    ) * (b[0] - origin[0])


def convex_hull(points):
    """返回 points 的凸包顶点（逆时针，起点为最左下点）。

    - points 必须是 list/tuple，否则 TypeError；
    - 每个点必须是二元组，否则 ValueError；
    - 坐标必须是数值（bool 拒绝），否则 TypeError；
    - 边上共线点只保留端点，重复点先去重；
    - 去重点少于 3 个时返回去重排序后的点。
    """
    if not isinstance(points, (list, tuple)):
        raise TypeError("points must be a list or tuple: %r" % (points,))

    unique = set()
    for point in points:
        if not isinstance(point, tuple) or len(point) != 2:
            raise ValueError("point must be a 2-tuple: %r" % (point,))
        x, y = point
        if not _is_number(x) or not _is_number(y):
            raise TypeError(
                "point coordinates must be numeric: %r" % (point,)
            )
        unique.add(point)

    ordered = sorted(unique)
    if len(ordered) < 3:
        return ordered

    lower = []
    for point in ordered:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)

    upper = []
    for point in reversed(ordered):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)

    # 每条链的末点是另一条链的首点，去掉以免重复。
    return lower[:-1] + upper[:-1]
