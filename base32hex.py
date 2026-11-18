"""base32hex: RFC 4648 Base32hex 编解码（第三十八轮 · 并发 A 单）。

字母表为 0-9 后接 A-V（共 32 个字符），输出带 ``=`` 填充。
仅使用标准库，不依赖仓库内其他模块。
"""

_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUV"

_DECODE = {ch: i for i, ch in enumerate(_ALPHABET)}

_PAD = "="


def encode(data: bytes) -> str:
    """把字节串编码为 RFC 4648 Base32hex 字符串（带 ``=`` 填充）。"""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes-like, got %r" % (type(data).__name__,))

    out = []
    bits = 0      # 当前累积的比特数
    acc = 0       # 当前累积的比特值（高位在前）

    for byte in data:
        acc = (acc << 8) | byte
        bits += 8
        while bits >= 5:
            bits -= 5
            out.append(_ALPHABET[(acc >> bits) & 0x1F])
        acc &= (1 << bits) - 1

    if bits:
        out.append(_ALPHABET[(acc << (5 - bits)) & 0x1F])

    padded = "".join(out)
    remainder = len(padded) % 8
    if remainder:
        padded += _PAD * (8 - remainder)
    return padded


def decode(text: str) -> bytes:
    """解码 RFC 4648 Base32hex 字符串；非法输入抛 ``ValueError``。"""
    if not isinstance(text, str):
        raise ValueError("invalid base32hex input: %r" % (text,))

    if text == "":
        return b""

    if len(text) % 8 != 0:
        raise ValueError("invalid base32hex length: %r" % (text,))

    body = text.rstrip(_PAD)
    if _PAD in body:
        raise ValueError("misplaced padding: %r" % (text,))
    pad_count = len(text) - len(body)
    if pad_count > 6:
        raise ValueError("too much padding: %r" % (text,))
    if pad_count and len(body) % 8 in (1, 3, 6):
        # 数据字符数只能是 0、2、4、5、7（模 8），对应 1..4 字节的余数。
        raise ValueError("non-conforming padding: %r" % (text,))

    bits = 0
    acc = 0
    out = []
    for ch in body:
        try:
            value = _DECODE[ch]
        except KeyError:
            raise ValueError("character out of alphabet: %r" % (ch,)) from None
        acc = (acc << 5) | value
        bits += 5
        if bits >= 8:
            bits -= 8
            out.append((acc >> bits) & 0xFF)
        acc &= (1 << bits) - 1

    # 尾部剩余比特必须为全 0（RFC 4648 要求不可用比特置 0）。
    if acc:
        raise ValueError("non-zero trailing bits: %r" % (text,))

    return bytes(out)
