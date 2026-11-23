"""ISSN 校验位计算与校验（第五十四轮 · 并发 C 单）。

本模块只依赖标准库，不依赖仓库内其他模块。函数行为以文档字符串为准：
`issn_check_digit` 计算前 7 位的 ISSN 校验位，`issn_validate` 校验完整
ISSN 字符串（8 位无分隔或 9 位带连字符两种形态）。
"""

__all__ = ["issn_check_digit", "issn_validate"]

_WEIGHTS = (8, 7, 6, 5, 4, 3, 2)


def issn_check_digit(seven: str) -> str:
    """计算 7 位 ISSN 前缀的校验位。

    seven 必须是恰好 7 位 ASCII 数字的字符串，否则抛 TypeError/ValueError。
    算法：前 7 位依次乘权重 8、7、6、5、4、3、2 求和，
    check = (11 − (sum % 11)) % 11；check == 10 返回 "X"，
    否则返回该数字的一位字符串。
    """
    if not isinstance(seven, str):
        raise TypeError("seven must be a str")
    if len(seven) != 7 or not seven.isdigit() or not seven.isascii():
        raise ValueError("seven must be exactly 7 ASCII digits")
    total = sum(int(d) * w for d, w in zip(seven, _WEIGHTS))
    check = (11 - (total % 11)) % 11
    return "X" if check == 10 else str(check)


def issn_validate(code: str) -> bool:
    """校验完整 ISSN 字符串。

    code 非 str 抛 TypeError。接受两种形态：
    8 位无分隔（前 7 位数字＋末位数字或大写 X），或
    9 位带连字符（第 5 个字符为 '-'，去掉后同前一种）。
    形态不合一律返回 False、不抛错；形态合则按 issn_check_digit 核对末位，
    一致返回 True，否则 False。
    """
    if not isinstance(code, str):
        raise TypeError("code must be a str")

    if len(code) == 9:
        if code[4] != "-":
            return False
        compact = code[:4] + code[5:]
    elif len(code) == 8:
        compact = code
    else:
        return False

    first7 = compact[:7]
    last = compact[7]
    if not (first7.isdigit() and first7.isascii()):
        return False
    if not (last.isdigit() or last == "X"):
        return False
    return last == issn_check_digit(first7)
