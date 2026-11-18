"""Duration string conversion in h/m/s units.

``parse`` converts strings such as ``"1h30m"`` into total seconds, and
``format`` converts seconds back into the canonical string form.  Only the
units ``h``, ``m`` and ``s`` are allowed, each at most once, and they must
appear in ``h`` -> ``m`` -> ``s`` order.
"""

import re

_PATTERN = re.compile(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?")


def parse(text: str) -> int:
    """Convert a duration string like ``"1h30m"`` into total seconds.

    Raises ValueError for empty strings, digits without a unit, unknown
    units, out-of-order units or duplicated units.
    """
    match = _PATTERN.fullmatch(text)
    if match is None:
        raise ValueError(f"invalid duration string: {text!r}")
    hours, minutes, seconds = match.groups()
    if hours is None and minutes is None and seconds is None:
        raise ValueError(f"invalid duration string: {text!r}")
    total = 0
    if hours is not None:
        total += int(hours) * 3600
    if minutes is not None:
        total += int(minutes) * 60
    if seconds is not None:
        total += int(seconds)
    return total


def format(seconds: int) -> str:
    """Convert a non-negative number of seconds into canonical h/m/s form.

    Zero components are omitted; a total of zero seconds formats as
    ``"0s"``.  Negative input raises ValueError.
    """
    if seconds < 0:
        raise ValueError(f"negative duration: {seconds}")
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if secs or not parts:
        parts.append(f"{secs}s")
    return "".join(parts)
