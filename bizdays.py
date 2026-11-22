"""Business-day counting and arithmetic on ``datetime.date`` values.

Business days are Monday through Friday, excluding any date present in the
``holidays`` collection.  Only the standard library is used.
"""

from datetime import date, datetime, timedelta

__all__ = ["is_business_day", "business_days", "add_business_days"]


def _check_date(value, name):
    """Return ``value`` if it is a plain ``datetime.date`` (not ``datetime``)."""
    if not isinstance(value, date) or isinstance(value, datetime):
        raise TypeError(f"{name} must be datetime.date, got {type(value).__name__}")
    return value


def _check_holidays(holidays):
    """Validate the holiday collection and return it as a frozenset."""
    try:
        items = list(holidays)
    except TypeError:
        raise TypeError(
            f"holidays must be an iterable of datetime.date, got "
            f"{type(holidays).__name__}"
        ) from None
    for item in items:
        if not isinstance(item, date) or isinstance(item, datetime):
            raise TypeError(
                f"holidays entries must be datetime.date, got {type(item).__name__}"
            )
    return frozenset(items)


def _check_n(n):
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    return n


def _weekday_count(start, length):
    """Count Monday..Friday dates in the half-open range [start, start+length)."""
    if length <= 0:
        return 0
    weeks, remainder = divmod(length, 7)
    total = weeks * 5
    day = start + timedelta(days=weeks * 7)
    for _ in range(remainder):
        if day.weekday() < 5:
            total += 1
        day += timedelta(days=1)
    return total


def is_business_day(d, holidays=frozenset()):
    """Return whether ``d`` is a business day (Mon-Fri and not a holiday)."""
    _check_date(d, "d")
    holiday_set = _check_holidays(holidays)
    return d.weekday() < 5 and d not in holiday_set


def business_days(start, end, holidays=frozenset()):
    """Return the number of business days in the half-open interval [start, end)."""
    _check_date(start, "start")
    _check_date(end, "end")
    holiday_set = _check_holidays(holidays)
    if end < start:
        return -business_days(end, start, holiday_set)
    if start == end:
        return 0
    length = (end - start).days
    count = _weekday_count(start, length)
    for holiday in holiday_set:
        if start <= holiday < end and holiday.weekday() < 5:
            count -= 1
    return count


def add_business_days(d, n, holidays=frozenset()):
    """Move ``n`` business days forward (n > 0) or backward (n < 0) from ``d``.

    ``n == 0`` returns ``d`` unchanged, even when ``d`` is not a business day.
    """
    _check_date(d, "d")
    _check_n(n)
    holiday_set = _check_holidays(holidays)
    if n == 0:
        return d
    step = 1 if n > 0 else -1
    remaining = abs(n)
    current = d
    while remaining:
        current += timedelta(days=step)
        if current.weekday() < 5 and current not in holiday_set:
            remaining -= 1
    return current
