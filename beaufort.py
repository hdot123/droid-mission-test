"""beaufort: Beaufort 密码小组件（第四十三轮 · 并发 B 单）。

`beaufort(text, key)` 按 Beaufort 规则 (key_letter - plain_letter) mod 26
加密字母：key 在字母上循环、大小写不敏感；保留原文大小写，非字母原样保留；
key 为空串抛 ValueError。仅用标准库，不依赖仓库内其他模块。
"""


def beaufort(text: str, key: str) -> str:
    """用 Beaufort 规则加密文本。

    对每个字母取当前 key 字母，密文 = (key_letter - plain_letter) mod 26。
    key 仅在遇到字母时向前推进（非字母不消耗 key）。
    保留原文大小写；非字母原样保留；key 为空串抛 ValueError。
    """
    if not key:
        raise ValueError("key must be a non-empty string")
    parts = []
    key_index = 0
    for ch in text:
        if not ch.isalpha():
            parts.append(ch)
            continue
        plain = ord(ch.lower()) - ord("a")
        key_letter = ord(key[key_index % len(key)].lower()) - ord("a")
        key_index += 1
        cipher_val = (key_letter - plain) % 26
        cipher_ch = chr(ord("a") + cipher_val)
        parts.append(cipher_ch.upper() if ch.isupper() else cipher_ch)
    return "".join(parts)
