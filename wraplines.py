"""Greedy word wrapping by width."""


def wrap(text, width):
    """Wrap text into lines of at most `width` characters (greedy, by words).

    Words are split on any whitespace. Each word is appended to the current
    line with a single space between words; if adding a word would make the
    line exceed `width`, a new line is started. A single word longer than
    `width` stands alone on its own line (over-length allowed). Empty or
    whitespace-only text returns an empty list.
    """
    words = text.split()
    if not words:
        return []

    lines = []
    current = words[0]
    for word in words[1:]:
        if len(current) + 1 + len(word) <= width:
            current = current + " " + word
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines
