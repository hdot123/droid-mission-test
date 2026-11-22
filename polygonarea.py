"""Polygon shoelace area and closed perimeter helpers (round 44, part D)."""

import math

__all__ = ["polygon_area", "polygon_perimeter"]


def _validate(points, min_points):
    if not isinstance(points, (list, tuple)):
        raise TypeError("points must be a list of (x, y) numeric pairs")
    if len(points) < min_points:
        raise ValueError("not enough points")
    for point in points:
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise TypeError("each point must be an (x, y) pair")
        x, y = point
        if isinstance(x, bool) or isinstance(y, bool) or not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("point coordinates must be numeric")
        if isinstance(x, float) and not math.isfinite(x):
            raise TypeError("point coordinates must be finite")
        if isinstance(y, float) and not math.isfinite(y):
            raise TypeError("point coordinates must be finite")
    return points


def polygon_area(points):
    """Return the signed shoelace area (counter-clockwise positive)."""
    pts = _validate(points, 3)
    total = 0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        total += x1 * y2 - x2 * y1
    return total / 2.0


def polygon_perimeter(points):
    """Return the closed perimeter (last point connects back to the first)."""
    pts = _validate(points, 2)
    total = 0.0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        total += math.hypot(x2 - x1, y2 - y1)
    return total
