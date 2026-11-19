"""crt: 中国剩余定理求解器（第四十六轮 · 并发 C 单）。

给定两两互素的模数与对应余数，求满足全部同余式的最小非负解。
只用标准库，不依赖仓库内其他模块。
"""

from math import gcd


def crt(remainders, moduli):
    """返回最小非负整数 x，使 x ≡ remainders[i] (mod moduli[i]) 对所有 i 成立。

    remainders 与 moduli 必须是等长非空的 list/tuple，元素均为 int；
    模数须 >= 2、余数须满足 0 <= r < m、模数须两两互素。
    类型错误抛 TypeError，取值/结构错误抛 ValueError。
    """
    if not isinstance(remainders, (list, tuple)) or not isinstance(
        moduli, (list, tuple)
    ):
        raise TypeError("remainders and moduli must be list or tuple")
    if len(remainders) != len(moduli):
        raise ValueError("remainders and moduli must have equal length")
    if len(remainders) == 0:
        raise ValueError("remainders and moduli must be non-empty")
    for value in remainders:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("remainders must contain only int")
    for value in moduli:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("moduli must contain only int")
    for r, m in zip(remainders, moduli):
        if m < 2:
            raise ValueError("modulus must be >= 2")
        if not (0 <= r < m):
            raise ValueError("remainder out of range: %r (mod %r)" % (r, m))
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                raise ValueError("moduli must be pairwise coprime")

    total = 1
    for m in moduli:
        total *= m
    x = 0
    for r, m in zip(remainders, moduli):
        partial = total // m
        x += r * partial * pow(partial, -1, m)
    return x % total
