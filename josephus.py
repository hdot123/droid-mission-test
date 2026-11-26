"""josephus: 约瑟夫环幸存者。

n 人围成一圈，编号 0 起。自当前位起数 k 人、淘汰第 k 人，
反复进行直到只剩一人，返回幸存者编号。
"""


def josephus(n: int, k: int) -> int:
    """n 人成环、每数到第 k 人淘汰，返回幸存者编号（0 起）。

    n < 1 或 k < 1 抛 ValueError；非 int（含 bool）抛 TypeError。
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int, got %r" % (n,))
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be int, got %r" % (k,))
    if n < 1:
        raise ValueError("n must be >= 1, got %r" % (n,))
    if k < 1:
        raise ValueError("k must be >= 1, got %r" % (k,))
    survivor = 0
    for people in range(2, n + 1):
        survivor = (survivor + k) % people
    return survivor
