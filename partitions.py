"""partitions: 整数分拆数 p(n)（数论小组件）。

p(n) 为正整数 n 的分拆数，即把 n 写成若干正整数之和（次序无关）的方案个数。
约定 p(0) == 1（空分拆）。只用标准库，精确整数运算。
"""

__all__ = ["partitions"]


def partitions(n: int) -> int:
    """返回正整数 n 的分拆数 p(n)，精确整数；p(0) == 1。

    n 须为 int（bool 拒）：n < 0 抛 ValueError，非 int 抛 TypeError。
    实现用欧拉五边形数定理递推：
    p(n) = sum_{k!=0} (-1)^(k-1) * p(n - g_k)，其中 g_k = k(3k-1)/2。
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int, got %r" % (type(n).__name__,))
    if n < 0:
        raise ValueError("n must be >= 0, got %r" % (n,))

    p = [1]  # p(0) = 1
    for m in range(1, n + 1):
        total = 0
        k = 1
        while True:
            g1 = k * (3 * k - 1) // 2  # 广义五边形数 g_k = k(3k-1)/2
            if g1 > m:
                break
            total += p[m - g1] if k % 2 == 1 else -p[m - g1]
            g2 = k * (3 * k + 1) // 2  # g_{-k} = k(3k+1)/2
            if g2 <= m:
                total += p[m - g2] if k % 2 == 1 else -p[m - g2]
            k += 1
        p.append(total)
    return p[n]
