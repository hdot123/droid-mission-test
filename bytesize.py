"""bytesize: 字节数人类可读格式化与解析（第四十轮 · C 单）。

1024 进制，单位依次为 B、KiB、MiB、GiB、TiB。
format 为正向格式化，parse 为其逆运算；非法输入一律抛 ValueError。
"""

import re

_UNITS = ("B", "KiB", "MiB", "GiB", "TiB")
_BASE = 1024
_MAX_INDEX = 4  # TiB，格式化时的单位上限
_VALUE_RE = re.compile(r"^(\d+)(?:\.(\d))?$")


def format(n: int) -> str:
    """把字节数格式化为人类可读文本；n 为负数抛 ValueError。"""
    if n < 0:
        raise ValueError("negative byte count: %r" % (n,))
    if n < _BASE:
        return "%d B" % n
    index = _MAX_INDEX
    while index > 1 and n < _BASE ** index:
        index -= 1
    return "%.1f %s" % (n / _BASE ** index, _UNITS[index])


def parse(text: str) -> int:
    """把 \"<数值> <单位>\" 形态的文本解析为整数字节数；形态不合规抛 ValueError。"""
    if not isinstance(text, str):
        raise ValueError("invalid byte size: %r" % (text,))
    parts = text.split(" ")
    if len(parts) != 2:
        raise ValueError("invalid byte size: %r" % (text,))
    number, unit = parts
    if unit not in _UNITS:
        raise ValueError("invalid unit: %r" % (unit,))
    match = _VALUE_RE.match(number)
    if match is None:
        raise ValueError("invalid number: %r" % (number,))
    whole = int(match.group(1))
    frac = int(match.group(2)) if match.group(2) else 0
    multiplier = _BASE ** _UNITS.index(unit)
    total = (whole * 10 + frac) * multiplier
    if total % 10 != 0:
        raise ValueError("not a whole number of bytes: %r" % (text,))
    return total // 10
