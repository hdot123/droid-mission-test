"""Ellipse geometry: area, perimeter (Ramanujan II), and eccentricity.

Standard library only. All three functions share one input-validation rule:
a and b must be numeric (int/float; bool rejected), finite, and > 0.
"""

import math

__all__ = ["ellipse_area", "ellipse_perimeter", "ellipse_eccentricity"]

_TOLERANCE = 1e-9


def _validate(a, b):
    """Shared validation: return (a, b) as floats, or raise."""
    for value in (a, b):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                "a and b must be numeric (int or float), got %r" % (value,)
            )
        if not math.isfinite(value):
            raise ValueError("a and b must be finite, got %r" % (value,))
        if value <= 0:
            raise ValueError("a and b must be > 0, got %r" % (value,))
    return float(a), float(b)


def ellipse_area(a, b) -> float:
    """Return the ellipse area: pi * a * b."""
    a, b = _validate(a, b)
    return math.pi * a * b


def ellipse_perimeter(a, b) -> float:
    """Return the ellipse perimeter via Ramanujan's second approximation.

    h = ((a - b) / (a + b)) ** 2
    perimeter = pi * (a + b) * (1 + 3h / (10 + sqrt(4 - 3h)))
    """
    a, b = _validate(a, b)
    h = ((a - b) / (a + b)) ** 2
    return math.pi * (a + b) * (1 + 3 * h / (10 + math.sqrt(4 - 3 * h)))


def ellipse_eccentricity(a, b) -> float:
    """Return the eccentricity sqrt(1 - (minor/major)**2); 0.0 when a == b."""
    a, b = _validate(a, b)
    major = max(a, b)
    minor = min(a, b)
    return math.sqrt(1 - (minor / major) ** 2)
