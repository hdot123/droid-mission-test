"""Word-frequency statistics for plain text.

This module provides small functions for counting how often words occur in
a piece of text: tokenizing text into words, counting every word, ranking the
most frequent words, and reporting a few summary figures.

All functions operate on ``str`` input and return plain Python objects
(``dict``, ``list``, ``int``); only the standard library is used.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable, List, Tuple

__all__ = [
    "tokenize",
    "count_words",
    "top_words",
    "word_count",
    "unique_word_count",
]

# Words are sequences of letters/digits optionally joined by apostrophes or
# hyphens (e.g. "don't", "well-known"). Everything else is a separator.
_WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['\-][A-Za-z0-9]+)*")


def tokenize(text: str) -> List[str]:
    """Split *text* into a list of word tokens in order of appearance.

    Tokens are maximal runs of letters and digits, optionally containing
    internal apostrophes or hyphens ("don't", "state-of-the-art"). Case is
    preserved exactly as it appears in the input; punctuation and whitespace
    act as separators and are dropped.

    >>> tokenize("Hello, hello world!")
    ['Hello', 'hello', 'world']
    """
    if not isinstance(text, str):
        raise TypeError("tokenize() requires a str argument")
    return _WORD_RE.findall(text)


def count_words(text: str) -> dict:
    """Count the occurrences of each word in *text*.

    Counting is case-insensitive: every token is lowercased before it is
    counted, so "The" and "the" contribute to the same key. The returned
    ``dict`` maps each lowercased word to its number of occurrences; keys
    follow first appearance order in the input.

    >>> count_words("A cat, a hat.")
    {'a': 2, 'cat': 1, 'hat': 1}
    """
    counter: Counter = Counter(token.lower() for token in tokenize(text))
    return dict(counter)


def top_words(text: str, n: int = 10) -> List[Tuple[str, int]]:
    """Return the *n* most frequent words in *text* as ``(word, count)`` pairs.

    Words are counted case-insensitively (see :func:`count_words`). Pairs are
    ordered by descending count; ties are broken alphabetically (ascending),
    so the output is deterministic. If *n* is greater than or equal to the
    number of distinct words, all pairs are returned; if *n* is less than or
    equal to 0, an empty list is returned.

    >>> top_words("a b b c c c", 2)
    [('c', 3), ('b', 2)]
    """
    if not isinstance(n, int):
        raise TypeError("top_words() requires an int for n")
    if n <= 0:
        return []
    counts = count_words(text)
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[:n]


def word_count(text: str) -> int:
    """Return the total number of word tokens in *text*.

    Repeated words are counted each time they occur; the count equals the
    length of ``tokenize(text)``.

    >>> word_count("one two two")
    3
    """
    return len(tokenize(text))


def unique_word_count(text: str) -> int:
    """Return the number of distinct words in *text*.

    Distinctness is case-insensitive, matching :func:`count_words`, so the
    result equals the size of ``count_words(text)``.

    >>> unique_word_count("The the THE")
    1
    """
    return len(count_words(text))
