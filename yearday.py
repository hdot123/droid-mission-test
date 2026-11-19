"""yearday: 年内日序号（day-of-year）与 (月, 日) 互转工具。

公历（格里高利历）规则：年份能被 4 整除为闰年，但能被 100 整除的不是
闰年，除非同时能被 400 整除。仅用标准库，不依赖其他模块。
"""

_MONTH_LENGTHS_COMMON = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
_MONTH_LENGTHS_LEAP = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def _is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _check_year(year) -> int:
    if isinstance(year, bool) or not isinstance(year, int):
        raise TypeError("year must be int, got %r" % (type(year).__name__,))
    if year < 1:
        raise ValueError("year must be >= 1, got %d" % year)
    return year


def _month_lengths(year: int) -> tuple:
    return _MONTH_LENGTHS_LEAP if _is_leap(year) else _MONTH_LENGTHS_COMMON


def to_yearday(year: int, month: int, day: int) -> int:
    """返回 1 起数的年内日序号（1 月 1 日为 1）。

    非法输入：非 int（含 bool）抛 TypeError；year < 1、month 不在 1–12、
    day 不是该月合法日期抛 ValueError。
    """
    year = _check_year(year)
    for value, name in ((month, "month"), (day, "day")):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("%s must be int, got %r" % (name, type(value).__name__))
    if not 1 <= month <= 12:
        raise ValueError("month must be in 1..12, got %d" % month)
    lengths = _month_lengths(year)
    max_day = lengths[month - 1]
    if not 1 <= day <= max_day:
        raise ValueError("day must be in 1..%d for month %d of year %d, got %d"
                         % (max_day, month, year, day))
    return sum(lengths[: month - 1]) + day


def from_yearday(year: int, n: int) -> tuple[int, int]:
    """返回年内日序号 n 对应的 (月, 日)。

    非法输入：非 int（含 bool）抛 TypeError；year < 1 抛 ValueError；
    n 不在 1..365（平年）／1..366（闰年）内抛 ValueError。
    """
    year = _check_year(year)
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int, got %r" % (type(n).__name__,))
    lengths = _month_lengths(year)
    max_n = sum(lengths)
    if not 1 <= n <= max_n:
        raise ValueError("n must be in 1..%d for year %d, got %d" % (max_n, year, n))
    rest = n
    for month, length in enumerate(lengths, start=1):
        if rest <= length:
            return month, rest
        rest -= length
    # Unreachable: bounds check above guarantees a match.
    raise ValueError("n must be in 1..%d for year %d, got %d" % (max_n, year, n))
