"""Hamming distance utilities."""


def hamming_distance(a, b):
    """Return the number of positions at which two equal-length strings differ.

    Raises ValueError if the strings have different lengths.
    """
    if len(a) != len(b):
        raise ValueError(
            f"strings must be of equal length, got {len(a)} and {len(b)}"
        )
    return sum(1 for x, y in zip(a, b) if x != y)


def is_within(a, b, k):
    """Return True if the Hamming distance between a and b is at most k.

    Raises ValueError if the strings have different lengths.
    """
    return hamming_distance(a, b) <= k
