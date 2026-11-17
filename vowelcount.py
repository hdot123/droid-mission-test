"""Count vowel letters in a string (standard library only)."""

VOWELS = frozenset("aeiou")


def count(s):
    """Return the number of vowel letters (a, e, i, o, u) in s.

    Matching is case-insensitive; all non-vowel characters are ignored.
    """
    return sum(1 for ch in s.lower() if ch in VOWELS)
