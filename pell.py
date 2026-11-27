"""pell: Pell 方程 x² − D·y² = 1 的最小正整数解。

规格自成一体：给定非完全平方数 D ≥ 2，返回使 x² − D·y² = 1 成立的
最小正整数解 (x, y)（y ≥ 1）。入参不合约定抛 ValueError／TypeError。
只用标准库。
"""

import math

__all__ = ["pell_minimal"]


def _is_int(value) -> bool:
    """仅接受真正的 int（bool 不算）。"""
    return isinstance(value, int) and not isinstance(value, bool)


def _is_perfect_square(n: int) -> bool:
    """判断 n 是否为完全平方数（整数平方根回代校验，任意大整数精确）。"""
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def pell_minimal(D: int) -> tuple[int, int]:
    """返回 x² − D·y² = 1 的最小正整数解 (x, y)，y ≥ 1。

    D < 2 或 D 为完全平方数抛 ValueError；非 int（含 bool）抛 TypeError。
    用 sqrt(D) 连分数展开的收敛列：最小解由周期（或半周期）处的
    收敛分子分母给出，避免逐 y 暴力搜索在大 D 上不可行。
    """
    if not _is_int(D):
        raise TypeError("D must be int, got %r" % (D,))
    if D < 2:
        raise ValueError("D must be >= 2, got %r" % (D,))
    if _is_perfect_square(D):
        raise ValueError("D must not be a perfect square, got %r" % (D,))

    # sqrt(D) 的连分数：a0 = isqrt(D)，其后周期展开
    # m_0 = 0, d_0 = 1, a_0 = isqrt(D)；递推
    #   m_{k+1} = d_k * a_k - m_k
    #   d_{k+1} = (D - m_{k+1}^2) // d_k
    #   a_{k+1} = (a0 + m_{k+1}) // d_{k+1}
    # 收敛 p_k / q_k：p_k = a_k*p_{k-1} + p_{k-2}, q_k 同理。
    # D 非平方时周期长度为 L；L 奇数取 2L 项、L 偶数取 L 项处的收敛，
    # 即 (p, q) 为 x² − D·y² = 1 的最小解。
    a0 = math.isqrt(D)

    m, d, a = 0, 1, a0
    p_prev2, p_prev1 = 0, 1   # p_{k-2}, p_{k-1}
    q_prev2, q_prev1 = 1, 0   # q_{k-2}, q_{k-1}
    convergents = []          # (p, q) 列表，下标 k 从 0 起
    period = 0
    while True:
        p = a * p_prev1 + p_prev2
        q = a * q_prev1 + q_prev2
        convergents.append((p, q))
        if p * p - D * q * q == 1:
            return (p, q)
        period += 1
        m = d * a - m
        d = (D - m * m) // d
        a = (a0 + m) // d
        p_prev2, p_prev1 = p_prev1, p
        q_prev2, q_prev1 = q_prev1, q
        # 理论上收敛处必命中，循环体内校验即返回；防御性上限
        if period > 10**6:  # pragma: no cover - 防御分支
            raise RuntimeError("period too long for D=%d" % (D,))
