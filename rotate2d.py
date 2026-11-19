"""2D point rotation: rotate a point (or list of points) counterclockwise."""

import math

__all__ = ["rotate_point", "rotate_points"]


def _is_number(value) -> bool:
    """True for int/float, but False for bool (bool is rejected)."""
    if isinstance(value, bool):
        return False
    return isinstance(value, (int, float))


def _check_number(value, name: str) -> float:
    if not _is_number(value):
        raise TypeError(f"{name} must be a numeric value (int/float), got {type(value).__name__}")
    return value


def _check_center(center):
    if not isinstance(center, (list, tuple)):
        raise TypeError(
            f"center must be a list or tuple of length 2, got {type(center).__name__}"
        )
    if len(center) != 2:
        raise TypeError(f"center must have length 2, got length {len(center)}")
    cx, cy = center
    _check_number(cx, "center[0]")
    _check_number(cy, "center[1]")
    return cx, cy


def rotate_point(x, y, degrees, center=(0, 0)) -> tuple[float, float]:
    """Rotate point (x, y) counterclockwise (math-positive) by *degrees*
    around *center*, returning a float pair.

    Formula: with c = (cx, cy), theta in radians, dx = x - cx, dy = y - cy,
    result = (cx + dx*cos(theta) - dy*sin(theta),
              cy + dx*sin(theta) + dy*cos(theta)).
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


def rotate_points(points, degrees, center=(0, 0)) -> list[tuple[float, float]]:
    """Rotate each point in *points* via :func:`rotate_point`, preserving order.

    *points* must be a list/tuple and every element a length-2 list/tuple,
    otherwise TypeError is raised.
    """
    if not isinstance(points, (list, tuple)):
        raise TypeError(
            f"points must be a list or tuple, got {type(points).__name__}"
        )
    result: list[tuple[float, float]] = []
    for i, pt in enumerate(points):
        if not isinstance(pt, (list, tuple)):
            raise TypeError(
                f"points[{i}] must be a list or tuple of length 2, "
                f"got {type(pt).__name__}"
            )
        if len(pt) != 2:
            raise TypeError(
                f"points[{i}] must have length 2, got length {len(pt)}"
            )
        px, py = pt
        result.append(rotate_point(px, py, degrees, center=center))
    return result
