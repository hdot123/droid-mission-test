"""Parse and format human-readable duration strings (d/h/m/s units)."""

__all__ = ["parse", "format"]

_UNIT_SECONDS = {
    "d": 86400,
    "h": 3600,
    "m": 60,
    "s": 1,
}


def parse(s):
    """Parse a duration string into total seconds.

    Accepts segments like ``"1h30m"``, ``"45s"``, ``"2d 3h"``. Units are
    d/h/m/s, may appear in any order, and whitespace between segments is
    allowed. A repeated unit raises ValueError; empty or whitespace-only
    input raises ValueError; malformed input (unknown units, missing
    numbers) raises ValueError; None raises TypeError.
    """
    if s is None:
        raise TypeError("parse() argument must be a string, not NoneType")
    if not isinstance(s, str):
        raise TypeError(
            "parse() argument must be a string, not %s" % type(s).__name__
        )

    text = s.strip()
    if not text:
        raise ValueError("empty duration string")

    total = 0
    seen = set()
    number = ""
    index = 0
    length = len(text)

    while index < length:
        char = text[index]
        if char.isdigit():
            number += char
            index += 1
            continue

        if char.isspace():
            index += 1
            continue

        if not number:
            raise ValueError("missing number before unit %r in %r" % (char, s))

        unit = char.lower()
        if unit not in _UNIT_SECONDS:
            raise ValueError("unknown unit %r in %r" % (char, s))
        if unit in seen:
            raise ValueError("duplicate unit %r in %r" % (char, s))

        seen.add(unit)
        total += int(number) * _UNIT_SECONDS[unit]
        number = ""
        index += 1

    if number:
        raise ValueError("missing unit after number in %r" % (s,))

    return total


def format(seconds):
    """Format a non-negative integer number of seconds into simplest form.

    Greedily uses the largest unit that divides the remaining value
    exactly (integral division priority): ``0 -> "0s"``, ``90 ->
    "1m30s"``, ``3600 -> "1h"``, ``86400 -> "1d"``. Negative input
    raises ValueError; None raises TypeError.
    """
    if seconds is None:
        raise TypeError("format() argument must be an int, not NoneType")
    if isinstance(seconds, bool) or not isinstance(seconds, int):
        raise TypeError(
            "format() argument must be an int, not %s" % type(seconds).__name__
        )
    if seconds < 0:
        raise ValueError("negative duration: %d" % (seconds,))

    if seconds == 0:
        return "0s"

    parts = []
    for unit in ("d", "h", "m", "s"):
        unit_seconds = _UNIT_SECONDS[unit]
        if seconds % unit_seconds == 0:
            count = seconds // unit_seconds
            parts.append("%d%s" % (count, unit))
            break
        if seconds >= unit_seconds:
            count = seconds // unit_seconds
            parts.append("%d%s" % (count, unit))
            seconds -= count * unit_seconds

    return "".join(parts)
