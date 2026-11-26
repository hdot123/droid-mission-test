"""Point-in-polygon three-state classification (ray-casting method).

``point_in_polygon`` returns one of ``"inside"``, ``"outside"`` or
``"boundary"``. Vertex order (CW or CCW) does not matter. A point lying on
any edge segment or coinciding with any vertex is classified as
``"boundary"``; the boundary test uses exact cross products so integer
coordinates are judged exactly.
"""

from __future__ import annotations

__all__ = ["point_in_polygon"]


def _on_segment(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> bool:
    """Exact collinearity + bounding-box test for point (px, py) on segment AB."""
    cross = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
    if cross != 0:
        return False
    # Collinear: check that the point lies within the segment's bounding box.
    if min(ax, bx) <= px <= max(ax, bx) and min(ay, by) <= py <= max(ay, by):
        return True
    return False


def point_in_polygon(x, y, polygon: list[tuple[float, float]]) -> str:
    """Classify (x, y) as "inside", "outside" or "boundary" of ``polygon``.

    Ray-casting method; works for CW and CCW vertex orders, convex and
    concave polygons. Fewer than 3 vertices raises ValueError.
    """
    if not isinstance(polygon, list) or len(polygon) < 3:
        raise ValueError("polygon must have at least 3 vertices")

    # 1. Boundary test: on an edge segment or coinciding with a vertex
    # (vertex coincidence is covered by the segment test since a segment
    # includes its endpoints).
    n = len(polygon)
    for i in range(n):
        ax, ay = polygon[i]
        bx, by = polygon[(i + 1) % n]
        if _on_segment(x, y, ax, ay, bx, by):
            return "boundary"

    # 2. Ray casting: cast a ray in +x direction and count crossings,
    # using the half-open rule (yi > y) != (yj > y) so vertices on the
    # ray are counted exactly once.
    inside = False
    for i in range(n):
        ax, ay = polygon[i]
        bx, by = polygon[(i + 1) % n]
        if (ay > y) != (by > y):
            # X coordinate of the intersection of edge AB with the horizontal
            # line through (x, y); compare against x to decide crossing.
            x_int = ax + (y - ay) * (bx - ax) / (by - ay)
            if x < x_int:
                inside = not inside

    return "inside" if inside else "outside"
