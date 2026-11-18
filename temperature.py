"""Temperature conversion helpers (Celsius, Fahrenheit, Kelvin)."""


def c_to_f(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return c * 9.0 / 5.0 + 32.0


def f_to_c(f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (f - 32.0) * 5.0 / 9.0


def c_to_k(c: float) -> float:
    """Convert Celsius to Kelvin."""
    return c + 273.15
