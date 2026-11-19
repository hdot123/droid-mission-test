"""Integer partition count p(n)."""

from __future__ import annotations

__all__ = ["partitions"]


def partitions(n: int) -> int:
    """Return the number of order-independent additive decompositions of n.

    ``partitions(0) == 1`` (the empty partition). ``n`` must be an ``int``
    (``bool`` is rejected); negative ``n`` raises ``ValueError`` and non-int
    input raises ``TypeError``.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if n <= 1:
        return 1

    # Classic DP: p(k) for k = 0..n, counting partitions of k.
    counts = [0] * (n + 1)
    counts[0] = 1
    for part in range(1, n + 1):
        for k in range(part, n + 1):
            counts[k] += counts[k - part]
    return counts[n]
