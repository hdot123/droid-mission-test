"""century: 年份 → 世纪与千年纪换算工具。

三件函数共用同一套校验规则：
- year 必须是 int（bool 一律拒绝，抛 TypeError）；
- year < 1 抛 ValueError。
"""


def _validate_year(year):
    """校验年份：非 int（含 bool）抛 TypeError，year < 1 抛 ValueError。"""
    if isinstance(year, bool) or not isinstance(year, int):
        raise TypeError("year must be an int, got %r" % (year,))
    if year < 1:
        raise ValueError("year must be >= 1, got %r" % (year,))
    return year


def century(year: int) -> int:
    """返回年份所属世纪（1–100 年为第 1 世纪，101–200 为第 2 世纪，以此类推）。"""
    _validate_year(year)
    return (year - 1) // 100 + 1


def century_range(year: int) -> tuple[int, int]:
    """返回该世纪的起止年份（含两端），如 21 世纪为 (2001, 2100)。"""
    c = century(year)
    return (c - 1) * 100 + 1, c * 100


def millennium(year: int) -> int:
    """返回年份所属千年纪（1–1000 年为第 1 千年纪，以此类推）。"""
    _validate_year(year)
    return (year - 1) // 1000 + 1
