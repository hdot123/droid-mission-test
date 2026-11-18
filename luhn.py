"""luhn: Luhn 校验码工具。

提供 Luhn 算法的校验位判定与校验位计算两个独立函数，
只依赖标准库，不依赖本仓库其他模块。
"""

__all__ = ["is_valid", "check_digit"]


def _digits(value, name):
    """校验入参是非空纯数字串，返回数字列表；否则抛 ValueError。"""
    if not isinstance(value, str) or not value:
        raise ValueError("invalid %s: %r" % (name, value))
    if any(ch < "0" or ch > "9" for ch in value):
        raise ValueError("invalid %s: %r" % (name, value))
    return [ord(ch) - 48 for ch in value]


def is_valid(number: str) -> bool:
    """按 Luhn 算法判定数字串是否有效；非空纯数字串以外入参抛 ValueError。

    自右起（含末位）隔位乘 2，乘积大于 9 减 9，总和被 10 整除即有效。
    """
    total = 0
    for index, digit in enumerate(reversed(_digits(number, "number"))):
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def check_digit(payload: str) -> int:
    """返回追加到 payload 末尾后使 Luhn 校验通过的 0-9 数字。

    非空纯数字串以外入参抛 ValueError。
    """
    total = 0
    for index, digit in enumerate(reversed(_digits(payload, "payload"))):
        if index % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return (10 - total % 10) % 10
