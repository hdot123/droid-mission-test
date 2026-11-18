"""Sentence-level statistics for plain text.

This module provides the sentence-statistics capability of the
text-statistics toolkit: how many sentences a text contains and roughly
how long those sentences are.

Sentence boundaries are detected heuristically: a sentence ends at a run
of ``.``, ``!`` or ``?`` (optionally followed by closing quotes or
brackets) that is followed by whitespace or the end of the text.
Standard library only; this module exposes no CLI.
"""

import re
from typing import Dict, List

__all__ = [
    "split_sentences",
    "count_sentences",
    "sentence_lengths",
    "average_sentence_length",
    "sentence_length_summary",
]

_TERMINATOR_RE = re.compile(r'[.!?]+["\')\]]*(?=\s|$)')


def split_sentences(text: str) -> List[str]:
    """Split *text* into individual sentences.

    A sentence boundary is a run of ``.``/``!``/``?`` (plus any adjacent
    closing quotes or brackets) followed by whitespace or the end of the
    text. Each returned sentence is stripped of leading and trailing
    whitespace, and empty pieces are dropped. Words are *not* otherwise
    normalized: the original characters of each sentence are preserved.

    Returns:
        The sentences in order. An empty or whitespace-only input yields
        ``[]``. Text with no terminal punctuation is returned as a single
        sentence (when it is non-empty).

    Raises:
        TypeError: If *text* is not a ``str``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    sentences: List[str] = []
    start = 0
    for match in _TERMINATOR_RE.finditer(text):
        piece = text[start:match.end()].strip()
        if piece:
            sentences.append(piece)
        start = match.end()
    tail = text[start:].strip()
    if tail:
        sentences.append(tail)
    return sentences


def count_sentences(text: str) -> int:
    """Return how many sentences *text* contains.

    Equivalent to ``len(split_sentences(text))``: an empty or
    whitespace-only input yields ``0``, and text without terminal
    punctuation counts as one sentence.
    """
    return len(split_sentences(text))


def sentence_lengths(text: str) -> List[int]:
    """Return the word count of each sentence in *text*.

    Words are whitespace-separated tokens of the sentences produced by
    :func:`split_sentences`, in the same order. The returned list has
    exactly ``count_sentences(text)`` elements; an empty input yields
    ``[]``.
    """
    return [len(sentence.split()) for sentence in split_sentences(text)]


def average_sentence_length(text: str) -> float:
    """Return the average number of words per sentence in *text*.

    Computed as the total number of whitespace-separated words divided
    by ``count_sentences(text)``. Returns ``0.0`` when *text* contains no
    sentences.
    """
    lengths = sentence_lengths(text)
    if not lengths:
        return 0.0
    return sum(lengths) / len(lengths)


def sentence_length_summary(text: str) -> Dict[str, float]:
    """Return summary statistics of the sentence lengths in *text*.

    The returned dict has exactly these keys:

    - ``sentence_count``: number of sentences (``0`` for empty input).
    - ``word_count``: total words across all sentences (``0`` when empty).
    - ``average_sentence_length``: mean words per sentence, ``0.0`` when
      there are no sentences.
    - ``min_sentence_length``: smallest per-sentence word count, ``0``
      when there are no sentences.
    - ``max_sentence_length``: largest per-sentence word count, ``0``
      when there are no sentences.
    """
    lengths = sentence_lengths(text)
    if not lengths:
        return {
            "sentence_count": 0,
            "word_count": 0,
            "average_sentence_length": 0.0,
            "min_sentence_length": 0,
            "max_sentence_length": 0,
        }
    return {
        "sentence_count": len(lengths),
        "word_count": sum(lengths),
        "average_sentence_length": sum(lengths) / len(lengths),
        "min_sentence_length": min(lengths),
        "max_sentence_length": max(lengths),
    }
