"""Fibonacci sequence helpers (round 42)."""


def fib(n: int) -> int:
    """Return the n-th Fibonacci number (fib(0) == 0, fib(1) == 1).

    Raises ValueError for negative n.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib_list(n: int) -> list[int]:
    """Return the list of the first n Fibonacci numbers (fib_list(0) == []).

    Raises ValueError for negative n.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    out: list[int] = []
    a, b = 0, 1
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out
