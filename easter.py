"""easter: 公历复活节日期计算（Anonymous Gregorian computus）。

实现 Meeus/Jones/Butcher 算法，返回给定年份复活节（周日）的日期。
year 须为 1583–4099 的 int：越界抛 ValueError，非 int（含 bool）抛 TypeError。
"""

import datetime

_MIN_YEAR = 1583
_MAX_YEAR = 4099


def easter_date(year: int) -> datetime.date:
    """返回 year 年复活节（周日）的日期（Anonymous Gregorian computus）。

    year 必须是 1583–4099 之间的 int（bool 拒绝）：越界抛 ValueError，
    非 int 抛 TypeError。
    """
    if isinstance(year, bool) or not isinstance(year, int):
        raise TypeError("year must be an int, got %r" % (type(year).__name__,))
    if year < _MIN_YEAR or year > _MAX_YEAR:
        raise ValueError("year out of range 1583-4099: %d" % year)

    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)
