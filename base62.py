"""base62: 整数与 Base62 字符串互转。

字母表钉死为 ``0-9A-Za-z``（下标 0–61 依次对应字符值）。
只用标准库，不依赖仓库内其他模块。
"""

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

_DECODE_MAP = {ch: i for i, ch in enumerate(ALPHABET)}


def base62_encode(n: int) -> str:
    """把非负整数 n 编码为 Base62 字符串。

    n 必须是 int（bool 拒），否则抛 TypeError；n < 0 抛 ValueError。
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int, got %r" % (type(n).__name__,))
    if n < 0:
        raise ValueError("n must be >= 0, got %r" % (n,))
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        n, rem = divmod(n, 62)
        digits.append(ALPHABET[rem])
    return "".join(reversed(digits))


def base62_decode(s: str) -> int:
    """把 Base62 字符串解码为整数。

    s 必须是 str，否则抛 TypeError；空串或含字母表外字符抛 ValueError。
    """
    if not isinstance(s, str):
        raise TypeError("s must be str, got %r" % (type(s).__name__,))
    if not s:
        raise ValueError("s must not be empty")
    total = 0
    for ch in s:
        value = _DECODE_MAP.get(ch)
        if value is None:
            raise ValueError("invalid Base62 character: %r" % (ch,))
        total = total * 62 + value
    return total
