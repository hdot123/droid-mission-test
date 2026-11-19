"""Hill 密码（2×2 矩阵，mod 26）。

明文预处理为大写并去除非字母（26 个字母全部保留，J 不并入 I，与 Playfair 不同），
按双字母分组，奇数长度末尾补 X；因此密文长度恒为偶数。
加密为明文对向量左乘 key 矩阵 mod 26；解密为左乘伴随矩阵乘 det 的模逆元 mod 26，
返回含补位 X 的制备明文（不剥离补位）。
"""

from math import gcd

__all__ = ["hill_encrypt", "hill_decrypt"]


def _check_key(key):
    """校验 2×2 密钥矩阵，返回 ((a, b), (c, d))。

    - key 不是矩阵（非 tuple/list，或行不是 tuple/list，或元素非 int）抛 TypeError；
    - 形状不对、元素超出 0–25、行列式与 26 不互素抛 ValueError。
    """
    if not isinstance(key, (tuple, list)):
        raise TypeError("key must be a 2x2 matrix, got %s" % type(key).__name__)
    rows = list(key)
    if not all(isinstance(r, (tuple, list)) for r in rows):
        raise TypeError("key must be a 2x2 matrix, got %s" % type(key).__name__)
    flat = [x for r in rows for x in r]
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in flat):
        raise TypeError("key elements must be int")
    if len(rows) != 2 or any(len(r) != 2 for r in rows):
        raise ValueError("key must be a 2x2 matrix")
    if not all(0 <= x <= 25 for x in flat):
        raise ValueError("key elements must be in 0..25")
    a, b = rows[0]
    c, d = rows[1]
    det = a * d - b * c
    if gcd(det, 26) != 1:
        raise ValueError("key determinant must be coprime with 26")
    return (a, b), (c, d)


def _letters(text):
    """转大写并只保留 A–Z（26 个字母全保留，J 不并入 I）。"""
    return [ch for ch in text.upper() if "A" <= ch <= "Z"]


def hill_encrypt(text: str, key) -> str:
    """用 2×2 Hill 密钥加密明文；奇数长度补 X，空串返回空串。"""
    if not isinstance(text, str):
        raise TypeError("text must be str, got %s" % type(text).__name__)
    (a, b), (c, d) = _check_key(key)
    chars = _letters(text)
    if not chars:
        return ""
    if len(chars) % 2 == 1:
        chars.append("X")
    out = []
    for i in range(0, len(chars), 2):
        x = ord(chars[i]) - 65
        y = ord(chars[i + 1]) - 65
        out.append(chr((a * x + b * y) % 26 + 65))
        out.append(chr((c * x + d * y) % 26 + 65))
    return "".join(out)


def hill_decrypt(cipher: str, key) -> str:
    """Hill 逆运算，返回含补位 X 的制备明文；密文奇数长度抛 ValueError。"""
    if not isinstance(cipher, str):
        raise TypeError("cipher must be str, got %s" % type(cipher).__name__)
    (a, b), (c, d) = _check_key(key)
    if len(cipher) % 2 == 1:
        raise ValueError("ciphertext length must be even, got %d" % len(cipher))
    if not cipher:
        return ""
    det = a * d - b * c
    inv = pow(det % 26, -1, 26)
    # 伴随矩阵 adj = ((d, -b), (-c, a)) 乘 det 模逆元 mod 26
    i00 = (d * inv) % 26
    i01 = (-b * inv) % 26
    i10 = (-c * inv) % 26
    i11 = (a * inv) % 26
    text = cipher.upper()
    out = []
    for i in range(0, len(text), 2):
        x = ord(text[i]) - 65
        y = ord(text[i + 1]) - 65
        out.append(chr((i00 * x + i01 * y) % 26 + 65))
        out.append(chr((i10 * x + i11 * y) % 26 + 65))
    return "".join(out)
