"""Classic Levenshtein edit distance over Unicode code points."""

__all__ = ["distance"]


def distance(a: str, b: str) -> int:
    """Return the Levenshtein distance between strings ``a`` and ``b``.

    Insertions, deletions, and substitutions each cost 1. Characters are
    compared as Unicode code points. Two empty strings have distance 0.
    """
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    # Keep the shorter string on the inner axis for a smaller row.
    if len(a) > len(b):
        a, b = b, a

    previous = list(range(len(a) + 1))
    for j, b_char in enumerate(b, start=1):
        current = [j]
        for i, a_char in enumerate(a, start=1):
            insertion = current[i - 1] + 1
            deletion = previous[i] + 1
            substitution = previous[i - 1] + (a_char != b_char)
            current.append(min(insertion, deletion, substitution))
        previous = current
    return previous[-1]
