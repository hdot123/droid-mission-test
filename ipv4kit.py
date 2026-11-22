"""ipv4kit: IPv4 点分十进制与 32 位整数互转（仅标准库）。

- ``parse(text)`` 严格接受点分四段十进制（每段 0-255，禁止前导零，
  禁止空格与非数字字符），返回首段为最高字节的 32 位整数。
- ``format(value)`` 是 ``parse`` 的逆运算，把 0-4294967295 的整数
  还原为点分十进制字符串。

不合规则抛出 ``ValueError``。
"""

__all__ = ["parse", "format"]

_MAX = 4294967295


def _is_digit(char: str) -> bool:
    """只认 ASCII 0-9（避免 isdigit 之类的 Unicode 数字混入）。"""
    return "0" <= char <= "9"


def parse(text: str) -> int:
    """严格解析点分十进制 IPv4 为 32 位整数；不合规抛 ValueError。"""
    if not isinstance(text, str):
        raise ValueError("not a string: %r" % (text,))
    segments = text.split(".")
    if len(segments) != 4:
        raise ValueError("expected 4 segments, got %d: %r" % (len(segments), text))
    value = 0
    for segment in segments:
        if segment == "":
            raise ValueError("empty segment: %r" % (text,))
        if any(not _is_digit(c) for c in segment):
            raise ValueError("non-digit or space in segment: %r" % (text,))
        if len(segment) > 1 and segment[0] == "0":
            raise ValueError("leading zero: %r" % (text,))
        number = int(segment)
        if number > 255:
            raise ValueError("octet out of range: %r" % (text,))
        value = (value << 8) | number
    return value


def format(value: int) -> str:
    """把 0-4294967295 的整数还原为点分十进制字符串；越界抛 ValueError。"""
    if not (0 <= value <= _MAX):
        raise ValueError("value out of range: %r" % (value,))
    return "%d.%d.%d.%d" % (
        (value >> 24) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        value & 0xFF,
    )
