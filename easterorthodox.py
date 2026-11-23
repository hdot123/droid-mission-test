"""Orthodox (Julian computus) Easter date, expressed in the Gregorian calendar."""

from __future__ import annotations

__all__ = ["orthodox_easter"]

_MIN_YEAR = 1583
_MAX_YEAR = 9999

# Month lengths used to convert a day-of-year (counted from March 1) back
# into (month, day). Orthodox Easter falls in March..May on the Gregorian
# calendar, so three months suffice.
_MONTH_LENGTHS = (31, 30, 31)  # March, April, May


def _is_int_like(year: object) -> bool:
    """True for real ints, False for bool (bool is a subclass of int)."""
    return isinstance(year, int) and not isinstance(year, bool)


def _day_of_year_to_date(ordinal: int) -> tuple[int, int]:
    """Convert a day-of-year counted from March 1 to (month, day)."""
    remaining = ordinal
    for length, month in zip(_MONTH_LENGTHS, (3, 4, 5)):
        if remaining <= length:
            return (month, remaining)
        remaining -= length
    raise AssertionError(f"ordinal {ordinal} out of range")  # pragma: no cover


def orthodox_easter(year: int) -> tuple[int, int]:
    """Return the Orthodox Easter date for ``year`` in the Gregorian calendar.

    Two pinned steps:

    1. Julian computus::

        a = year % 4, b = year % 7, c = year % 19
        d = (19c + 15) % 30
        e = (2a + 4b - d + 34) % 7
        julian_month = (d + e + 114) // 31
        julian_day   = ((d + e + 114) % 31) + 1

    2. Convert Julian to Gregorian by adding the offset
       ``(year // 100 - year // 400 - 2)`` days.

    Raises TypeError for non-int (bool rejected) and ValueError outside
    ``1583 <= year <= 9999``.
    """
    if not _is_int_like(year):
        raise TypeError(f"year must be int, not {type(year).__name__}")
    if not (_MIN_YEAR <= year <= _MAX_YEAR):
        raise ValueError(
            f"year must satisfy {_MIN_YEAR} <= year <= {_MAX_YEAR}, got {year}"
        )

    # Step 1: Julian computus.
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    julian_month = (d + e + 114) // 31
    julian_day = ((d + e + 114) % 31) + 1

    # Day-of-year for the Julian date (months before March are irrelevant).
    julian_ordinal = julian_day
    for month in range(3, julian_month):
        julian_ordinal += 31 if month in (3, 5) else 30

    # Step 2: Julian -> Gregorian offset.
    offset = (year // 100) - (year // 400) - 2
    gregorian_ordinal = julian_ordinal + offset

    return _day_of_year_to_date(gregorian_ordinal)
