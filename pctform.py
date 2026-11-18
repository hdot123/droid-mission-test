"""pctform: application/x-www-form-urlencoded 表单值编码（第三十八轮新增组件）。

只依赖标准库。encode 先把文本按 UTF-8 编码成字节，再逐字节处理：
未保留字符 A-Z a-z 0-9 与 `-` `.` `_` `~` 原样通过，空格编码为 `+`，
其余字节编码为 `%XX`（大写十六进制）。decode 是逆运算，
`+` 还原为空格、`%XX` 还原字节后再按 UTF-8 解码成文本。
"""

_UNRESERVED = frozenset(
    b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)
_HEX_DIGITS = frozenset(b"0123456789abcdefABCDEF")


def encode(text: str) -> str:
    """把文本编码为 application/x-www-form-urlencoded 值。"""
    out = []
    for byte in text.encode("utf-8"):
        if byte in _UNRESERVED:
            out.append(chr(byte))
        elif byte == 0x20:
            out.append("+")
        else:
            out.append("%%%02X" % byte)
    return "".join(out)


def decode(text: str) -> str:
    """解码 application/x-www-form-urlencoded 值；非法转义或非法 UTF-8 抛 ValueError。"""
    data = bytearray()
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "+":
            data.append(0x20)
            i += 1
        elif ch == "%":
            if i + 2 >= n:
                raise ValueError("incomplete %% escape at position %d" % i)
            pair = text[i + 1 : i + 3]
            if len(pair) != 2 or any(c not in "0123456789abcdefABCDEF" for c in pair):
                raise ValueError("invalid %% escape at position %d: %r" % (i, pair))
            data.append(int(pair, 16))
            i += 3
        else:
            data.extend(ch.encode("utf-8"))
            i += 1
    try:
        return bytes(data).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("decoded bytes are not valid UTF-8") from exc
