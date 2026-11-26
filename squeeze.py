"""squeeze: 重复段压缩（只删重复，不产出计数）。

- squeeze_chars：任意字符的连续重复段压为一个（大小写敏感）。
- squeeze_spaces：空白段（str.isspace 口径，含制表／换行等）压为单个
  ASCII 空格；不去首尾——首尾空白段同样压为一个空格保留。

本模块只做去重，不产出 (字符, 计数) 对——与 run-length 编码语义不同。
只用标准库。
"""

__all__ = ["squeeze_chars", "squeeze_spaces"]


def squeeze_chars(text: str) -> str:
    """把 text 中每个连续重复的字符压为一个（大小写敏感）；非 str 抛 TypeError。"""
    if not isinstance(text, str):
        raise TypeError("squeeze_chars() expected str, got %r" % (type(text).__name__,))
    out = []
    prev = None
    for ch in text:
        if ch != prev:
            out.append(ch)
            prev = ch
    return "".join(out)


def squeeze_spaces(text: str) -> str:
    """把 text 中每个空白段（str.isspace 口径）压为一个 ASCII 空格，不去首尾。

    非 str 抛 TypeError。
    """
    if not isinstance(text, str):
        raise TypeError("squeeze_spaces() expected str, got %r" % (type(text).__name__,))
    out = []
    in_space = False
    for ch in text:
        if ch.isspace():
            if not in_space:
                out.append(" ")
                in_space = True
        else:
            out.append(ch)
            in_space = False
    return "".join(out)
