"""damm: Damm 算法校验位（新增组件，仅标准库）。

准群运算表钉死如下（行 = 当前中间位 interim，列 = 下一位数字，
初始 interim = 0，逐位替换 interim = 表[interim][数字]）。
因表对角线全 0，校验位直接取处理完整串后的最终 interim，无附加变换。
"""

_TABLE = (
    (0, 3, 1, 7, 5, 9, 8, 6, 4, 2),
    (7, 0, 9, 2, 1, 5, 4, 8, 6, 3),
    (4, 2, 0, 6, 8, 7, 1, 3, 5, 9),
    (1, 7, 5, 0, 9, 8, 3, 4, 2, 6),
    (6, 1, 2, 3, 0, 4, 5, 9, 7, 8),
    (3, 6, 7, 4, 2, 0, 9, 5, 8, 1),
    (5, 8, 6, 9, 7, 2, 0, 1, 3, 4),
    (8, 9, 4, 5, 3, 6, 2, 0, 1, 7),
    (9, 4, 3, 8, 6, 1, 7, 2, 0, 5),
    (2, 5, 8, 1, 4, 3, 6, 7, 9, 0),
)

_DIGITS = "0123456789"


def _interim(number):
    """逐位算出最终 interim；入参非 str 抛 TypeError，空串或含非 ASCII 数字抛 ValueError。"""
    if not isinstance(number, str):
        raise TypeError("number must be str, got %r" % (type(number).__name__,))
    if not number:
        raise ValueError("number must be a non-empty digit string")
    interim = 0
    for ch in number:
        if ch not in _DIGITS:
            raise ValueError("invalid digit character: %r" % (ch,))
        interim = _TABLE[interim][ord(ch) - 48]
    return interim


def damm_check_digit(number):
    """返回不含校验位的数字串对应的校验位字符串（最终 interim 本身）。"""
    return str(_interim(number))


def damm_validate(number):
    """校验含校验位的完整数字串：全串处理后 interim == 0 返回 True，否则 False。"""
    return _interim(number) == 0
