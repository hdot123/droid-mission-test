"""factorial: 阶乘与二项式系数（第四十二轮 C 单）。

仅使用标准库；本模块不 import fib 或 sieve（三个模块互不依赖）。
"""


def factorial(n: int) -> int:
    """返回 n 的阶乘 n!（factorial(0) = 1）；n 为负数抛 ValueError。"""
    if n < 0:
        raise ValueError("n must be non-negative, got %r" % (n,))
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def binom(n: int, k: int) -> int:
    """返回二项式系数 C(n, k)；须满足 0 <= k <= n，否则抛 ValueError。"""
    if k < 0 or k > n:
        raise ValueError("require 0 <= k <= n, got n=%r k=%r" % (n, k))
    # C(n, k) = n! / (k! * (n - k)!)，用乘法累加避免中间除法截断。
    k = min(k, n - k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result
