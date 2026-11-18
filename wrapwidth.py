"""Word wrapping and justification helpers (standard library only)."""

__all__ = ["wrap", "justify"]


def _check_width(width):
    if isinstance(width, bool) or not isinstance(width, int) or width <= 0:
        raise ValueError("width must be a positive integer")


def wrap(text, width):
    """Wrap `text` by words into lines of at most `width` characters.

    Words are split on any whitespace and rejoined with a single space.
    A single word longer than `width` occupies its own unbroken line.
    Empty or all-whitespace text returns [].
    Raises ValueError if `width` is not a positive integer.
    """
    _check_width(width)
    words = text.split()
    if not words:
        return []
    lines = []
    current = ""
    for word in words:
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current = current + " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def justify(line, width):
    """Justify a single line to `width` characters.

    The input line's words are separated by single spaces.  The number of
    spaces to insert is `width` minus the line's current length, distributed
    evenly across the gaps between words (base share first; the remainder, if
    any, adds one extra space per gap from left to right).  If the line is
    already at least `width` long, or the line has only one word, it is
    returned unchanged.
    Raises ValueError if `width` is not a positive integer.
    """
    _check_width(width)
    words = line.split(" ")
    if len(words) <= 1:
        return line
    current_len = len(line)
    if current_len >= width:
        return line
    gaps = len(words) - 1
    extra = width - current_len
    base, remainder = divmod(extra, gaps)
    parts = []
    for i, word in enumerate(words):
        parts.append(word)
        if i < gaps:
            spaces = 1 + base + (1 if i < remainder else 0)
            parts.append(" " * spaces)
    return "".join(parts)
