"""unaccent: 去重音符号（剥离附加符号）组件。

strip_accents(text) -> str：先做 NFD 分解，删除全部 category = Mn 的组合记号，
再 NFC 重组。无分解映射的字母（æ / ø / đ 等）原样保留（规格明示，不是遗漏）。
入参非 str 抛 TypeError。仅用标准库。
"""

import unicodedata


def strip_accents(text: str) -> str:
    """NFD 分解后删除全部 Mn 类组合记号，再 NFC 重组；非 str 抛 TypeError。"""
    if not isinstance(text, str):
        raise TypeError("strip_accents() requires str, got %s" % type(text).__name__)
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", stripped)
