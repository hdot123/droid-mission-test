"""pangram: 全字母句判定与缺失字母列表（第 46 轮 B）。

仅用标准库，不依赖仓库内其他模块。
"""

_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def _letters(text: str) -> set:
    if not isinstance(text, str):
        raise TypeError("text must be str, got %s" % type(text).__name__)
    return {ch.lower() for ch in text if ch.isalpha()}


def is_pangram(text: str) -> bool:
    """大小写不敏感、忽略非字母；26 个小写字母全出现返回 True。"""
    return set(_ALPHABET) <= _letters(text)


def missing_letters(text: str) -> list:
    """返回未出现的小写字母排序列表。"""
    seen = _letters(text)
    return [ch for ch in _ALPHABET if ch not in seen]
