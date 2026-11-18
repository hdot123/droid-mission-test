"""Prime sieve utilities (standard library only)."""


def primes_up_to(n: int) -> list[int]:
    """Return the ascending list of all primes <= n.

    Raises ValueError for negative n; returns [] for n < 2.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = bytearray(len(sieve[p * p :: p]))
    return [i for i in range(n + 1) if sieve[i]]


def is_prime(n: int) -> bool:
    """Return True iff n is prime (n < 2 is not prime)."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True
