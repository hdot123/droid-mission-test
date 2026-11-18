"""Hex color string parsing and formatting for "#RGB" / "#RRGGBB" notations.

Standard library only; this module does not import any sibling modules.
"""

_HEX_DIGITS = frozenset("0123456789abcdefABCDEF")


def parse(color):
    """Parse a "#RGB" or "#RRGGBB" color string into an (r, g, b) int tuple.

    Hex letters are case-insensitive.  The three-digit form repeats each
    digit once (e.g. "#f80" -> "#ff8000").

    Raises ValueError for anything else: a missing leading "#", a length
    other than 3 or 6 hex digits, or non-hexadecimal characters.
    """
    if not isinstance(color, str):
        raise ValueError("color must be a string, got %r" % (color,))
    if not color.startswith("#"):
        raise ValueError("color must start with '#': %r" % (color,))
    digits = color[1:]
    if len(digits) == 3:
        digits = "".join(ch * 2 for ch in digits)
    elif len(digits) != 6:
        raise ValueError(
            "color must have 3 or 6 hex digits after '#': %r" % (color,)
        )
    if not all(ch in _HEX_DIGITS for ch in digits):
        raise ValueError("color contains non-hex characters: %r" % (color,))
    return (int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16))


def to_hex(r, g, b):
    """Format an (r, g, b) triple as a lowercase "#rrggbb" string.

    Raises ValueError if any component is not an int in 0..255.
    """
    for name, value in (("r", r), ("g", g), ("b", b)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("%s must be an int, got %r" % (name, value))
        if not 0 <= value <= 255:
            raise ValueError("%s must be in 0..255, got %r" % (name, value))
    return "#%02x%02x%02x" % (r, g, b)
