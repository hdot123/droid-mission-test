"""CSS length unit conversion (px, pt, pc, in, cm, mm, em, rem).

Conversion goes through px as the intermediary. The px factor for each unit
is pinned: px = 1; in = dpi; pt = dpi / 72; pc = dpi / 6; cm = dpi / 2.54;
mm = dpi / 25.4; em = base_font_px; rem = base_font_px.

Standard library only.
"""

import math

UNITS = frozenset({"px", "pt", "pc", "in", "cm", "mm", "em", "rem"})


def _is_number(x):
    """True for int/float but not bool."""
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _px_factor(unit, base_font_px, dpi):
    if unit == "px":
        return 1.0
    if unit == "in":
        return float(dpi)
    if unit == "pt":
        return dpi / 72
    if unit == "pc":
        return dpi / 6
    if unit == "cm":
        return dpi / 2.54
    if unit == "mm":
        return dpi / 25.4
    if unit in ("em", "rem"):
        return float(base_font_px)
    raise ValueError("unknown CSS unit: %r" % (unit,))


def css_convert(value, from_unit, to_unit, base_font_px=16.0, dpi=96.0):
    """Convert ``value`` from ``from_unit`` to ``to_unit``.

    Returns a float with no rounding. Raises TypeError for non-numeric or
    non-string inputs, ValueError for unknown units or non-positive
    base_font_px / dpi.
    """
    if not _is_number(value):
        raise TypeError("value must be a number, got %r" % (type(value).__name__,))
    if not math.isfinite(value):
        raise TypeError("value must be finite")

    if not isinstance(from_unit, str):
        raise TypeError(
            "from_unit must be a str, got %r" % (type(from_unit).__name__,)
        )
    if not isinstance(to_unit, str):
        raise TypeError("to_unit must be a str, got %r" % (type(to_unit).__name__,))
    if from_unit not in UNITS:
        raise ValueError("unknown CSS unit: %r" % (from_unit,))
    if to_unit not in UNITS:
        raise ValueError("unknown CSS unit: %r" % (to_unit,))

    if not _is_number(base_font_px):
        raise TypeError(
            "base_font_px must be a number, got %r" % (type(base_font_px).__name__,)
        )
    if not math.isfinite(base_font_px):
        raise TypeError("base_font_px must be finite")
    if base_font_px <= 0:
        raise ValueError("base_font_px must be > 0")

    if not _is_number(dpi):
        raise TypeError("dpi must be a number, got %r" % (type(dpi).__name__,))
    if not math.isfinite(dpi):
        raise TypeError("dpi must be finite")
    if dpi <= 0:
        raise ValueError("dpi must be > 0")

    result = float(value) * _px_factor(from_unit, base_font_px, dpi)
    result = result / _px_factor(to_unit, base_font_px, dpi)
    return float(result)
