"""isbn13: ISBN-13 校验位计算与校验。

提供两个函数：

- ``check_digit(first12)``：给定恰 12 位纯数字前缀，按 ISBN-13 规则
  （自左第一位权重 1、其后 1/3 交替）计算校验位（0–9）；
  长度不对或含非数字字符时抛 ``ValueError``。
- ``is_valid(isbn)``：恰 13 位纯数字且校验位吻合时返回 ``True``，
  其余情况（含连字符形式、非字符串输入等）一律返回 ``False``，不抛异常。

只依赖标准库。
"""

_ASCII_DIGITS = "0123456789"


def _is_ascii_digits(text) -> bool:
    """text 为非空字符串且每个字符都是 ASCII 数字时返回 True。"""
    return isinstance(text, str) and bool(text) and all(ch in _ASCII_DIGITS for ch in text)


def check_digit(first12: str) -> int:
    """返回使 ISBN-13 通过校验的校验位（0–9）。

    入参必须是恰 12 位纯数字字符串；长度不对或含非数字字符抛 ValueError。
    """
    if not isinstance(first12, str) or len(first12) != 12 or not _is_ascii_digits(first12):
        raise ValueError("first12 must be exactly 12 pure digits: %r" % (first12,))
    total = 0
    for index, ch in enumerate(first12):
        weight = 1 if index % 2 == 0 else 3
        total += (ord(ch) - 48) * weight
    return (10 - total % 10) % 10


def is_valid(isbn: str) -> bool:
    """恰 13 位纯数字且校验位吻合返回 True，其余（含连字符形式）返回 False。"""
    if not isinstance(isbn, str) or len(isbn) != 13 or not _is_ascii_digits(isbn):
        return False
    return check_digit(isbn[:12]) == ord(isbn[12]) - 48
