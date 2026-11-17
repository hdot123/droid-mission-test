"""Text wrapping (fence) utilities.

Public API:
    wrap(text, width) -> str   greedy word wrap
    unwrap(text) -> str        collapse a wrapped block to a single line
"""


def wrap(text, width):
    """Wrap *text* into lines of at most *width* characters.

    Words are never split; a word longer than *width* goes on its own
    line and is kept in full (that line may exceed *width*).  Input
    whitespace runs are treated as word separators, and output words
    are separated by single spaces.

    Raises:
        TypeError: if *text* or *width* is None.
        ValueError: if *width* is not positive.
    """
    if text is None:
        raise TypeError("wrap() argument 'text' must be str, not None")
    if width is None:
        raise TypeError("wrap() argument 'width' must be int, not None")
    if width <= 0:
        raise ValueError("width must be a positive number")

    lines = []
    current = ""
    for word in text.split():
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current = current + " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return "\n".join(lines)


def unwrap(text):
    """Collapse wrapped *text* back into a single line.

    Lines are joined with single spaces; blank lines and whitespace runs
    become single spaces between words.  A trailing hyphen at a line end
    is preserved as-is: it is never removed, and the following word is
    still joined with a single space.

    Raises:
        TypeError: if *text* is None.
    """
    if text is None:
        raise TypeError("unwrap() argument 'text' must be str, not None")
    return " ".join(text.split())
