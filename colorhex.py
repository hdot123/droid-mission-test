"""Hex color parsing and formatting (standard library only)."""


def parse(text: str) -> tuple[int, int, int]:
    """Parse "#RGB" or "#RRGGBB" (case-insensitive) into an (r, g, b) tuple.

    The short form expands each digit to two digits (e.g. "#f80" -> FF8000).
    Missing '#', bad length, or non-hex characters raise ValueError.
    """
    if not isinstance(text, str) or not text.startswith("#"):
        raise ValueError("color must start with '#'")
    body = text[1:]
    if len(body) == 3:
        body = "".join(ch * 2 for ch in body)
    elif len(body) != 6:
        raise ValueError("color must be #RGB or #RRGGBB")
    try:
        value = int(body, 16)
    except ValueError:
        raise ValueError(f"invalid hex color: {text!r}") from None
    # int(body, 16) accepts whitespace/signs; re-check every character is hex.
    if any(ch not in "0123456789abcdefABCDEF" for ch in body):
        raise ValueError(f"invalid hex color: {text!r}")
    return (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF


def format(r: int, g: int, b: int) -> str:
    """Format channel values (0-255) as an uppercase "#RRGGBB" string."""
    for name, channel in (("r", r), ("g", g), ("b", b)):
        if not isinstance(channel, int) or isinstance(channel, bool) or not 0 <= channel <= 255:
            raise ValueError(f"channel {name} must be an int in 0-255, got {channel!r}")
    return f"#{r:02X}{g:02X}{b:02X}"
