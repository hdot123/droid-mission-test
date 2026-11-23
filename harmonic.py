"""harmonic: 调和数精确分数计算（第五十四轮并发 D 单组件）。

H_n = Σ_{k=1}^{n} 1/k，以 fractions.Fraction 精确表示；H_0 = Fraction(0)。
"""

from fractions import Fraction


def harmonic(n):
    """返回第 n 个调和数 H_n 的精确分数。

    n 须为 int（bool 拒）；n < 0 抛 ValueError；非 int 抛 TypeError。
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int, got %r" % (n,))
    if n < 0:
        raise ValueError("n must be >= 0, got %r" % (n,))
    total = Fraction(0)
    for k in range(1, n + 1):
        total += Fraction(1, k)
    return total
