"""Sentence statistics: sentence counts and average sentence length."""

import re

SENTENCE_END = re.compile(r"[.!?]+")


def count_sentences(text):
    """Return the number of sentences in text.

    Sentences are delimited by runs of terminal punctuation (., !, ?);
    consecutive terminal punctuation counts as a single separator, and
    empty fragments are not counted.
    """
    return len([part for part in SENTENCE_END.split(text) if part.strip()])


def average_sentence_length(text):
    """Return the average number of words per sentence (a float).

    Words are whitespace-delimited. Returns 0.0 when there are no
    sentences.
    """
    parts = [part for part in SENTENCE_END.split(text) if part.strip()]
    if not parts:
        return 0.0
    total_words = sum(len(part.split()) for part in parts)
    return total_words / len(parts)
