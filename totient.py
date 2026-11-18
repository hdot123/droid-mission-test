"""Euler's totient function phi(n)."""

from math import isqrt


def totient(n: int) -> int:
    """Return Euler's totient phi(n), the count of integers in [1, n]
    that are coprime to n.

    Raises ValueError for n < 1.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    result = n
    remaining = n
    # Trial-divide out factors 2 and then odd candidates up to sqrt.
    for p in [2] + list(range(3, isqrt(remaining) + 1, 2)):
        if p * p > remaining:
            break
        if remaining % p == 0:
            while remaining % p == 0:
                remaining //= p
            result -= result // p
        if remaining == 1:
            break
    if remaining > 1:
        result -= result // remaining
    return result
