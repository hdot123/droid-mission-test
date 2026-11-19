"""Primorial: product of the first n primes (p_n#)."""


def primorial(n: int) -> int:
    """Return the product of the first n primes; primorial(0) == 1."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be >= 0")

    product = 1
    count = 0
    candidate = 2
    while count < n:
        if all(candidate % p != 0 for p in range(2, int(candidate ** 0.5) + 1)):
            product *= candidate
            count += 1
        candidate += 1
    return product
