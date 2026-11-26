"""divisorsum: 约数和与盈亏分类工具（第五十五轮并发 C 单）。

口径注记：本模块 σ(n) 含本身，与真约数和（不含本身）口径不同，勿混。
"""


def _check(n):
    """入参约定：非 int（含 bool）抛 TypeError；n < 1 抛 ValueError。"""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("expected int, got %r" % (type(n).__name__,))
    if n < 1:
        raise ValueError("n must be >= 1, got %r" % (n,))


def _divisors(n):
    """返回 n 的全部正约数（含本身），未排序。"""
    divs = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divs.append(i)
            j = n // i
            if j != i:
                divs.append(j)
        i += 1
    return divs


def divisor_sum(n: int) -> int:
    """σ(n)：n 的全部正约数之和（含本身，σ(1) = 1）。"""
    _check(n)
    return sum(_divisors(n))


def divisor_count(n) -> int:
    """τ(n)：n 的正约数个数。"""
    _check(n)
    return len(_divisors(n))


def classify_abundance(n) -> str:
    """按 σ(n) 与 2n 比较返回 "perfect" / "abundant" / "deficient"。"""
    _check(n)
    sigma = sum(_divisors(n))
    if sigma == 2 * n:
        return "perfect"
    if sigma > 2 * n:
        return "abundant"
    return "deficient"
