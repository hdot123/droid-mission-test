"""Bezier curve evaluation via de Casteljau recursion.

Public API:
    bezier_point(points, t) -> tuple[float, float]
    bezier_curve(points, samples) -> list[tuple[float, float]]

Standard library only; no imports from sibling modules.
"""

__all__ = ["bezier_point", "bezier_curve"]


def _is_number(value):
    """Numeric check: int/float accepted, bool excluded."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_points(points):
    """Validate the control point list and return it as float pairs.

    Raises TypeError for a non-list container or malformed points,
    ValueError when there are fewer than 2 control points.
    """
    if not isinstance(points, list):
        raise TypeError("points must be a list of (x, y) pairs")
    for point in points:
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise TypeError("each control point must be a length-2 pair")
        for coordinate in point:
            if not _is_number(coordinate):
                raise TypeError("control point coordinates must be numeric")
    if len(points) < 2:
        raise ValueError("at least 2 control points are required")
    return [(float(x), float(y)) for x, y in points]


def bezier_point(points, t):
    """Return the Bezier curve point at parameter t in [0, 1].

    Uses de Casteljau linear interpolation, which lands exactly on the
    first/last control point at t = 0 / t = 1.
    """
    control = _validate_points(points)
    if not _is_number(t):
        raise TypeError("t must be numeric")
    t = float(t)
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be within [0, 1]")
    # de Casteljau: repeatedly lerp adjacent points until one remains.
    # lerp(a, b, u) = a * (1 - u) + b * u is exact at u = 0 and u = 1.
    current = control
    while len(current) > 1:
        current = [
            (
                a[0] * (1.0 - t) + b[0] * t,
                a[1] * (1.0 - t) + b[1] * t,
            )
            for a, b in zip(current, current[1:])
        ]
    return current[0]


def bezier_curve(points, samples):
    """Return `samples` equally spaced points on [0, 1], both ends included."""
    control = _validate_points(points)
    if isinstance(samples, bool) or not isinstance(samples, int):
        raise TypeError("samples must be an int")
    if samples < 2:
        raise ValueError("samples must be at least 2")
    denominator = samples - 1
    return [bezier_point(control, i / denominator) for i in range(samples)]
