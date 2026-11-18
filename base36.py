"""base36: 非负整数与 Base36 字符串互转。

Base36 字符表为数字 0-9 与小写字母 a-z。编码结果不含前导零，
零本身编码为 "0"。解码时字母大小写不敏感。
"""

_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"

_DECODE_MAP = {ch: i for i, ch in enumerate(_ALPHABET)}


def encode(n: int) -> str:
    """把非负整数 n 转成 base36 字符串；n 为负数抛 ValueError。"""
    if not isinstance(n, int):
        raise TypeError("expected int, got %s" % type(n).__name__)
    if n < 0:
        raise ValueError("negative number: %r" % (n,))
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        n, rem = divmod(n, 36)
        digits.append(_ALPHABET[rem])
    return "".join(reversed(digits))


def decode(text: str) -> int:
    """把 base36 字符串转回整数；空串或字母表外字符抛 ValueError。"""
    if not isinstance(text, str):
        raise TypeError("expected str, got %s" % type(text).__name__)
    if not text:
        raise ValueError("empty base36 string")
    total = 0
    for ch in text:
        value = _DECODE_MAP.get(ch.lower())
        if value is None:
            raise ValueError("invalid base36 character: %r" % (ch,))
        total = total * 36 + value
    return total
