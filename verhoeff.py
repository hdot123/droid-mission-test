"""verhoeff: Verhoeff check digit computation and validation (第四十三轮 · A 单).

只使用标准库。checksum 对不含校验位的纯数字串计算 Verhoeff 校验数字；
validate 校验含末位校验位的整串。
"""

# 乘法表 d，标准 Verhoeff (dihedral group D5) 定义。
_D = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
)

# 置换表 p，标准 Verhoeff 定义。
_P = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
)

# 逆元表 inv，标准 Verhoeff 定义。
_INV = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)


def _digits_to_values(digits: str) -> list:
    """把纯数字串转为整数列表；空串或含非数字字符抛 ValueError。"""
    if not isinstance(digits, str):
        raise ValueError("expected a decimal string, got %r" % (digits,))
    if not digits:
        raise ValueError("empty digits string")
    values = []
    for ch in digits:
        if ch < "0" or ch > "9":
            raise ValueError("non-digit character: %r" % (ch,))
        values.append(ord(ch) - 48)
    return values


def checksum(digits: str) -> int:
    """对不含校验位的纯数字串计算 Verhoeff 校验数字（0–9）。

    空串或含非数字字符抛 ValueError。
    """
    values = _digits_to_values(digits)
    # 校验位位于最右侧（倒数第 1 位，置换下标 0），故本串各位的置换下标从 1 起；
    # 折叠结果 c 即校验位的群元素，取逆元即为校验数字。
    c = 0
    for i, v in enumerate(reversed(values)):
        c = _D[c][_P[(i + 1) % 8][v]]
    return _INV[c]


def validate(digits: str) -> bool:
    """校验含末位校验位的整串；通过返回 True，否则 False。

    空串或含非数字字符抛 ValueError。
    """
    values = _digits_to_values(digits)
    # 完整串的 Verhoeff 折叠值应为 0 才算通过。
    c = 0
    for i, v in enumerate(reversed(values)):
        c = _D[c][_P[i % 8][v]]
    return c == 0
