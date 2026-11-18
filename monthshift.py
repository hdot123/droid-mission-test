"""Shift (year, month) pairs and full dates along the month timeline."""


def _month_index(year, month):
    """Convert (year, month) to a 0-based absolute month index."""
    return (year - 1) * 12 + (month - 1)


def _from_month_index(index):
    """Convert a 0-based absolute month index back to (year, month)."""
    year, month_index = divmod(index, 12)
    return year + 1, month_index + 1


def _days_in_month(year, month):
    """Return the number of days in the given month of the proleptic Gregorian year."""
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if month in (4, 6, 9, 11):
        return 30
    if month == 2:
        leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        return 29 if leap else 28
    return 0  # unreachable: month is validated by callers


def _validate_month(year, month):
    if not isinstance(month, int) or isinstance(month, bool) or month < 1 or month > 12:
        raise ValueError("month must be an integer in 1-12, got {!r}".format(month))
    if not isinstance(year, int) or isinstance(year, bool) or year < 1:
        raise ValueError("year must be an integer >= 1, got {!r}".format(year))


def add_months(year, month, delta):
    """Shift (year, month) by delta months; negative delta moves into the past.

    Returns the new (year, month) tuple.  Raises ValueError if month is
    outside 1-12, or if the shifted year is < 1.
    """
    _validate_month(year, month)
    if not isinstance(delta, int) or isinstance(delta, bool):
        raise ValueError("delta must be an integer, got {!r}".format(delta))
    new_year, new_month = _from_month_index(_month_index(year, month) + delta)
    if new_year < 1:
        raise ValueError(
            "shifted year {} is before year 1".format(new_year)
        )
    return new_year, new_month


def _validate_date(year, month, day):
    _validate_month(year, month)
    if not isinstance(day, int) or isinstance(day, bool):
        raise ValueError("day must be an integer, got {!r}".format(day))
    if day < 1 or day > _days_in_month(year, month):
        raise ValueError(
            "day {} is out of range for {:04d}-{:02d}".format(day, year, month)
        )


def add_months_to_date(year, month, day, delta):
    """Shift the full date by delta months, clamping the day to the target month.

    The year/month are shifted via add_months; if the day exceeds the length
    of the target month it is clamped to that month's last day.  Raises
    ValueError if the input date itself is invalid.
    """
    _validate_date(year, month, day)
    if not isinstance(delta, int) or isinstance(delta, bool):
        raise ValueError("delta must be an integer, got {!r}".format(delta))
    new_year, new_month = add_months(year, month, delta)
    new_day = min(day, _days_in_month(new_year, new_month))
    return new_year, new_month, new_day
