"""eulerian: Eulerian 数（按下降位计排列数）。

提供 ``eulerian(n, m)`` 返回 n 元排列中恰有 m 个下降位（相邻逆序位置）的
个数 A(n, m)，以及 ``eulerian_row(n)`` 返回整行 [A(n, 0), …, A(n, n−1)]。

m 计数的是下降位个数（取值 0..n−1），不是上升数或逆序对总数；同一行各项
之和为 n!。实现使用递推 A(n, m) = (n−m)·A(n−1, m−1) + (m+1)·A(n−1, m)。
"""

def _check_n(n):
    """校验 n 为 ≥1 的 int（bool 视为非 int）；否则抛对应异常。"""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int, got %r" % (type(n).__name__,))
    if n < 1:
        raise ValueError("n must be >= 1, got %r" % (n,))


def _check_m(n, m):
    """校验 m 为 int 且落在 [0, n−1]；否则抛对应异常。"""
    if isinstance(m, bool) or not isinstance(m, int):
        raise TypeError("m must be int, got %r" % (type(m).__name__,))
    if m < 0 or m > n - 1:
        raise ValueError("m out of range [0, %d]: %r" % (n - 1, m))


def eulerian(n, m):
    """返回 Eulerian 数 A(n, m)：n 元排列中恰有 m 个下降位的个数。

    n < 1 或 m 越界（< 0 或 > n−1）抛 ValueError；非 int（含 bool）抛 TypeError。
    """
    _check_n(n)
    _check_m(n, m)
    # 递推构建前 n 行（行 1..n），只保留上一行以省内存。
    row = [1]  # A(1, 0)
    for size in range(2, n + 1):
        prev = row
        cur = [0] * size
        for k in range(size):
            left = (size - k) * prev[k - 1] if k >= 1 else 0
            right = (k + 1) * prev[k] if k < len(prev) else 0
            cur[k] = left + right
        row = cur
    return row[m]


def eulerian_row(n):
    """返回整行 [A(n, 0), …, A(n, n−1)]。

    n < 1 抛 ValueError；非 int（含 bool）抛 TypeError。
    """
    _check_n(n)
    row = [1]  # A(1, 0)
    for size in range(2, n + 1):
        prev = row
        cur = [0] * size
        for k in range(size):
            left = (size - k) * prev[k - 1] if k >= 1 else 0
            right = (k + 1) * prev[k] if k < len(prev) else 0
            cur[k] = left + right
        row = cur
    return row
