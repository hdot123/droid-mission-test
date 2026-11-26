"""stirling2: 第二类 Stirling 数工具（第五十六轮新增组件）。

本模块只依赖标准库，不 import 仓库内任何其他模块。
函数行为以文档字符串与验收规格为准。
"""


def _check_int(value, name):
    """入参校验：非 int（含 bool）抛 TypeError，负数抛 ValueError。"""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("%s must be int, got %r" % (name, value))
    if value < 0:
        raise ValueError("%s must be >= 0, got %r" % (name, value))


def stirling2(n: int, k: int) -> int:
    """第二类 Stirling 数 S(n, k)：n 个元素分成 k 个非空子集的分拆数。

    S(0, 0) = 1；S(n, 0) = 0（n > 0）；k > n 返回 0。
    n < 0 或 k < 0 抛 ValueError；非 int（含 bool）抛 TypeError。
    逐 k 给值的分拆分布，不是行和总数（Bell 数）。
    """
    _check_int(n, "n")
    _check_int(k, "k")
    if k > n:
        return 0
    if k == 0:
        return 1 if n == 0 else 0
    # 递推：S(n, k) = k * S(n-1, k) + S(n-1, k-1)
    row = [1]  # S(i, 0)，i 从 0 开始
    for i in range(1, n + 1):
        # 由上一行从右向左更新，得到第 i 行
        row.append(1)  # S(i, i) = 1
        for j in range(i - 1, 0, -1):
            row[j] = row[j] * j + row[j - 1]
        row[0] = 0  # S(i, 0) = 0（i > 0）
    return row[k]


def stirling2_row(n: int) -> list[int]:
    """返回第 n 行 [S(n, 0), …, S(n, n)]，共 n+1 项。

    行和在数学上等于 Bell 数，但本函数逐项给出每个 S(n, k)。
    n < 0 抛 ValueError；非 int（含 bool）抛 TypeError。
    """
    _check_int(n, "n")
    row = [1]
    for i in range(1, n + 1):
        row.append(1)
        for j in range(i - 1, 0, -1):
            row[j] = row[j] * j + row[j - 1]
        row[0] = 0
    return row
