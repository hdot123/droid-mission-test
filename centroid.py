"""centroid: 多边形带符号面积与重心（第五十二轮并发 A 单）。

- `polygon_area(vertices)`: 鞋带公式带符号面积（逆时针为正、顺时针为负）。
- `polygon_centroid(vertices)`: 面积加权重心，带符号面积计算，顺/逆时针一致。

只用标准库；不 import 仓内其他模块。
"""

__all__ = ["polygon_area", "polygon_centroid"]


def _validate(vertices):
    """校验入参，返回顶点 (x, y) 列表；不合法抛 TypeError/ValueError。"""
    if not isinstance(vertices, (list, tuple)):
        raise TypeError(
            "vertices must be a list or tuple, got %s" % type(vertices).__name__
        )
    if len(vertices) < 3:
        raise ValueError("at least 3 vertices required, got %d" % len(vertices))
    points = []
    for vertex in vertices:
        if not isinstance(vertex, (list, tuple)) or len(vertex) != 2:
            raise TypeError(
                "each vertex must be a 2-item (x, y) pair, got %r" % (vertex,)
            )
        x, y = vertex
        for coord in (x, y):
            if isinstance(coord, bool) or not isinstance(coord, (int, float)):
                raise TypeError(
                    "coordinates must be int or float, got %r" % (coord,)
                )
        points.append((x, y))
    return points


def polygon_area(vertices):
    """鞋带公式带符号面积；共线退化返回 0.0。"""
    points = _validate(vertices)
    n = len(points)
    total = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        total += x1 * y2 - x2 * y1
    return float(total) * 0.5


def polygon_centroid(vertices):
    """面积加权重心 (Cx, Cy)；面积为 0（退化多边形）抛 ValueError。"""
    points = _validate(vertices)
    n = len(points)
    cross_sum = 0
    cx_num = 0.0
    cy_num = 0.0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        cross = x1 * y2 - x2 * y1
        cross_sum += cross
        cx_num += (x1 + x2) * cross
        cy_num += (y1 + y2) * cross
    if cross_sum == 0:
        raise ValueError("degenerate polygon: zero area")
    # Cx = sum((x1+x2)*cross) / (6A)，其中 A = cross_sum / 2，故除数为 3*cross_sum。
    return (cx_num / (3.0 * cross_sum), cy_num / (3.0 * cross_sum))
