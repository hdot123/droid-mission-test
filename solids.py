"""Common solid geometry: volume and surface area.

Standard library only. Every dimension argument must be a positive
int/float (bool rejected): non-numeric raises TypeError, values <= 0
raise ValueError. Results are floats computed with math.pi.
"""

import math

__all__ = [
    "sphere_volume",
    "sphere_surface",
    "cylinder_volume",
    "cylinder_surface",
    "cone_volume",
    "cone_surface",
    "box_volume",
    "box_surface",
    "pyramid_volume",
    "pyramid_surface",
]


def _dim(value, name):
    """Validate one dimension: real number (bool rejected) and > 0."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(
            f"{name} must be a real number, got {type(value).__name__}"
        )
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value!r}")
    return value


def sphere_volume(r):
    """Volume of a sphere: V = 4*pi*r^3/3."""
    r = _dim(r, "r")
    return 4.0 * math.pi * r**3 / 3.0


def sphere_surface(r):
    """Surface area of a sphere: S = 4*pi*r^2."""
    r = _dim(r, "r")
    return 4.0 * math.pi * r**2


def cylinder_volume(r, h):
    """Volume of a cylinder: V = pi*r^2*h."""
    r = _dim(r, "r")
    h = _dim(h, "h")
    return math.pi * r**2 * h


def cylinder_surface(r, h):
    """Surface area of a closed cylinder: S = 2*pi*r^2 + 2*pi*r*h."""
    r = _dim(r, "r")
    h = _dim(h, "h")
    return 2.0 * math.pi * r**2 + 2.0 * math.pi * r * h


def cone_volume(r, h):
    """Volume of a cone: V = pi*r^2*h/3."""
    r = _dim(r, "r")
    h = _dim(h, "h")
    return math.pi * r**2 * h / 3.0


def cone_surface(r, h):
    """Surface area of a cone including its base.

    Slant height is sqrt(r^2 + h^2); S = pi*r^2 + pi*r*slant.
    """
    r = _dim(r, "r")
    h = _dim(h, "h")
    slant = math.sqrt(r**2 + h**2)
    return math.pi * r**2 + math.pi * r * slant


def box_volume(l, w, h):
    """Volume of a rectangular box: V = l*w*h."""
    l = _dim(l, "l")
    w = _dim(w, "w")
    h = _dim(h, "h")
    return float(l * w * h)


def box_surface(l, w, h):
    """Surface area of a rectangular box: S = 2*(l*w + l*h + w*h)."""
    l = _dim(l, "l")
    w = _dim(w, "w")
    h = _dim(h, "h")
    return float(2.0 * (l * w + l * h + w * h))


def pyramid_volume(b, h):
    """Volume of a regular square pyramid: V = b^2*h/3."""
    b = _dim(b, "b")
    h = _dim(h, "h")
    return b**2 * h / 3.0


def pyramid_surface(b, h):
    """Surface area of a regular square pyramid.

    Base is a square of side b; S = b^2 + 2*b*slant, where the triangle
    slant height is sqrt((b/2)^2 + h^2).
    """
    b = _dim(b, "b")
    h = _dim(h, "h")
    slant = math.sqrt((b / 2.0) ** 2 + h**2)
    return b**2 + 2.0 * b * slant
