"""Volume unit conversion using liters as the pivot unit.

Only the units and factors pinned by the work order are supported.
"""

__all__ = ["convert"]

# Unit -> factor in liters (US liquid measures where applicable).
_FACTORS = {
    "L": 1,
    "mL": 0.001,
    "m3": 1000,
    "cm3": 0.001,
    "gal": 3.785411784,
    "qt": 0.946352946,
    "pt": 0.473176473,
    "floz": 0.0295735295625,
    "cup": 0.2365882365,
    "tbsp": 0.01478676478125,
    "tsp": 0.00492892159375,
}


def convert(value, from_unit: str, to_unit: str) -> float:
    """Convert ``value`` from ``from_unit`` to ``to_unit`` via liters.

    ``value`` must be an int or float (bool is rejected). Both units must
    appear in the supported table, otherwise ValueError is raised.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(
            "value must be an int or float, got {}".format(type(value).__name__)
        )
    if not isinstance(from_unit, str) or from_unit not in _FACTORS:
        raise ValueError("unknown unit: {!r}".format(from_unit))
    if not isinstance(to_unit, str) or to_unit not in _FACTORS:
        raise ValueError("unknown unit: {!r}".format(to_unit))
    ratio = _FACTORS[from_unit] / _FACTORS[to_unit]
    return value * ratio
