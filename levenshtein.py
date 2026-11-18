"""Levenshtein edit distance between two strings."""


def distance(a, b):
    """Return the edit distance between strings a and b.

    Insertions, deletions, and substitutions each cost 1.
    """
    # Distance is symmetric; keep the shorter string as the inner row
    # to minimize memory use.
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, char_a in enumerate(a, 1):
        current = [i]
        for j, char_b in enumerate(b, 1):
            current.append(
                min(
                    current[j - 1] + 1,  # insertion
                    previous[j] + 1,  # deletion
                    previous[j - 1] + (char_a != char_b),  # substitution
                )
            )
        previous = current
    return previous[-1]
