"""monthgrid: 月历网格生成（第五十五轮并发 B 单 · 三件独立小部件之一）。

只用标准库；days_in_month 采用格里高利闰年规则，month_grid 产出
周行 × 7 的网格，当月日期填数字、月外位置填 None。
"""

__all__ = ["days_in_month", "month_grid"]

_MONTH_LENGTHS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def _is_leap(year: int) -> bool:
    """格里高利闰年：能被 4 整除且不被 100 整除，或能被 400 整除。"""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_in_month(year: int, month: int) -> int:
    """返回该月天数；month 超出 1..12 抛 ValueError。"""
    if not 1 <= month <= 12:
        raise ValueError("month out of range: %r" % (month,))
    if month == 2 and _is_leap(year):
        return 29
    return _MONTH_LENGTHS[month - 1]


def month_grid(year, month, first_weekday: int = 0) -> list:
    """周行 × 7 的月历网格。

    当月日期填数字、月外位置填 None；first_weekday 指定每周第一列的
    星期（0 = 周一 … 6 = 周日）。month 超出 1..12 或 first_weekday
    超出 0..6 抛 ValueError。
    """
    if not 0 <= first_weekday <= 6:
        raise ValueError("first_weekday out of range: %r" % (first_weekday,))
    ndays = days_in_month(year, month)  # 内部校验 month，越界抛 ValueError

    # 计算当月 1 号是星期几（0 = 周一 … 6 = 周日）。
    # Sakamoto 公式，对格里高利历成立。
    t = (0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4)
    y = year - 1 if month < 3 else year
    weekday_of_first = (y + y // 4 - y // 100 + y // 400 + t[month - 1]) % 7

    offset = (weekday_of_first - first_weekday) % 7
    cells = [None] * offset + list(range(1, ndays + 1))
    while len(cells) % 7:
        cells.append(None)
    return [cells[i:i + 7] for i in range(0, len(cells), 7)]
