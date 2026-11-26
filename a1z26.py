"""a1z26: A1Z26 字母序号编解码（大写 A-Z ↔ 1-26）。

编码约定（encode）：
- 只接受大写 A-Z 与单空格分词的文本；空串原样返回 ""。
- 字母 → 序号（A = 1 … Z = 26）；词内序号以 "-" 连接，词间以单空格分隔。
- 含小写、数字、连续空格或首尾空格时抛 ValueError；非 str 抛 TypeError。

解码约定（decode）：
- encode 的逆变换；序号须为 1–26 且无前导零，分隔形态与 encode 对称。
- 序号越界、前导零、空段（含词内空格导致的空段）时抛 ValueError；非 str 抛 TypeError。
"""

_UPPERCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def a1z26_encode(text: str) -> str:
    """把大写 A-Z 单空格分词的文本编码为 A1Z26 序号串；非法输入抛异常。"""
    if not isinstance(text, str):
        raise TypeError("expected str, got %s" % type(text).__name__)
    if text == "":
        return ""
    if text[0] == " " or text[-1] == " ":
        raise ValueError("leading/trailing space: %r" % (text,))
    if "  " in text:
        raise ValueError("consecutive spaces: %r" % (text,))
    words = []
    for word in text.split(" "):
        indices = []
        for ch in word:
            if ch not in _UPPERCASE_LETTERS:
                raise ValueError("invalid character %r in %r" % (ch, text))
            indices.append(str(_UPPERCASE_LETTERS.index(ch) + 1))
        words.append("-".join(indices))
    return " ".join(words)


def a1z26_decode(code: str) -> str:
    """把 A1Z26 序号串解码为大写 A-Z 文本；非法输入抛 ValueError。"""
    if not isinstance(code, str):
        raise TypeError("expected str, got %s" % type(code).__name__)
    if code == "":
        return ""
    if code[0] == " " or code[-1] == " ":
        raise ValueError("leading/trailing space: %r" % (code,))
    if "  " in code:
        raise ValueError("consecutive spaces: %r" % (code,))
    words = []
    for word in code.split(" "):
        letters = []
        for segment in word.split("-"):
            if segment == "":
                raise ValueError("empty segment: %r" % (code,))
            if not segment.isdigit():
                raise ValueError("non-numeric index %r in %r" % (segment, code))
            if len(segment) > 1 and segment[0] == "0":
                raise ValueError("leading zero in %r" % (segment,))
            value = int(segment)
            if value < 1 or value > 26:
                raise ValueError("index out of range: %r" % (segment,))
            letters.append(_UPPERCASE_LETTERS[value - 1])
        words.append("".join(letters))
    return " ".join(words)
