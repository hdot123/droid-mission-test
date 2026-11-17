"""Hexadecimal color parsing and formatting helpers."""


def parse(s):
    """Parse "#RGB" or "#RRGGBB" (case-insensitive) into an (r, g, b) tuple.

    The short form expands each digit by doubling it. Raises ValueError on
    missing '#', wrong length, or non-hexadecimal characters.
    """
    if not isinstance(s, str):
        raise ValueError("color must be a string")
    if not s.startswith("#"):
        raise ValueError("color must start with '#'")
    body = s[1:]
    if len(body) == 3:
        if not all(c in "0123456789abcdefABCDEF" for c in body):
            raise ValueError("color contains non-hex characters")
        body = "".join(c * 2 for c in body)
    elif len(body) != 6:
        raise ValueError("color must be #RGB or #RRGGBB")
    elif not all(c in "0123456789abcdefABCDEF" for c in body):
        raise ValueError("color contains non-hex characters")
    r = int(body[0:2], 16)
    g = int(body[2:4], 16)
    b = int(body[4:6], 16)
    return (r, g, b)


def to_hex(r, g, b):
    """Return the uppercase "#RRGGBB" form for components in 0-255.

    Each component must be an int in 0-255, otherwise ValueError.
    """
    for name, value in (("r", r), ("g", g), ("b", b)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("%s must be an int" % name)
        if not 0 <= value <= 255:
            raise ValueError("%s must be in 0-255" % name)
    return "#%02X%02X%02X" % (r, g, b)


def is_valid(s):
    """Boolean version of parse: True if s is a valid color, else False."""
    try:
        parse(s)
    except ValueError:
        return False
    return True
