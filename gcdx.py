"""GCD and LCM utilities for non-negative integers."""


def gcd(a, b):
    """Return the greatest common divisor of two non-negative integers.

    gcd(0, 0) returns 0. Negative arguments raise ValueError.
    """
    if a < 0 or b < 0:
        raise ValueError("gcd requires non-negative arguments")
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return the least common multiple of two non-negative integers.

    Returns 0 if either argument is 0. Negative arguments raise ValueError.
    """
    if a < 0 or b < 0:
        raise ValueError("lcm requires non-negative arguments")
    if a == 0 or b == 0:
        return 0
    return a // gcd(a, b) * b
