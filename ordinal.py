"""Ordinal suffix formatting (standard library only)."""


def ordinal_suffix(n: int) -> str:
    """Return the English ordinal suffix ("st"/"nd"/"rd"/"th") for n.

    Rules: last two digits 11-13 always give "th"; otherwise last digit
    1 -> "st", 2 -> "nd", 3 -> "rd", everything else -> "th".
    n must be a non-negative int: negative raises ValueError,
    non-int raises TypeError.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    last_two = n % 100
    if 11 <= last_two <= 13:
        return "th"
    last = n % 10
    if last == 1:
        return "st"
    if last == 2:
        return "nd"
    if last == 3:
        return "rd"
    return "th"


def ordinal(n: int) -> str:
    """Return the number with its ordinal suffix, e.g. "1st", "11th"."""
    return f"{n}{ordinal_suffix(n)}"
