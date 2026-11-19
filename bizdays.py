"""工作日计数与推算（标准库实现）。

工作日 = 周一至周五且不在 holidays 内。
锚点：2026-01-01 为周四、2026-01-05 为周一。
"""

from datetime import date, datetime, timedelta

__all__ = ["is_business_day", "business_days", "add_business_days"]

_EMPTY_HOLIDAYS = frozenset()


def _check_date(value, name):
    """校验入参为 datetime.date 且不为 datetime.datetime，否则抛 TypeError。"""
    if isinstance(value, datetime) or not isinstance(value, date):
        raise TypeError(
            f"{name} must be datetime.date, got {type(value).__name__}"
        )
    return value


def _check_holidays(holidays):
    """校验 holidays 为日期的可迭代集合，返回 frozenset。"""
    if isinstance(holidays, (str, bytes)):
        raise TypeError("holidays must be an iterable of datetime.date")
    try:
        items = list(holidays)
    except TypeError:
        raise TypeError(
            "holidays must be an iterable of datetime.date"
        ) from None
    for item in items:
        _check_date(item, "holiday")
    return frozenset(items)


def is_business_day(d, holidays=frozenset()):
    """d 是否为工作日（周一至周五且不在 holidays 内）。"""
    _check_date(d, "d")
    holiday_set = _check_holidays(holidays)
    return d.weekday() < 5 and d not in holiday_set


def business_days(start, end, holidays=frozenset()):
    """半开区间 [start, end) 内的工作日数；end < start 时取相反数。"""
    _check_date(start, "start")
    _check_date(end, "end")
    holiday_set = _check_holidays(holidays)
    if end < start:
        return -business_days(end, start, holiday_set)
    count = 0
    current = start
    while current < end:
        if current.weekday() < 5 and current not in holiday_set:
            count += 1
        current += timedelta(days=1)
    return count


def add_business_days(d, n, holidays=frozenset()):
    """自 d 起沿 sign(n) 方向逐日步进、只数工作日，移动 n 个工作日。

    n == 0 时原样返回 d（即使 d 非工作日）。
    """
    _check_date(d, "d")
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    holiday_set = _check_holidays(holidays)
    if n == 0:
        return d
    step = timedelta(days=1 if n > 0 else -1)
    remaining = abs(n)
    current = d
    while remaining > 0:
        current += step
        if current.weekday() < 5 and current not in holiday_set:
            remaining -= 1
    return current
