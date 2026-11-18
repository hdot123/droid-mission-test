"""rle 编解码器插件：导入时向 codecbox 目录登记名为 "rle" 的编解码对。

encode 把每段连续相同字符写成「字符＋段长」，decode 为其逆运算（输入限英文字母）。
"""

import codecbox


def encode(text):
    """把每段连续相同字符写成「字符＋段长」："" -> ""，"aaab" -> "a3b1"，"abc" -> "a1b1c1"。"""
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
    """encode 的逆运算：把「字符＋段长」还原为连续相同字符序列（输入限英文字母）。"""
    if not text:
        return ""
    result = []
    i = 0
    while i < len(text):
        ch = text[i]
        j = i + 1
        while j < len(text) and text[j].isdigit():
            j += 1
        result.append(ch * int(text[i + 1 : j]))
        i = j
    return "".join(result)


codecbox.add_codec("rle", encode, decode)
