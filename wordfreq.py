"""Word frequency counting utilities (standard library only)."""

_PUNCT = ".,;:!?\"'()"


def count_words(text):
    """Return a dict mapping lower-cased words to their counts.

    Text is split on whitespace; each token is lower-cased and stripped
    of leading/trailing punctuation in ``.,;:!?"'()``; empty tokens are
    discarded.
    """
    counts = {}
    for token in text.split():
        word = token.lower().strip(_PUNCT)
        if not word:
            continue
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(text, n):
    """Return the top ``n`` ``(word, count)`` pairs.

    Sorted by count descending, ties broken by word ascending
    (alphabetical). Returns an empty list when ``n`` < 1.
    """
    if n < 1:
        return []
    counts = count_words(text)
    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return items[:n]
