"""roman: 罗马数字与整数互转工具（存量代码）。

本模块是仓库里已有的存量代码，点火前随其测试一并推上 main 作为基线，
基线中附带的测试全部通过。各函数的行为以其文档字符串为准。
"""

_VALUES = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]

_SYMBOL_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def to_roman(n):
    """把 1..3999 的整数转成罗马数字（标准减法记法）；越界抛 ValueError。"""
    if n < 1 or n > 3999:
        raise ValueError(f"out of range: {n!r}")
    parts = []
    rest = n
    for value, symbol in _VALUES:
        while rest >= value:
            parts.append(symbol)
            rest -= value
    return "".join(parts)


def from_roman(s):
    """把合法罗马数字字符串（大写、标准记法）转成整数；非法抛 ValueError。"""
    if not isinstance(s, str) or not s:
        raise ValueError(f"invalid roman numeral: {s!r}")
    total = 0
    prev = 0
    for ch in reversed(s):
        if ch not in _SYMBOL_VALUES:
            raise ValueError(f"invalid roman numeral: {s!r}")
        value = _SYMBOL_VALUES[ch]
        if value < prev:
            total -= value
        else:
            total += value
            prev = value
    if total < 1 or total > 3999 or to_roman(total) != s:
        raise ValueError(f"invalid roman numeral: {s!r}")
    return total
