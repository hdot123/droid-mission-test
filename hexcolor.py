"""Hexadecimal color parsing and formatting helpers (stdlib only)."""


def parse(s):
    """Parse "#RGB" or "#RRGGBB" (case-insensitive) into an (r, g, b) tuple.

    Raises ValueError for missing "#", wrong length, or non-hex characters.
    The short form is expanded by doubling each digit.
    """
    if not isinstance(s, str):
        raise ValueError("color must be a string")
    if not s.startswith("#"):
        raise ValueError("color must start with '#'")
    body = s[1:]
    if len(body) == 3:
        body = "".join(ch * 2 for ch in body)
    elif len(body) != 6:
        raise ValueError("color must be 3 or 6 hex digits after '#'")
    if any(ch not in "0123456789abcdefABCDEF" for ch in body):
        raise ValueError("color contains non-hex characters")
    r = int(body[0:2], 16)
    g = int(body[2:4], 16)
    b = int(body[4:6], 16)
    return (r, g, b)


def to_hex(r, g, b):
    """Return the uppercase "#RRGGBB" form of (r, g, b).

    Each component must be an int in 0-255, else ValueError.
    """
    for value in (r, g, b):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("components must be int")
        if not 0 <= value <= 255:
            raise ValueError("components must be in 0-255")
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def is_valid(s):
    """Boolean version of parse: True when s is a valid color, else False."""
    try:
        parse(s)
    except ValueError:
        return False
    return True
