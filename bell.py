"""bell: Bell 数计算组件。

bell_number(n) 返回第 n 个 Bell 数 B_n（n 元集合的划分数），约定 B_0 = 1。
仅用标准库，精确整数算法（Bell 三角）。
"""


def bell_number(n: int) -> int:
    """返回第 n 个 Bell 数 B_n。

    n 必须是 int（bool 拒绝）；非 int 抛 TypeError；n < 0 抛 ValueError。
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int, got %r" % (type(n).__name__,))
    if n < 0:
        raise ValueError("n must be >= 0, got %r" % (n,))

    # Bell 三角：row[0] 为上一行末元素，row[k] = row[k-1] + 上一行 row[k-1]。
    row = [1]
    for _ in range(n):
        next_row = [row[-1]]
        for k in range(1, len(row) + 1):
            next_row.append(next_row[-1] + row[k - 1])
        row = next_row
    return row[0]
