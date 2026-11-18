"""codec_flip: 导入本模块即向 codecbox 登记名为 flip 的编解码器。

encode 与 decode 均为字符串翻转（互为逆运算）。
"""

import codecbox


def encode(text):
    """把字符串翻转。"""
    return text[::-1]


def decode(text):
    """把字符串翻转（encode 的逆运算）。"""
    return text[::-1]


codecbox.add_codec("flip", encode, decode)
