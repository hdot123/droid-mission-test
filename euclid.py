"""Euclidean algorithm helpers: gcd, lcm, and extended gcd."""


def gcd(a, b):
    """Return the non-negative greatest common divisor of a and b."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return the non-negative least common multiple of a and b.

    If either input is 0, the result is 0.
    """
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b) * b)


def extended_gcd(a, b):
    """Return (g, x, y) with g == gcd(a, b) and a*x + b*y == g."""
    old_r, r = abs(a), abs(b)
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    if a < 0:
        old_s = -old_s
    if b < 0:
        old_t = -old_t
    return old_r, old_s, old_t
