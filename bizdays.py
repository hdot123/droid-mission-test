"""Business-day counting and stepping (standard library only).

A business day is Monday through Friday and not in the holiday set.

Date anchors used by the spec: 2026-01-01 is a Thursday, 2026-01-05 is a
Monday.
"""

from datetime import date, datetime, timedelta

__all__ = ["is_business_day", "business_days", "add_business_days"]


def _as_date(value, name):
    """Validate that value is a datetime.date; datetime.datetime is rejected."""
    if isinstance(value, datetime) or not isinstance(value, date):
        raise TypeError(
            f"{name} must be a datetime.date instance, got {type(value).__name__}"
        )
    return value


def _as_holidays(holidays):
    """Validate holidays as an iterable of dates and return a frozen set."""
    try:
        items = list(holidays)
    except TypeError:
        raise TypeError(
            "holidays must be an iterable of datetime.date instances"
        ) from None
    return frozenset(_as_date(item, "holiday") for item in items)


def _is_business_day(d, holidays):
    """Internal check against an already-validated holiday set."""
    return d.weekday() < 5 and d not in holidays


def _count_forward(start, end, holidays):
    """Count business days over [start, end); caller guarantees start <= end."""
    total = 0
    cur = start
    while cur < end:
        if _is_business_day(cur, holidays):
            total += 1
        cur += timedelta(days=1)
    return total


def is_business_day(d: date, holidays=frozenset()) -> bool:
    """Return whether d is a business day (Monday-Friday, not a holiday)."""
    d = _as_date(d, "d")
    hol = _as_holidays(holidays)
    return _is_business_day(d, hol)


def business_days(start: date, end: date, holidays=frozenset()) -> int:
    """Number of business days in the half-open interval [start, end).

    When end < start the result is the negation of the count over
    [end, start). An empty interval (start == end) counts 0.
    """
    start = _as_date(start, "start")
    end = _as_date(end, "end")
    hol = _as_holidays(holidays)
    if end < start:
        return -_count_forward(end, start, hol)
    return _count_forward(start, end, hol)


def add_business_days(d: date, n: int, holidays=frozenset()) -> date:
    """Move n business days from d, stepping one calendar day at a time.

    n may be negative; n == 0 returns d unchanged even when d is not a
    business day. The starting day itself is never counted.
    """
    d = _as_date(d, "d")
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    hol = _as_holidays(holidays)
    if n == 0:
        return d
    step = 1 if n > 0 else -1
    remaining = n if n > 0 else -n
    cur = d
    while remaining > 0:
        cur += timedelta(days=step)
        if _is_business_day(cur, hol):
            remaining -= 1
    return cur
