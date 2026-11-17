"""Collatz (3n+1) sequence utilities."""


def sequence(n):
    """Return the full Collatz sequence starting from positive integer n.

    The sequence includes n itself and ends at 1. Even numbers are divided
    by 2; odd numbers become 3n + 1.

    Raises ValueError if n is not a positive integer.
    """
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer, got {!r}".format(n))
    result = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        result.append(n)
    return result


def steps(n):
    """Return the number of steps to reach 1, i.e. len(sequence(n)) - 1."""
    return len(sequence(n)) - 1


def peak(n):
    """Return the maximum value in the Collatz sequence for n."""
    return max(sequence(n))
