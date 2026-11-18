"""Collatz (3n+1) sequence utilities."""


def sequence(n):
    """Return the complete Collatz sequence from positive integer n to 1.

    Includes both the first element ``n`` and the final ``1``.

    Raises:
        ValueError: if ``n`` is not a positive integer (not an int, or < 1).
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    seq = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        seq.append(n)
    return seq


def steps(n):
    """Return the number of steps from n to 1 (len(sequence(n)) - 1).

    Raises the same ValueError as :func:`sequence` for non-positive-integer input.
    """
    return len(sequence(n)) - 1
