"""hexcodec: 十六进制编解码小组件（第三十八轮 · 并发 B 单）。

只用标准库，不依赖仓库内其他模块。行为以本模块文档字符串为准。
"""

import string


def encode(data: bytes) -> str:
    """小写十六进制、无分隔符；空 bytes 返回空串。"""
    return data.hex()


def decode(text: str) -> bytes:
    """接受大小写混合；长度为奇数或含非十六进制字符抛 ValueError；空串返回空 bytes。"""
    if len(text) % 2 != 0:
        raise ValueError("odd-length hex string: %r" % (text,))
    for ch in text:
        if ch not in string.hexdigits:
            raise ValueError("invalid hex character: %r" % (ch,))
    return bytes.fromhex(text)


def encode_spaced(data: bytes) -> str:
    """小写十六进制、每字节以单个空格分隔（如 "00 ff"）；空 bytes 返回空串。"""
    if not data:
        return ""
    return " ".join("%02x" % b for b in data)
