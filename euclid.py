"""Euclidean number-theory helpers: gcd, lcm, and coprimality checks."""


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of ``a`` and ``b``.

    The result is always non-negative; negative inputs are counted by
    absolute value. ``gcd(0, 0)`` is ``0``.
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of ``a`` and ``b``.

    The result is always non-negative. If either input is ``0`` the
    result is ``0``.
    """
    a, b = abs(a), abs(b)
    if a == 0 or b == 0:
        return 0
    return a // gcd(a, b) * b


def is_coprime(a: int, b: int) -> bool:
    """Return ``True`` when ``gcd(a, b) == 1``."""
    return gcd(a, b) == 1
