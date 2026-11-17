"""Levenshtein edit distance utilities (standard library only)."""


def distance(a, b):
    """Return the edit distance between strings ``a`` and ``b``.

    Insertions, deletions and substitutions each cost 1.
    """
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("distance() arguments must be strings")

    # Ensure b is the shorter string so the row stays small.
    if len(a) < len(b):
        a, b = b, a

    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1
            substitution = previous[j - 1] + (ca != cb)
            current.append(min(insertion, deletion, substitution))
        previous = current
    return previous[-1]


def is_within(a, b, k):
    """Return whether ``distance(a, b) <= k``.

    Raises ValueError when ``k`` is negative.
    """
    if k < 0:
        raise ValueError("k must be non-negative, got {!r}".format(k))
    return distance(a, b) <= k
