"""Business-day counting and arithmetic (Mon-Fri, excluding holidays).

Standard library only.  Dates must be ``datetime.date`` instances;
``datetime.datetime`` is rejected because it is also a ``date`` subclass.
"""

from datetime import date, datetime, timedelta

__all__ = ["is_business_day", "business_days", "add_business_days"]

_EMPTY_HOLIDAYS = frozenset()


def _check_date(value, name="date"):
    """Validate that *value* is a ``datetime.date`` but not a ``datetime``."""
    if not isinstance(value, date) or isinstance(value, datetime):
        raise TypeError(
            f"{name} must be datetime.date, got {type(value).__name__}"
        )
    return value


def _check_holidays(holidays):
    """Validate the holidays collection and return it as a frozenset."""
    if isinstance(holidays, (str, bytes)):
        raise TypeError(
            "holidays must be an iterable of datetime.date, "
            f"got {type(holidays).__name__}"
        )
    try:
        elements = list(holidays)
    except TypeError as exc:
        raise TypeError(
            "holidays must be an iterable of datetime.date, "
            f"got {type(holidays).__name__}"
        ) from exc
    for element in elements:
        _check_date(element, "holiday")
    return frozenset(elements)


def _check_n(n):
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    return n


def is_business_day(d, holidays=_EMPTY_HOLIDAYS) -> bool:
    """Return True if *d* is Monday-Friday and not in *holidays*."""
    _check_date(d, "d")
    holiday_set = _check_holidays(holidays)
    return d.weekday() < 5 and d not in holiday_set


def business_days(start, end, holidays=_EMPTY_HOLIDAYS) -> int:
    """Count business days in the half-open interval ``[start, end)``.

    When ``end < start`` the result is the negation of the reversed count;
    ``start == end`` returns 0.
    """
    _check_date(start, "start")
    _check_date(end, "end")
    holiday_set = _check_holidays(holidays)

    if end < start:
        return -business_days(end, start, holiday_set)
    if start == end:
        return 0

    count = 0
    current = start
    while current < end:
        if current.weekday() < 5 and current not in holiday_set:
            count += 1
        current = _next_day(current)
    return count


def _next_day(d):
    return d + timedelta(days=1)


def add_business_days(d, n, holidays=_EMPTY_HOLIDAYS) -> date:
    """Move *n* business days from *d* (negative *n* moves backwards).

    ``n == 0`` returns *d* unchanged, even when *d* is not a business day.
    The starting day *d* itself is never counted; stepping begins immediately.
    """
    _check_date(d, "d")
    _check_n(n)
    holiday_set = _check_holidays(holidays)

    if n == 0:
        return d

    step = 1 if n > 0 else -1
    remaining = abs(n)
    current = d
    while remaining > 0:
        current = current + timedelta(days=step)
        if current.weekday() < 5 and current not in holiday_set:
            remaining -= 1
    return current
