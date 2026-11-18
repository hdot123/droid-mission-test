"""atbash: Atbash 密码（字母按 a↔z 镜像的自逆替换）。"""

_LOWER_A = ord("a")
_LOWER_Z = ord("z")
_UPPER_A = ord("A")
_UPPER_Z = ord("Z")


def atbash(text: str) -> str:
    """字母按 Atbash 规则镜像（a↔z、b↔y、…，A↔Z、B↔Y、…）。

    大小写保持不变；非字母字符（含空格、标点、数字）原样保留。
    该变换是自逆的：atbash(atbash(s)) == s。
    """
    out = []
    for ch in text:
        code = ord(ch)
        if _LOWER_A <= code <= _LOWER_Z:
            out.append(chr(_LOWER_Z - (code - _LOWER_A)))
        elif _UPPER_A <= code <= _UPPER_Z:
            out.append(chr(_UPPER_Z - (code - _UPPER_A)))
        else:
            out.append(ch)
    return "".join(out)
