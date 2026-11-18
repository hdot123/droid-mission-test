"""vigenere: 维吉尼亚密码（第四十轮 · E 单 · 子卡 #367）。

encrypt(text, key) / decrypt(text, key)：
- key 必须是非空、只含 ASCII 字母的字符串（大小写不敏感），否则抛 ValueError；
- 只变换 ASCII 字母，大小写保持不变；
- 非字母字符原样保留，且不推进 key 位置。
"""

__all__ = ["encrypt", "decrypt"]


def _validate_key(key):
    """key 须为非空且只含 ASCII 字母，否则抛 ValueError。"""
    if not isinstance(key, str) or not key:
        raise ValueError("key must be a non-empty string: %r" % (key,))
    if not all(("A" <= ch <= "Z") or ("a" <= ch <= "z") for ch in key):
        raise ValueError("key must contain only ASCII letters: %r" % (key,))


def _is_ascii_letter(ch):
    """只有 ASCII 字母参与移位。"""
    return ("A" <= ch <= "Z") or ("a" <= ch <= "z")


def _shift_char(ch, amount):
    """把单个 ASCII 字母移 amount 位（mod 26），大小写保持不变。"""
    base = ord("A") if "A" <= ch <= "Z" else ord("a")
    return chr((ord(ch) - base + amount) % 26 + base)


def _transform(text, key, direction):
    """按 key 逐字母移位；direction 为 1（加密）或 -1（解密）。"""
    _validate_key(key)
    out = []
    pos = 0
    for ch in text:
        if _is_ascii_letter(ch):
            amount = ord(key[pos % len(key)].lower()) - ord("a")
            out.append(_shift_char(ch, direction * amount))
            pos += 1
        else:
            out.append(ch)
    return "".join(out)


def encrypt(text: str, key: str) -> str:
    """用 key 对 text 做维吉尼亚加密；非字母字符不推进 key 位置。"""
    return _transform(text, key, 1)


def decrypt(text: str, key: str) -> str:
    """用 key 对 text 做维吉尼亚解密，encrypt 的逆运算。"""
    return _transform(text, key, -1)
