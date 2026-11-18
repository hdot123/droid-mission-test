"""Anagram utilities: case-insensitive, punctuation/space-ignoring comparison."""


def _normalize(s):
    """Keep only letters and digits, lowercased."""
    return "".join(ch.lower() for ch in s if ch.isalnum())


def is_anagram(a, b):
    """Return True if a and b are anagrams.

    Comparison is case-insensitive and ignores spaces and punctuation;
    only letters and digits participate, judged by character counts.
    """
    ca = _normalize(a)
    cb = _normalize(b)
    return sorted(ca) == sorted(cb)


def group_anagrams(words):
    """Group words by the anagram relation.

    Groups are ordered by the first appearance position of each group's
    first member in the original list; within a group the original list
    order is preserved.
    """
    groups = []
    keys = []
    for word in words:
        key = tuple(sorted(_normalize(word)))
        if key in keys:
            groups[keys.index(key)].append(word)
        else:
            keys.append(key)
            groups.append([word])
    return groups
