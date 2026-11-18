"""Proleptic Gregorian weekday computation.

weekday() returns 0 for Monday through 6 for Sunday.
The day of week is derived in this module from a day count anchored on
0001-01-01 being a Monday; no datetime or calendar weekday helpers are used.
"""

__all__ = ["is_leap_year", "weekday"]

_DAYS_BEFORE_MONTH = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)


def is_leap_year(year):
    """Return True if year is a Gregorian leap year, else False."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_in_month(year, month):
    if month == 2:
        return 29 if is_leap_year(year) else 28
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    return 30


def weekday(year, month, day):
    """Return the weekday of (year, month, day) as an int 0-6 (0 = Monday)."""
    if year < 1:
        raise ValueError("year must be >= 1")
    if not 1 <= month <= 12:
        raise ValueError("month must be in 1..12")
    if not 1 <= day <= _days_in_month(year, month):
        raise ValueError("day out of range for given year and month")

    years = year - 1
    # Days elapsed before 0001-01-01 is 0; count full years before `year`.
    total = years * 365 + years // 4 - years // 100 + years // 400
    total += _DAYS_BEFORE_MONTH[month - 1]
    if month > 2 and is_leap_year(year):
        total += 1
    total += day - 1
    # 0001-01-01 is a Monday (weekday 0).
    return total % 7
