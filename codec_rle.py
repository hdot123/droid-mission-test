"""rle 编解码器插件：导入本模块时即向 codecbox 目录登记名为 "rle" 的编解码器。

encode 把每段连续相同字符写成「字符＋段长」，decode 为其逆运算（输入限英文字母）。
"""

import codecbox


def encode(text):
    """每段连续相同字符写成 字符+段长，如 "aaab" -> "a3b1"、"abc" -> "a1b1c1"。"""
    if not text:
        return ""
    parts = []
    run_char = text[0]
    run_len = 1
    for ch in text[1:]:
        if ch == run_char:
            run_len += 1
        else:
            parts.append(run_char + str(run_len))
            run_char = ch
            run_len = 1
    parts.append(run_char + str(run_len))
    return "".join(parts)


def decode(text):
    """encode 的逆运算：如 "a3b1" -> "aaab"（输入为 encode 的输出，限英文字母）。"""
    if not text:
        return ""
    parts = []
    i = 0
    while i < len(text):
        ch = text[i]
        i += 1
        digits = []
        while i < len(text) and text[i].isdigit():
            digits.append(text[i])
            i += 1
        parts.append(ch * int("".join(digits)))
    return "".join(parts)


codecbox.add_codec("rle", encode, decode)
