"""IEC 1024 byte-size formatting.

Formats a non-negative integer byte count as a human-readable string using
binary units: B, KiB, MiB, GiB, TiB (each step is 1024x).
"""

_UNITS = ("B", "KiB", "MiB", "GiB", "TiB")


def format_bytes(n: int) -> str:
    """Format a non-negative integer ``n`` as ``"{value} {unit}"``.

    Values below 1024 are rendered as integer bytes (``B``); larger values
    are scaled to the largest unit that keeps them below 1024 and rendered
    with one decimal place. The largest unit is ``TiB``.

    Raises:
        ValueError: if ``n`` is negative.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    index = 0
    while index < len(_UNITS) - 1 and n >= 1024 ** (index + 1):
        index += 1

    if index == 0:
        return f"{n} B"

    value = n / (1024 ** index)
    return f"{value:.1f} {_UNITS[index]}"
