"""Trifid 密码（3×3×3 立方、周期分置）。

字母表钉死为 ``ABCDEFGHIJKLMNOPQRSTUVWXYZ+``（27 个字符），按顺序依次填充
3×3×3 立方：字符下标 i（0 起）对应坐标（层，行，列）
= (i//9 + 1, (i mod 9)//3 + 1, i mod 3 + 1)，坐标均为 1–3。

只用标准库，不依赖任何其他模块。
"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ+"

_CUBESIDE = 3
_LAYER_SIZE = 9


def _validate_period(period):
    """period 须为正 int：非 int 抛 TypeError，<= 0 抛 ValueError。"""
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period must be an int, got %r" % (type(period).__name__,))
    if period <= 0:
        raise ValueError("period must be positive, got %r" % (period,))


def _validate_text(text):
    """text/cipher 须为 str，否则抛 TypeError。"""
    if not isinstance(text, str):
        raise TypeError("expected str, got %r" % (type(text).__name__,))


def _preprocess(text):
    """明文预处理为大写、只保留字母表内字符。"""
    upper = text.upper()
    return "".join(ch for ch in upper if ch in ALPHABET)


def _coords(ch):
    """字符 -> (层, 行, 列)，坐标 1–3。"""
    i = ALPHABET.index(ch)
    return (i // _LAYER_SIZE + 1,
            (i % _LAYER_SIZE) // _CUBESIDE + 1,
            i % _CUBESIDE + 1)


def _char_from_coords(layer, row, col):
    """(层, 行, 列) -> 字符。"""
    i = (layer - 1) * _LAYER_SIZE + (row - 1) * _CUBESIDE + (col - 1)
    return ALPHABET[i]


def trifid_encrypt(text: str, period: int = 5) -> str:
    """Trifid 加密。

    明文预处理为大写、只保留字母表内字符；按 period 个字符分组（末组可短）：
    组内先逐字写下三坐标的第一分量（层）成行、再写第二分量（行）成行、
    再写第三分量（列）成行，三行首尾相接成数字串，再按每 3 个数字一组
    （三坐标）映射回字符。空串返回空串。
    """
    _validate_text(text)
    _validate_period(period)
    plain = _preprocess(text)
    if not plain:
        return ""
    out = []
    for start in range(0, len(plain), period):
        group = plain[start:start + period]
        triples = [_coords(ch) for ch in group]
        digits = "".join(str(t[0]) for t in triples) \
            + "".join(str(t[1]) for t in triples) \
            + "".join(str(t[2]) for t in triples)
        for k in range(0, len(digits), 3):
            layer = int(digits[k])
            row = int(digits[k + 1])
            col = int(digits[k + 2])
            out.append(_char_from_coords(layer, row, col))
    return "".join(out)


def trifid_decrypt(cipher: str, period: int = 5) -> str:
    """Trifid 解密（trifid_encrypt 的逆运算）。

    同分组：先把组内每字的三坐标横写成数字串，再均分为三行、逐列读出
    三坐标还原字符；返回制备后的明文。空串返回空串。
    """
    _validate_text(cipher)
    _validate_period(period)
    prepared = _preprocess(cipher)
    if not prepared:
        return ""
    out = []
    for start in range(0, len(prepared), period):
        group = prepared[start:start + period]
        digits = "".join("".join(str(c) for c in _coords(ch)) for ch in group)
        third = len(digits) // 3
        layers = digits[:third]
        rows = digits[third:2 * third]
        cols = digits[2 * third:]
        for k in range(third):
            out.append(_char_from_coords(int(layers[k]),
                                         int(rows[k]),
                                         int(cols[k])))
    return "".join(out)


__all__ = ["ALPHABET", "trifid_encrypt", "trifid_decrypt"]
