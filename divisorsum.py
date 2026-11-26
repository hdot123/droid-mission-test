"""Divisor sum (sigma), divisor count (tau) and abundance classification.

Caliber note: ``divisor_sum`` computes sigma(n), the sum of ALL positive
divisors of n INCLUDING n itself (sigma(1) = 1).  This differs from the
aliquot sum (proper divisors, excluding n) -- do not mix the two.
"""

__all__ = ["divisor_sum", "divisor_count", "classify_abundance"]


def _validate(n) -> int:
    """Validate the shared input contract.

    n < 1 raises ValueError; non-int (including bool) raises TypeError.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int, got %r" % (n,))
    if n < 1:
        raise ValueError("n must be >= 1, got %r" % (n,))
    return n


def _divisors(n: int):
    """Yield all positive divisors of n (n >= 1)."""
    i = 1
    while i * i <= n:
        if n % i == 0:
            yield i
            j = n // i
            if j != i:
                yield j
        i += 1


def divisor_sum(n: int) -> int:
    """Return sigma(n): the sum of all positive divisors of n, including n."""
    _validate(n)
    return sum(_divisors(n))


def divisor_count(n) -> int:
    """Return tau(n): the number of positive divisors of n."""
    _validate(n)
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            count += 1
            if n // i != i:
                count += 1
        i += 1
    return count


def classify_abundance(n) -> str:
    """Classify n by comparing sigma(n) with 2n.

    Returns "perfect" (sigma = 2n), "abundant" (sigma > 2n), or
    "deficient" (sigma < 2n).
    """
    sigma = divisor_sum(n)  # performs input validation as well
    double_n = 2 * n
    if sigma == double_n:
        return "perfect"
    if sigma > double_n:
        return "abundant"
    return "deficient"
