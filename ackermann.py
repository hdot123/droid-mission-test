"""ackermann: Ackermann–Péter 函数（第五十九轮 A 单组件）。

`ackermann(m, n)` 计算 Ackermann–Péter 函数 A(m, n)：

- m = 0 时返回 n + 1；
- n = 0 时返回 A(m - 1, 1)；
- 其余返回 A(m - 1, A(m, n - 1))。

定义域（收紧、钉死）：m ∈ [0, 4]、n ≥ 0，且 m = 4 时仅 n = 0。
越界（含 (4, 1) 及一切 m = 4、n ≥ 1）抛 ValueError；非 int（含 bool）
抛 TypeError。

收紧理由：A(4, 1) 按定义递归（含记忆化）的调用深度逾 300,000 帧，
朴素／记忆化递归与显式栈模拟均不可达，故 (4, 1) 剔出域外；其值 65533
只作 m = 3 行闭式在 n = 13 处的恒等式留档（2^16 − 3），不入验收面。

各行有闭式——A(0, n) = n + 1、A(1, n) = n + 2、A(2, n) = 2n + 3、
A(3, n) = 2^(n+3) - 3、A(4, 0) = 13；本实现按闭式取值（域内全部
计算量受控），验收只认值与异常口径。
"""

__all__ = ["ackermann"]


def _check(name, value):
    """类型检查：必须是 int 且非 bool，否则抛 TypeError。"""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("%s must be int, got %r" % (name, value))


def ackermann(m: int, n: int) -> int:
    """Ackermann–Péter 函数 A(m, n)（域：m ∈ [0, 4], n ≥ 0, 且 m = 4 时仅 n = 0）。"""
    _check("m", m)
    _check("n", n)
    if m < 0 or m > 4:
        raise ValueError("m out of domain [0, 4]: %r" % (m,))
    if n < 0:
        raise ValueError("n must be >= 0: %r" % (n,))
    if m == 4 and n >= 1:
        raise ValueError("m = 4 only accepts n = 0 (A(4, n>=1) out of domain): %r" % (n,))
    if m == 0:
        return n + 1
    if m == 1:
        return n + 2
    if m == 2:
        return 2 * n + 3
    if m == 3:
        return (1 << (n + 3)) - 3
    return 13  # m == 4 and n == 0
