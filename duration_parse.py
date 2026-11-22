"""Parse and format simple duration strings (d/h/m/s units)."""

import re

_UNITS = {"d": 86400, "h": 3600, "m": 60, "s": 1}

# One or more segments: a non-negative integer immediately followed by a unit
# letter; segments may be separated by spaces.
_FORMAT = re.compile(r"\d+[dhms](?: *\d+[dhms])*")
_SEGMENT = re.compile(r"(\d+)([dhms])")


def parse_duration(s):
    """Parse a duration string into total seconds as an int.

    The string consists of one or more segments, each a non-negative integer
    immediately followed by a unit letter (d, h, m, s). Segments may be
    separated by spaces and leading/trailing spaces are allowed. Each unit may
    appear at most once. Any input not matching this format raises ValueError.
    """
    text = s.strip()
    if not text or not _FORMAT.fullmatch(text):
        raise ValueError("invalid duration string: {!r}".format(s))
    total = 0
    seen = set()
    for number, unit in _SEGMENT.findall(text):
        if unit in seen:
            raise ValueError("unit {!r} appears more than once".format(unit))
        seen.add(unit)
        total += int(number) * _UNITS[unit]
    return total


def format_duration(seconds):
    """Format a non-negative integer number of seconds into minimal form.

    Greedily decomposes by day, hour, minute, second from largest to smallest,
    omits zero-valued units, joins segments without spaces, and renders 0 as
    "0s". A negative input raises ValueError.
    """
    if not isinstance(seconds, int):
        raise TypeError("seconds must be an int")
    if seconds < 0:
        raise ValueError("seconds must be non-negative: {!r}".format(seconds))
    if seconds == 0:
        return "0s"
    parts = []
    remaining = seconds
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60), ("s", 1)):
        value, remaining = divmod(remaining, size)
        if value:
            parts.append("{}{}".format(value, unit))
    return "".join(parts)
