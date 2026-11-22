"""julian: 儒略日换算（格里高利历）。

给定格里高利历日期，返回该日期 12:00 UT 的整数儒略日数，并提供逆运算。
2 月按格里高利闰年规则：能被 4 整除且不能被 100 整除，或能被 400 整除。
仅使用标准库，不依赖仓库内其他模块。
"""

_DAYS_IN_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def _is_gregorian_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_in_month(year: int, month: int) -> int:
    if month == 2 and _is_gregorian_leap(year):
        return 29
    return _DAYS_IN_MONTH[month - 1]


def to_jd(y: int, m: int, d: int) -> int:
    """返回格里高利历日期 (y, m, d) 在 12:00 UT 的儒略日数（整数）。

    年须 >= 1，月须在 1..12，日须为该月合法日期，否则抛 ValueError。
    """
    if y < 1:
        raise ValueError("year must be >= 1: %r" % (y,))
    if not 1 <= m <= 12:
        raise ValueError("month must be in 1..12: %r" % (m,))
    if not 1 <= d <= _days_in_month(y, m):
        raise ValueError("invalid day for %04d-%02d: %r" % (y, m, d))
    # Fliegel–Van Flandern: 格里高利历正午（12:00 UT）的整数儒略日。
    a = (14 - m) // 12
    year_adj = y + 4800 - a
    month_adj = m + 12 * a - 3
    return (
        d
        + (153 * month_adj + 2) // 5
        + 365 * year_adj
        + year_adj // 4
        - year_adj // 100
        + year_adj // 400
        - 32045
    )


def from_jd(jd: int) -> tuple:
    """儒略日（12:00 UT）逆运算，返回 (年, 月, 日)。"""
    a = jd + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + m // 10
    return (year, month, day)
