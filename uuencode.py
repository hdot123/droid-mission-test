"""uuencode: 经典 uuencode 编解码组件（第五十八轮 D 单）。

正文格式（带行长前缀的分行格式，与 ascii85／base45 等连续流编码族结构全异）：

- 数据按 45 字节分行，每行行首一个长度字符 = 本行字节数 + 32
  （45 字节整行时长度字符为 "M"）；
- 行内每 3 字节转 4 字符：四个 6 位组各 + 32，零值写反引号而不是空格；
- 全部行后以单反引号行收尾；行间以 "\\n" 连接、无尾随换行；
  不带 begin/end 头尾行；空输入返回单个反引号字符。

解码侧宽容：容忍空格作零值；格式不合（空文本、缺收尾行、正文长度与长度
字符不合、收尾行不在末行、含空行）抛 ValueError。
"""

_LINE_BYTES = 45


def _emit(value: int) -> str:
    """6 位组值 → uuencode 字符：零值写反引号，其余各 +32。"""
    return "`" if value == 0 else chr(value + 32)


def uuencode(data: bytes) -> str:
    """把字节串编码为经典 uuencode 正文（无头尾行、无尾随换行）。

    入参必须是 bytes，否则抛 TypeError。
    """
    if not isinstance(data, bytes):
        raise TypeError("uuencode() expected bytes, got %s" % type(data).__name__)
    lines = []
    for start in range(0, len(data), _LINE_BYTES):
        chunk = data[start:start + _LINE_BYTES]
        chars = [chr(len(chunk) + 32)]
        for i in range(0, len(chunk), 3):
            b0 = chunk[i]
            b1 = chunk[i + 1] if i + 1 < len(chunk) else 0
            b2 = chunk[i + 2] if i + 2 < len(chunk) else 0
            group = (b0 << 16) | (b1 << 8) | b2
            chars.append(_emit((group >> 18) & 0x3F))
            chars.append(_emit((group >> 12) & 0x3F))
            chars.append(_emit((group >> 6) & 0x3F))
            chars.append(_emit(group & 0x3F))
        lines.append("".join(chars))
    lines.append("`")
    return "\n".join(lines)


def uudecode(text: str) -> bytes:
    """把经典 uuencode 正文还原为字节串。

    入参必须是 str，否则抛 TypeError；格式不合抛 ValueError。
    """
    if not isinstance(text, str):
        raise TypeError("uudecode() expected str, got %s" % type(text).__name__)
    if text == "":
        raise ValueError("empty text")
    lines = text.split("\n")
    for line in lines:
        if line == "":
            raise ValueError("empty line in input")
    if lines[-1] != "`":
        raise ValueError("missing terminator line")
    out = bytearray()
    for line in lines[:-1]:
        length = ord(line[0]) - 32
        if length < 0 or length > _LINE_BYTES:
            raise ValueError("bad length character: %r" % line[0])
        payload = line[1:]
        if len(payload) != 4 * ((length + 2) // 3):
            raise ValueError("body length inconsistent with length character")
        raw = bytearray()
        for i in range(0, len(payload), 4):
            value = 0
            for ch in payload[i:i + 4]:
                if ch == "`":  # 零值写反引号
                    v = 0
                else:
                    v = ord(ch) - 32
                    if v < 0 or v > 0x3F:
                        raise ValueError("bad data character: %r" % ch)
                value = (value << 6) | v
            raw += value.to_bytes(3, "big")
        out += raw[:length]
    return bytes(out)
