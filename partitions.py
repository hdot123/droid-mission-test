"""Integer partition counts p(n) (order-independent sum decompositions)."""


def partitions(n: int) -> int:
    """Return the number of partitions of a positive integer n.

    ``partitions(0) == 1`` by convention (the empty partition).

    Args:
        n: A non-negative integer.

    Returns:
        The exact partition count p(n).

    Raises:
        TypeError: If n is not an int (bools are rejected).
        ValueError: If n is negative.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    # Pentagonal number theorem recurrence:
    # p(n) = sum_{k != 0} (-1)^{k-1} p(n - g_k), g_k = k(3k-1)/2
    p = [0] * (n + 1)
    p[0] = 1
    for i in range(1, n + 1):
        total = 0
        k = 1
        while True:
            g1 = k * (3 * k - 1) // 2
            if g1 > i:
                break
            sign = 1 if k % 2 == 1 else -1
            total += sign * p[i - g1]
            g2 = k * (3 * k + 1) // 2
            if g2 <= i:
                total += sign * p[i - g2]
            k += 1
        p[i] = total
    return p[n]
