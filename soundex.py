"""soundex: 美式 Soundex 语音编码（第四十一轮 · 自实现）。

只接受非空纯 ASCII 字母串（大小写不敏感），否则抛 ValueError。
首字母原样保留（转大写），后续字母按编码表映射：
bfpv→1、cgjkqsxz→2、dt→3、l→4、mn→5、r→6；
元音 aeiouy 不产码且隔断同码折叠；h、w 不产码且不隔断（透明）；
相邻同码折叠为一码（首字母自身的编码亦参与折叠）；
结果为首字母＋3 位数字，不足补 0、超长截断至 4 字符。
"""

_CODES = {
    "b": "1", "f": "1", "p": "1", "v": "1",
    "c": "2", "g": "2", "j": "2", "k": "2", "q": "2", "s": "2", "x": "2", "z": "2",
    "d": "3", "t": "3",
    "l": "4",
    "m": "5", "n": "5",
    "r": "6",
}

_VOWELS = "aeiouy"
_TRANSPARENT = "hw"


def soundex(name: str) -> str:
    """返回 name 的美式 Soundex 码；非空纯 ASCII 字母串以外的输入抛 ValueError。"""
    if not isinstance(name, str) or not (name.isascii() and name.isalpha()):
        raise ValueError("invalid soundex input: %r" % (name,))
    lower = name.lower()
    first = lower[0]
    # 首字母自身的编码参与后续折叠：元音/h/w 首字母无编码（None）。
    prev = _CODES.get(first)
    digits = []
    for ch in lower[1:]:
        if ch in _VOWELS:
            prev = None  # 元音隔断同码折叠
        elif ch in _TRANSPARENT:
            continue  # h、w 透明，不产码也不隔断
        else:
            code = _CODES[ch]
            if code != prev:
                digits.append(code)
                prev = code
    return first.upper() + "".join(digits)[:3].ljust(3, "0")
