"""Pressure unit conversion with pascals (Pa) as the intermediary unit."""

_FACTORS = {
    "Pa": 1.0,
    "kPa": 1000.0,
    "bar": 100000.0,
    "atm": 101325.0,
    "psi": 6894.757293168,
    "mmHg": 133.322387415,
    "torr": 133.322387415,
    "inHg": 3386.389,
}


def convert(value, from_unit: str, to_unit: str) -> float:
    """Convert a pressure value between units, using pascals as intermediary.

    Raises TypeError for non-numeric values (bool is rejected) and
    ValueError for units not in the conversion table.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("value must be a numeric int or float")
    if from_unit not in _FACTORS:
        raise ValueError(f"unknown unit: {from_unit!r}")
    if to_unit not in _FACTORS:
        raise ValueError(f"unknown unit: {to_unit!r}")
    pascals = value * _FACTORS[from_unit]
    return pascals / _FACTORS[to_unit]
