"""partitions: 整数分拆数 p(n)（第五十轮 C 单 · 领班制 v2.7.0）。

返回正整数 n 的分拆数，即次序无关的加法分解个数，结果为精确整数。
约定 partitions(0) == 1（空分拆）。仅用标准库。
"""

from functools import lru_cache

__all__ = ["partitions"]


def _validated(n):
    """校验入参：必须是 int 且非 bool；n < 0 抛 ValueError。"""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int, got %s" % type(n).__name__)
    if n < 0:
        raise ValueError("n must be non-negative, got %r" % (n,))
    return n


def _pentagonal(k: int) -> int:
    """广义五边形数 g_k = k(3k-1)/2（k 取 1, -1, 2, -2, ...）。"""
    return k * (3 * k - 1) // 2


@lru_cache(maxsize=None)
def _partitions(n: int) -> int:
    """欧拉五边形数定理递推：p(n) = Σ (-1)^(k-1) · p(n - g_k)。"""
    if n == 0:
        return 1
    total = 0
    k = 1
    while True:
        g = _pentagonal(k)
        if g > n:
            break
        # p(n) = Σ_{k≥1} (-1)^(k-1) [p(n-g_k) + p(n-g_{-k})]，即 +,+,-,-... 按 k 奇偶
        sign = 1 if k % 2 == 1 else -1
        total += sign * _partitions(n - g)
        g_neg = _pentagonal(-k)
        if g_neg <= n:
            total += sign * _partitions(n - g_neg)
        k += 1
    return total


def partitions(n: int) -> int:
    """返回正整数 n 的分拆数 p(n)（精确整数）。

    约定 partitions(0) == 1（空分拆）。
    n 须为 int（bool 拒）：非 int 抛 TypeError，n < 0 抛 ValueError。
    """
    n = _validated(n)
    return _partitions(n)
