"""motzkin: Motzkin 数计算工具（第五十七轮新增小组件）。

Motzkin 数 M_n 是长度 n 的 Motzkin 路径数：每步为 U（上）、D（下）或
F（平），路径高度永不为负且终点回到高度 0。M_0 = 1。

本模块只用标准库，不依赖仓库内其它模块。
"""

__all__ = ["motzkin"]


def motzkin(n: int) -> int:
    """返回 Motzkin 数 M_n（长度 n 的 Motzkin 路径数）。

    按标准三项递推 M_n = ((2n+1)*M_{n-1} + (3n-3)*M_{n-2}) / (n+2)
    逐项对锚列直接计算，不借用 Catalan 求和等校验恒等式。
    M_0 = 1、M_1 = 1。

    入参约定：n < 0 抛 ValueError；非 int（含 bool）抛 TypeError。
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int, got %r" % (type(n).__name__,))
    if n < 0:
        raise ValueError("n must be non-negative, got %d" % (n,))
    if n <= 1:
        return 1
    m_prev, m_curr = 1, 1  # k = 1: M_0, M_1
    for k in range(2, n + 1):
        next_val = ((2 * k + 1) * m_curr + (3 * k - 3) * m_prev) // (k + 2)
        m_prev, m_curr = m_curr, next_val
    return m_curr
