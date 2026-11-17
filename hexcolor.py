"""Hexadecimal color parsing and formatting helpers."""


def parse(s):
    """Parse "#RGB" or "#RRGGBB" (case-insensitive) into an (r, g, b) tuple.

    Short form digits are expanded by doubling each digit.
    Raises ValueError for invalid format.
    """
    if not isinstance(s, str):
        raise ValueError("expected a string")
    if not s.startswith("#"):
        raise ValueError("missing leading '#'")
    body = s[1:]
    if len(body) == 3:
        if any(c not in "0123456789abcdefABCDEF" for c in body):
            raise ValueError("non-hex characters")
        r = int(body[0] * 2, 16)
        g = int(body[1] * 2, 16)
        b = int(body[2] * 2, 16)
        return (r, g, b)
    if len(body) == 6:
        if any(c not in "0123456789abcdefABCDEF" for c in body):
            raise ValueError("non-hex characters")
        r = int(body[0:2], 16)
        g = int(body[2:4], 16)
        b = int(body[4:6], 16)
        return (r, g, b)
    raise ValueError("length must be 3 or 6 hex digits")


def to_hex(r, g, b):
    """Return the uppercase "#RRGGBB" form of (r, g, b).

    Each component must be an int in 0-255, else ValueError is raised.
    """
    for value in (r, g, b):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("components must be int")
        if not 0 <= value <= 255:
            raise ValueError("components must be in 0-255")
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def is_valid(s):
    """Boolean version of parse: True if s is valid, False otherwise."""
    try:
        parse(s)
    except Exception:
        return False
    return True
