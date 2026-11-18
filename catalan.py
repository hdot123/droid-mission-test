"""catalan: 卡特兰数 C_n（第四十三轮新增组件）。

实现只依赖标准库，函数行为以文档字符串为准。
"""

from math import comb


def catalan(n: int) -> int:
    """返回第 n 个卡特兰数 C_n（C_0 = 1）；n 为负数抛 ValueError。"""
    if n < 0:
        raise ValueError("n must be non-negative: %r" % (n,))
    return comb(2 * n, n) // (n + 1)
