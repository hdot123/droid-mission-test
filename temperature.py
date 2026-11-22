"""Temperature conversion helpers (Celsius, Fahrenheit, Kelvin)."""


def c_to_f(c):
    """Convert Celsius to Fahrenheit, returning a float."""
    return float(c) * 9.0 / 5.0 + 32.0


def f_to_c(f):
    """Convert Fahrenheit to Celsius, returning a float."""
    return (float(f) - 32.0) * 5.0 / 9.0


def c_to_k(c):
    """Convert Celsius to Kelvin, returning a float."""
    return float(c) + 273.15
