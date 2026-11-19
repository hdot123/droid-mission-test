"""Aliquot sums, perfect/abundant/deficient classification, and aliquot sequences."""


def _check_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 1:
        raise ValueError(f"{name} must be >= 1, got {value}")


def aliquot_sum(n: int) -> int:
    """Return the sum of the proper divisors of n (excludes n itself, includes 1)."""
    _check_int(n, "n")
    if n == 1:
        return 0
    total = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            total += i
            other = n // i
            if other != i:
                total += other
        i += 1
    return total


def classify(n: int) -> str:
    """Classify n as "perfect", "abundant", or "deficient" by its aliquot sum."""
    _check_int(n, "n")
    total = aliquot_sum(n)
    if total == n:
        return "perfect"
    if total > n:
        return "abundant"
    return "deficient"


def aliquot_sequence(n: int, count: int) -> list[int]:
    """Return the aliquot sequence starting at n, up to count terms.

    If a term's aliquot sum is 0 the sequence ends early and 0 is not included.
    """
    _check_int(n, "n")
    _check_int(count, "count")
    sequence = [n]
    current = n
    while len(sequence) < count:
        nxt = aliquot_sum(current)
        if nxt == 0:
            break
        sequence.append(nxt)
        current = nxt
    return sequence
