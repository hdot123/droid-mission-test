"""abacheck: ABA 路由号校验位（新增小组件）。

位权序自左起按 3、7、1 循环（第 1 位权 3、第 2 位权 7、第 3 位权 1、
第 4 位权 3、……），与 Luhn 倍替求和、IBAN 模 97、Damm 准群表均不同算法。
"""

_WEIGHTS = (3, 7, 1)


def _check_shape(value, expected_len, name):
    """入参形态校验：非 str 抛 TypeError，长度不符或含非数字字符抛 ValueError。"""
    if not isinstance(value, str):
        raise TypeError("%s must be str, got %s" % (name, type(value).__name__))
    if len(value) != expected_len:
        raise ValueError("%s must be exactly %d characters" % (name, expected_len))
    if not all("0" <= ch <= "9" for ch in value):
        raise ValueError("%s must contain only digits" % name)


def _weighted_sum(digits):
    """按自左起 3/7/1 循环位权求加权和。"""
    return sum(d * _WEIGHTS[i % 3] for i, d in enumerate(digits))


def aba_check_digit(first8: str) -> str:
    """8 位数字串的 ABA 校验位：加权和模 10 取补，返回单字符字符串。

    形态不合（长度／非数字）抛 ValueError；非 str 抛 TypeError。
    """
    _check_shape(first8, 8, "first8")
    total = _weighted_sum(int(ch) for ch in first8)
    return str((10 - total % 10) % 10)


def aba_validate(number: str) -> bool:
    """9 位数字串的 ABA 校验：九位按同一位权序（第 9 位权 1）加权和模 10 为 0。

    校验不合只返回 False、不抛错；只有形态不合（长度／非数字）才抛 ValueError，
    非 str 抛 TypeError。
    """
    _check_shape(number, 9, "number")
    total = _weighted_sum(int(ch) for ch in number)
    return total % 10 == 0
