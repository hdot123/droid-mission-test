"""Clamp a numeric value into the closed interval [lo, hi]."""


def clamp(v, lo, hi):
    """Return v clamped to [lo, hi]: lo when v < lo, hi when v > hi, else v."""
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v
