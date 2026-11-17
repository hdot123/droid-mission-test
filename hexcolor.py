"""Hexadecimal color parsing and formatting helpers (standard library only)."""

_HEX_DIGITS = "0123456789abcdef"


def parse(s):
    """Parse "#RGB" or "#RRGGBB" (case-insensitive) into an (r, g, b) int tuple.

    Raises ValueError for invalid format: missing '#', wrong length, or
    non-hexadecimal characters.
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
    body = body.lower()
    if any(ch not in _HEX_DIGITS for ch in body):
        raise ValueError("color contains non-hexadecimal characters")
    r = int(body[0:2], 16)
    g = int(body[2:4], 16)
    b = int(body[4:6], 16)
    return (r, g, b)


def to_hex(r, g, b):
    """Return the uppercase "#RRGGBB" string for components 0-255.

    Raises ValueError if any component is not an int in 0-255.
    """
    for name, value in (("r", r), ("g", g), ("b", b)):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{name} must be an int in 0-255")
        if not 0 <= value <= 255:
            raise ValueError(f"{name} must be an int in 0-255")
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def is_valid(s):
    """Boolean version of parse: True if s is a valid color, else False."""
    try:
        parse(s)
    except ValueError:
        return False
    return True
