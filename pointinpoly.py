"""Point-in-polygon three-state classification (ray casting).

``point_in_polygon`` returns one of ``"inside"``, ``"outside"`` or
``"boundary"``.  Vertex order (CW or CCW) does not matter.  The boundary
state covers both points lying on an edge segment and points coinciding
with a vertex.  Judgement is exact for integer coordinates: all
arithmetic that decides the result is done with integer cross products,
never with floating point division.
"""


def _on_segment(px, py, x1, y1, x2, y2):
    """True iff (px, py) lies on the closed segment (x1,y1)-(x2,y2)."""
    cross = (px - x1) * (y2 - y1) - (py - y1) * (x2 - x1)
    if cross != 0:
        return False
    return min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2)


def point_in_polygon(x, y, polygon: list[tuple[float, float]]) -> str:
    """Classify (x, y) against ``polygon`` as "inside"/"outside"/"boundary".

    Ray-casting method: shoot a ray in the +x direction and count edge
    crossings.  Before the parity test, an explicit collinearity test
    detects points on an edge or on a vertex, which are "boundary".

    Raises ValueError when the polygon has fewer than 3 vertices.
    """
    if len(polygon) < 3:
        raise ValueError("polygon must have at least 3 vertices")

    inside = False
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        if _on_segment(x, y, x1, y1, x2, y2):
            return "boundary"

        # Does the edge straddle the horizontal line through (x, y)?
        if (y1 > y) != (y2 > y):
            # x-intersection > x, evaluated without division so integer
            # inputs stay exact:
            #   x1 + (y-y1)*(x2-x1)/(y2-y1) > x
            den = y2 - y1  # non-zero here (straddle implies y1 != y2)
            num = (y - y1) * (x2 - x1)
            lhs = (x1 - x) * den + num
            if (lhs > 0) if den > 0 else (lhs < 0):
                inside = not inside

    return "inside" if inside else "outside"
