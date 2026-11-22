"""Clamp a numeric value into the inclusive interval [lo, hi]."""


def clamp(v, lo, hi):
    """Return v clamped to the inclusive range [lo, hi].

    If v < lo return lo; if v > hi return hi; otherwise return v itself.
    """
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v
