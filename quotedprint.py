"""Quoted-Printable 编解码（简化口径）。

本轮口径明确不含行长处理：encode 不做软换行切分。
"""

_HEX = "0123456789ABCDEF"


def encode(data: bytes) -> str:
    """字节按简化 Quoted-Printable 编码为 str。

    33-60、62-126 范围内的字节（除 ``=`` 外的可打印 ASCII）原样输出；
    其余字节（含 ``=``、空格、制表符、非 ASCII）一律编码为 ``=XX``（大写十六进制）。
    """
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("data must be bytes-like")
    out = []
    for b in data:
        if 33 <= b <= 60 or 62 <= b <= 126:
            out.append(chr(b))
        else:
            out.append("=" + _HEX[b >> 4] + _HEX[b & 0x0F])
    return "".join(out)


def decode(text: str) -> bytes:
    """encode 的逆运算。

    ``=`` 后不是两位十六进制数时抛 ValueError。
    """
    if not isinstance(text, str):
        raise TypeError("text must be str")
    out = bytearray()
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "=":
            if i + 2 >= n:
                raise ValueError("trailing '=' at position %d" % i)
            pair = text[i + 1 : i + 3]
            try:
                out.append(int(pair, 16))
            except ValueError:
                raise ValueError(
                    "invalid escape '=%s' at position %d" % (pair, i)
                ) from None
            i += 3
        else:
            b = ord(ch)
            if b > 127:
                raise ValueError("non-ASCII character %r at position %d" % (ch, i))
            out.append(b)
            i += 1
    return bytes(out)
