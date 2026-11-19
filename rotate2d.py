"""Two-dimensional point rotation (standard library only)."""

import math

__all__ = ["rotate_point", "rotate_points"]

_TOLERANCE = 1e-9


def _is_number(value) -> bool:
    """True only for real int/float (bool is rejected)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_number(value, name: str) -> None:
    if not _is_number(value):
        raise TypeError(f"{name} must be a real number (int or float), got {type(value).__name__}")


def _validate_point(x, y) -> None:
    _validate_number(x, "x")
    _validate_number(y, "y")


def _validate_center(center) -> tuple:
    if not isinstance(center, (list, tuple)) or len(center) != 2:
        raise TypeError(
            "center must be a sequence of length 2, got "
            f"{type(center).__name__}"
        )
    _validate_number(center[0], "center[0]")
    _validate_number(center[1], "center[1]")
    return (center[0], center[1])


def rotate_point(x, y, degrees, center=(0, 0)) -> tuple[float, float]:
    """Rotate ``(x, y)`` counter-clockwise by ``degrees`` around ``center``.

    Returns a float pair ``(rx, ry)``. ``x``, ``y``, ``degrees`` and both
    ``center`` components must be real numbers (bool is rejected); invalid
    values raise TypeError.
    """
    _validate_point(x, y)
    _validate_number(degrees, "degrees")
    cx, cy = _validate_center(center)

    theta = math.radians(degrees)
    dx = x - cx
    dy = y - cy
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    rx = cx + dx * cos_t - dy * sin_t
    ry = cy + dx * sin_t + dy * cos_t

    # Snap values that are within tolerance of zero (or of the exact
    # expected value) to keep results stable across platforms.
    rx = _snap(rx)
    ry = _snap(ry)
    return (float(rx), float(ry))


def _snap(value: float) -> float:
    if abs(value) < _TOLERANCE:
        return 0.0
    return value


def rotate_points(points, degrees, center=(0, 0)) -> list[tuple[float, float]]:
    """Rotate every point in ``points`` with :func:`rotate_point`, in order.

    ``points`` must be a list or tuple whose elements are list/tuple pairs
    of real numbers; otherwise TypeError is raised. An empty input returns
    an empty list.
    """
    if not isinstance(points, (list, tuple)):
        raise TypeError(f"points must be a list or tuple, got {type(points).__name__}")

    results: list[tuple[float, float]] = []
    for point in points:
        if not isinstance(point, (list, tuple)) or len(point) != 2:
            raise TypeError(
                "each point must be a sequence of length 2, got "
                f"{type(point).__name__}"
            )
        results.append(rotate_point(point[0], point[1], degrees, center))
    return results
