"""macaddr: MAC 地址规范化工具。

接受三种入参形态——冒号分隔（``AA:BB:CC:DD:EE:FF``）、连字符分隔
（``AA-BB-CC-DD-EE-FF``）、点分隔三组四位（``AABB.CCDD.EEFF``），
大小写不限；输出统一为小写冒号分隔形态。组数、每组长度、非十六进制
字符或混合分隔符不合规时抛出 ValueError。
"""

import re

_COLON = re.compile(r"\A[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}\Z")
_HYPHEN = re.compile(r"\A[0-9A-Fa-f]{2}(?:-[0-9A-Fa-f]{2}){5}\Z")
_DOT = re.compile(r"\A[0-9A-Fa-f]{4}(?:\.[0-9A-Fa-f]{4}){2}\Z")


def normalize(text: str) -> str:
    """把三种合规形态的 MAC 地址统一为小写冒号分隔形态，不合规抛 ValueError。"""
    if not isinstance(text, str):
        raise ValueError("invalid MAC address: %r" % (text,))
    if _COLON.fullmatch(text):
        return text.lower()
    if _HYPHEN.fullmatch(text):
        return text.replace("-", ":").lower()
    if _DOT.fullmatch(text):
        octets = []
        for group in text.split("."):
            octets.extend([group[:2], group[2:]])
        return ":".join(octets).lower()
    raise ValueError("invalid MAC address: %r" % (text,))
