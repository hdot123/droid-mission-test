"""Length unit conversion via meters as the pivot unit."""

from fractions import Fraction

# Exact conversion factors to meters: in = 0.0254 m, ft = 0.3048 m,
# yd = 0.9144 m, mi = 1609.344 m; mm = 0.001, cm = 0.01, km = 1000.
TO_METERS = {
    "mm": Fraction(1, 1000),
    "cm": Fraction(1, 100),
    "m": Fraction(1, 1),
    "km": Fraction(1000, 1),
    "in": Fraction(254, 10000),
    "ft": Fraction(3048, 10000),
    "yd": Fraction(9144, 10000),
    "mi": Fraction(1609344, 1000),
}


def convert(value, from_unit, to_unit) -> float:
    """Convert ``value`` from ``from_unit`` to ``to_unit`` using meters as pivot."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("value must be a number (bool is not accepted)")
    if from_unit not in TO_METERS:
        raise ValueError(f"unknown unit: {from_unit!r}")
    if to_unit not in TO_METERS:
        raise ValueError(f"unknown unit: {to_unit!r}")
    amount = Fraction(str(value)) if isinstance(value, float) else Fraction(value)
    meters = amount * TO_METERS[from_unit]
    return float(meters / TO_METERS[to_unit])
