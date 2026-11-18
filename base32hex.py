"""base32hex: RFC 4648 Base32hex 编解码工具。

字母表为 ``0123456789ABCDEFGHIJKLMNOPQRSTUV``，输出用 ``=`` 补齐到 8 的倍数。
``encode`` 输入 ``bytes`` 返回 ``str``；``decode`` 输入 ``str`` 返回 ``bytes``，
只接受字母表内的大写字符与末尾 ``=`` 补齐，其余非法输入抛 ``ValueError``。
"""

_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUV"
_DECODE_TABLE = {ch: i for i, ch in enumerate(_ALPHABET)}
_VALID_PAD_COUNTS = {0, 1, 3, 4, 6}


def encode(data):
    """把 bytes 编码为 RFC 4648 Base32hex 字符串，用 '=' 补齐到 8 的倍数。"""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes, got %r" % (type(data).__name__,))
    out = []
    for start in range(0, len(data), 5):
        chunk = bytes(data[start:start + 5])
        # 左对齐到 40 比特，再按 5 比特一组切分。
        acc = int.from_bytes(chunk, "big") << (40 - 8 * len(chunk))
        for shift in range(35, -1, -5):
            out.append(_ALPHABET[(acc >> shift) & 0x1F])
        # 本块前 keep 个字符为数据，其余替换为 '='（keep = ceil(8n/5)）。
        keep = -(-8 * len(chunk) // 5)
        for i in range(keep, 8):
            out[-8 + i] = "="
    return "".join(out)


def decode(s):
    """把 Base32hex 字符串解码为 bytes；非法输入抛 ValueError。"""
    if not isinstance(s, str):
        raise ValueError("expected str, got %r" % (type(s).__name__,))
    if len(s) % 8 != 0:
        raise ValueError("length must be a multiple of 8: %r" % (s,))
    eq = s.find("=")
    if eq == -1:
        body, pad = s, 0
    else:
        body, tail = s[:eq], s[eq:]
        if any(ch != "=" for ch in tail):
            raise ValueError("'=' must only appear at the end: %r" % (s,))
        pad = len(tail)
        if pad not in _VALID_PAD_COUNTS:
            raise ValueError("invalid padding count %d: %r" % (pad, s))
    values = []
    for ch in body:
        if ch not in _DECODE_TABLE:
            raise ValueError("character outside alphabet: %r" % (ch,))
        values.append(_DECODE_TABLE[ch])
    total_bits = 5 * len(values)
    nbytes, leftover = divmod(total_bits, 8)
    acc = 0
    for value in values:
        acc = (acc << 5) | value
    if leftover:
        acc >>= leftover  # 丢弃末尾的填充比特
    return acc.to_bytes(nbytes, "big")
