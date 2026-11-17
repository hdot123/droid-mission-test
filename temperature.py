"""Temperature conversion helpers (Celsius, Fahrenheit, Kelvin)."""

_ABS_ZERO_C = -273.15
_ABS_ZERO_K = 0.0
_ABS_ZERO_F = -459.67


def c_to_f(c: float) -> float:
    """Convert Celsius to Fahrenheit. Returns float."""
    return float(c) * 9.0 / 5.0 + 32.0


def f_to_c(f: float) -> float:
    """Convert Fahrenheit to Celsius. Returns float.

    Raises ValueError if the result would be below absolute zero
    (i.e. f < -459.67).
    """
    c = (float(f) - 32.0) * 5.0 / 9.0
    if c < _ABS_ZERO_C:
        raise ValueError(f"temperature below absolute zero: {f} F")
    return c


def c_to_k(c: float) -> float:
    """Convert Celsius to Kelvin. Returns float.

    Raises ValueError if c < -273.15 (below absolute zero).
    """
    if float(c) < _ABS_ZERO_C:
        raise ValueError(f"temperature below absolute zero: {c} C")
    return float(c) + 273.15


def k_to_c(k: float) -> float:
    """Convert Kelvin to Celsius. Returns float.

    Raises ValueError if k < 0 (below absolute zero).
    """
    if float(k) < _ABS_ZERO_K:
        raise ValueError(f"temperature below absolute zero: {k} K")
    return float(k) - 273.15
