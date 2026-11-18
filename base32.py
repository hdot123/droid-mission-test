"""RFC 4648 Base32 编解码（标准字母表 A-Z、2-7，带 '=' 填充）。

只依赖标准库（本模块无任何 import），不 import 仓库内的其它模块。
行为规格：
- encode(data: bytes) -> str：标准 Base32，带 '=' 填充；空输入返回 ""。
- decode(text: str) -> bytes：逆运算；字母表外字符（含小写字母）、
  填充不合规、长度不合规均抛 ValueError。
"""

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
_DECODE_TABLE = {ch: idx for idx, ch in enumerate(_ALPHABET)}

# 一个 8 字符块内合法的尾部 '=' 数量：对应 5/4/3/2/0 个数据字符。
_VALID_PAD_LENGTHS = (0, 1, 3, 4, 6)


def encode(data: bytes) -> str:
    """把字节串编码为带 '=' 填充的标准 Base32 文本。"""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes, got %s" % type(data).__name__)
    out = []
    acc = 0
    bits = 0
    for byte in data:
        acc = (acc << 8) | byte
        bits += 8
        while bits >= 5:
            bits -= 5
            out.append(_ALPHABET[(acc >> bits) & 0x1F])
        acc &= (1 << bits) - 1
    if bits:
        out.append(_ALPHABET[(acc << (5 - bits)) & 0x1F])
    text = "".join(out)
    return text + "=" * (-len(text) % 8)


def decode(text: str) -> bytes:
    """把标准 Base32 文本解码回字节串；非法输入抛 ValueError。"""
    if not isinstance(text, str):
        raise TypeError("text must be str, got %s" % type(text).__name__)
    if len(text) % 8 != 0:
        raise ValueError("invalid Base32 length: %r" % (text,))
    body = text.rstrip("=")
    pad = len(text) - len(body)
    if pad not in _VALID_PAD_LENGTHS:
        raise ValueError("invalid Base32 padding: %r" % (text,))
    acc = 0
    bits = 0
    out = bytearray()
    for ch in body:
        value = _DECODE_TABLE.get(ch)
        if value is None:
            # 覆盖字母表外字符，含小写字母与 '*' 等符号。
            raise ValueError("invalid Base32 character: %r" % (ch,))
        acc = (acc << 5) | value
        bits += 5
        while bits >= 8:
            bits -= 8
            out.append((acc >> bits) & 0xFF)
        acc &= (1 << bits) - 1
    if acc:
        # 末字符剩余的填充位必须为零（非合规填充）。
        raise ValueError("non-zero Base32 padding bits: %r" % (text,))
    return bytes(out)
