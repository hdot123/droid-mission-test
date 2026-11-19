"""mobius: Möbius 函数（数论，标准库实现）。

`mobius(n)` 返回经典 Möbius 函数值：
- n 含平方质因子时返回 0；
- 否则设 n 的互异质因子个数为 k，返回 (-1)^k；
- 约定 mobius(1) == 1。
n 须为正 int（bool 拒）：非 int 抛 TypeError，n < 1 抛 ValueError。
"""


def mobius(n: int) -> int:
    """返回 Möbius 函数值 mobius(n)。

    参数:
        n: 正整数（bool 不视为 int）。

    返回:
        n 含平方质因子时为 0，否则为 (-1)^k，k 为互异质因子个数；mobius(1) == 1。

    异常:
        TypeError: n 不是 int（bool 亦拒）。
        ValueError: n < 1。
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int, got %r" % (type(n).__name__,))
    if n < 1:
        raise ValueError("n must be positive, got %r" % (n,))

    k = 0  # 互异质因子个数
    m = n
    d = 2
    while d * d <= m:
        if m % d == 0:
            k += 1
            m //= d
            if m % d == 0:  # 仍可整除 => d^2 整除 n
                return 0
        d += 1 if d == 2 else 2  # 2 之后只试奇数
    if m > 1:  # 剩余的质因子
        k += 1
    return -1 if k % 2 else 1
