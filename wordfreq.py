"""Word frequency utility (standard library only)."""

import re

_WORD_RE = re.compile(r"[A-Za-z0-9]+")


def top_words(text, n):
    """Return the top ``n`` most frequent words in ``text``.

    A word is a maximal run of ASCII letters or digits, lowercased for
    counting. Results are sorted by descending frequency, ties broken by
    word in ascending alphabetical order. ``n <= 0`` returns an empty
    list; ``n`` larger than the number of distinct words returns all
    words.
    """
    if n <= 0:
        return []
    counts = {}
    for match in _WORD_RE.finditer(text):
        word = match.group(0).lower()
        counts[word] = counts.get(word, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]
