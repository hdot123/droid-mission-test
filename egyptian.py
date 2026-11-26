"""egyptian: 埃及分数（贪心 Sylvester 单位分数展开）。

给定正有理数 p/q，贪心展开：每一步取不超过当前余数的**最大**单位分数
1/d（d = ceil(q/p)），减去后对余数约分，重复直到余数为 0，返回分母列。
入参未约分时先约分（如 egyptian(2, 6) 按 1/3 展开）。

只用标准库；本模块是纯文本/数值展开，与分数四则运算类模块（fractionx 等）
无关，也不互相引用。
"""

from math import gcd


def egyptian(p: int, q: int) -> list[int]:
    """返回正有理数 p/q 的贪心（Sylvester）单位分数展开分母列。

    每步取 <= 当前余数的最大单位分数，分母列由贪心唯一确定。
    入参约定：p < 1 或 q < 1 抛 ValueError；非 int（含 bool）抛 TypeError。
    """
    if (
        isinstance(p, bool)
        or isinstance(q, bool)
        or not isinstance(p, int)
        or not isinstance(q, int)
    ):
        raise TypeError(
            "egyptian() requires int arguments, got %r, %r" % (p, q)
        )
    if p < 1 or q < 1:
        raise ValueError("p and q must be >= 1, got p=%d, q=%d" % (p, q))

    g = gcd(p, q)
    p //= g
    q //= g

    denoms: list[int] = []
    while p > 0:
        # 不超过 p/q 的最大单位分数是 1/ceil(q/p)。
        d = -(-q // p)
        denoms.append(d)
        p, q = p * d - q, q * d
        g = gcd(p, q)
        p //= g
        q //= g
    return denoms
