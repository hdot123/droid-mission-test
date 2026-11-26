"""farey: Farey 数列枚举（n 阶，约分元组升序）。

返回 0/1 与 1/1 之间（含两端）、分母不超过 n 的全部约分分数，
按数值升序排列为 (分子, 分母) 元组。仅用标准库，不依赖其他模块。
"""


def farey(n: int) -> list[tuple[int, int]]:
    """返回 n 阶 Farey 数列：[(0, 1), ..., (1, 1)]，约分元组按值升序。

    入参约定：
    - n < 1 抛 ValueError；
    - 非 int（含 bool）抛 TypeError。
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int, got %r" % (type(n).__name__,))
    if n < 1:
        raise ValueError("n must be >= 1, got %r" % (n,))

    # 经典 Farey 递推（Stern–Brocot 中序遍历的相邻分数生成）：
    # 由相邻项 (a/b, c/d) 求下一个满足 b*c - a*d == 1 的项。
    a, b = 0, 1
    c, d = 1, n
    result: list[tuple[int, int]] = [(a, b)]
    while (a, b) != (1, 1):
        k = (n + b) // d
        a, c = c, k * c - a
        b, d = d, k * d - b
        result.append((a, b))
    return result
