"""collatz: Collatz (3n+1) 序列的步数与峰值工具。"""


def steps(n: int) -> int:
    """正整数 n 按 Collatz 规则（偶数除 2、奇数 3n+1）到达 1 的步数。

    steps(1) == 0；n 小于 1 抛 ValueError。
    """
    if n < 1:
        raise ValueError("n must be >= 1: %r" % (n,))
    count = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        count += 1
    return count


def peak(n: int) -> int:
    """Collatz 序列（含起点与终点 1）中的最大值。

    n 小于 1 抛 ValueError。
    """
    if n < 1:
        raise ValueError("n must be >= 1: %r" % (n,))
    best = n
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        if n > best:
            best = n
    return best
