"""zarray: Z 数组（Z-array）计算。

给定字符串 s，Z 数组满足：Z[0] = 0，Z[i]（i >= 1）为 s 与其后缀 s[i:]
的最长公共前缀长度。与 KMP 前缀函数 π（边框长）不同，Z[i] 比较的是
原串整体前缀与后缀，输出亦不同。空串返回 []。
入参约定：非 str 抛 TypeError（本模块无 ValueError 面）。
"""

__all__ = ["z_array"]


def z_array(s):
    """返回字符串 s 的 Z 数组；非 str 入参抛 TypeError，空串返回 []。"""
    if not isinstance(s, str):
        raise TypeError("z_array() expected str, got %r" % type(s).__name__)
    n = len(s)
    if n == 0:
        return []
    z = [0] * n
    # 线性 Z-box 算法
    l = 0
    r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l = i
            r = i + z[i]
    return z
