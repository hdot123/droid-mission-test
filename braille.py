"""braille: 一级盲文（Grade 1）字母与盲文字符互转（第 54 轮并发 B 单新增）。

点位编号 1–6，码点 = 0x2800 + Σ 2^(点位 − 1)。
to_braille 仅接受小写 a–z 与空格；from_braille 仅接受表中 26 个盲文字符与
U+2800（空白盲文格）。其他字符抛 ValueError，非 str 抛 TypeError。
"""

_DOTS = {
    "a": (1,),
    "b": (1, 2),
    "c": (1, 4),
    "d": (1, 4, 5),
    "e": (1, 5),
    "f": (1, 2, 4),
    "g": (1, 2, 4, 5),
    "h": (1, 2, 5),
    "i": (2, 4),
    "j": (2, 4, 5),
    "k": (1, 3),
    "l": (1, 2, 3),
    "m": (1, 3, 4),
    "n": (1, 3, 4, 5),
    "o": (1, 3, 5),
    "p": (1, 2, 3, 4),
    "q": (1, 2, 3, 4, 5),
    "r": (1, 2, 3, 5),
    "s": (2, 3, 4),
    "t": (2, 3, 4, 5),
    "u": (1, 3, 6),
    "v": (1, 2, 3, 6),
    "w": (2, 4, 5, 6),
    "x": (1, 3, 4, 6),
    "y": (1, 3, 4, 5, 6),
    "z": (1, 3, 5, 6),
}

_LETTER_TO_CHAR = {
    letter: chr(0x2800 + sum(1 << (dot - 1) for dot in dots))
    for letter, dots in _DOTS.items()
}
_CHAR_TO_LETTER = {char: letter for letter, char in _LETTER_TO_CHAR.items()}
_BLANK_CELL = "⠀"


def to_braille(text):
    """把小写 a–z 与空格转成一级盲文；空格转 U+2800，空串返回空串。"""
    if not isinstance(text, str):
        raise TypeError("to_braille() expected str, got %s" % type(text).__name__)
    parts = []
    for ch in text:
        if ch == " ":
            parts.append(_BLANK_CELL)
        elif ch in _LETTER_TO_CHAR:
            parts.append(_LETTER_TO_CHAR[ch])
        else:
            raise ValueError("unsupported character for to_braille: %r" % (ch,))
    return "".join(parts)


def from_braille(text):
    """把一级盲文转回小写 a–z 与空格；U+2800 转空格，空串返回空串。"""
    if not isinstance(text, str):
        raise TypeError("from_braille() expected str, got %s" % type(text).__name__)
    parts = []
    for ch in text:
        if ch == _BLANK_CELL:
            parts.append(" ")
        elif ch in _CHAR_TO_LETTER:
            parts.append(_CHAR_TO_LETTER[ch])
        else:
            raise ValueError("unsupported braille character: %r" % (ch,))
    return "".join(parts)
