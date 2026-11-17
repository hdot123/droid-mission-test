"""Anagram helpers: letter-insensitive anagram detection and grouping."""


def _letters(text):
    """Return only the alphabetic characters of text, lowercased."""
    return [ch.lower() for ch in text if ch.isalpha()]


def are_anagrams(a, b):
    """Return True if a and b are anagrams.

    Only alphabetic characters are considered; case and all non-letter
    characters are ignored.
    """
    return sorted(_letters(a)) == sorted(_letters(b))


def group(words):
    """Group words that are anagrams of each other.

    Within each group words keep their original input order; groups are
    ordered by the position in the input of each group's first word.
    """
    groups = []
    signatures = []
    for word in words:
        sig = tuple(sorted(_letters(word)))
        if sig in signatures:
            idx = signatures.index(sig)
            groups[idx].append(word)
        else:
            signatures.append(sig)
            groups.append([word])
    return groups
