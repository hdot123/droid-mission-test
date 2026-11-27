"""快乐数（happy numbers）判定与枚举（标准库，零依赖）。

迭代映射：n -> 各位数字平方和。快乐数迭代到达 1；
不快乐数永不到达 1，最终落入 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4
的环，因此必须做环检测（见证集或 Floyd 判环），不能用固定步数猜测。

与 collatz（3n+1 迭代步数）同属迭代数论族，但迭代映射与问题均不同。
"""

__all__ = ["is_happy", "happy_numbers"]


def _check_int(n, name: str) -> int:
    """入参契约：非 int（含 bool）抛 TypeError；n < 1 抛 ValueError。"""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be an int, got {type(n).__name__}")
    if n < 1:
        raise ValueError(f"{name} must be >= 1, got {n}")
    return n


def _digit_square_sum(n: int) -> int:
    total = 0
    while n:
        d = n % 10
        total += d * d
        n //= 10
    return total


def _is_happy_visited(n: int) -> bool:
    """见证集环检测。"""
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = _digit_square_sum(n)
    return n == 1


def _is_happy_floyd(n: int) -> bool:
    """Floyd 判环（龟兔），与见证集结果必须逐个一致。"""
    slow = n
    fast = _digit_square_sum(n)
    while slow != fast:
        slow = _digit_square_sum(slow)
        fast = _digit_square_sum(_digit_square_sum(fast))
    return slow == 1


def is_happy(n: int) -> bool:
    """判定 n 的各位平方和迭代是否到达 1（快乐数为 True）。"""
    _check_int(n, "n")
    return _is_happy_visited(n)


def happy_numbers(limit: int) -> list:
    """返回 [1, limit] 内全部快乐数的升序列表。"""
    _check_int(limit, "limit")
    return [x for x in range(1, limit + 1) if _is_happy_visited(x)]
