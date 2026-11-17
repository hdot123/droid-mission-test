"""Count vowel letters in a string."""

VOWELS = set("aeiou")


def count(s):
    """Return the number of vowel letters (a, e, i, o, u) in s, case-insensitive.

    Non-vowel characters are ignored.
    """
    return sum(1 for ch in s.lower() if ch in VOWELS)
