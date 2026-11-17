"""Clamp a numeric value into the inclusive range [lo, hi]."""


def clamp(v, lo, hi):
    """Return v bounded to the inclusive interval [lo, hi].

    Returns lo when v < lo, hi when v > hi, otherwise v itself.
    """
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v
