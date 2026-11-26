"""kmpsearch: KMP 子串搜索（全部出现位置，含重叠）。

`find_all(text, pattern)` 返回 pattern 在 text 中全部出现的起始下标，
升序、**含重叠出现**。算法为经典 KMP（前缀函数 / LPS 表），不使用正则。

入参约定：
- pattern 为空 -> ValueError；
- text 或 pattern 非 str -> TypeError。
"""

from __future__ import annotations


def _lps(pattern: str) -> list[int]:
    """构造 pattern 的最长公共前后缀表（prefix function / LPS）。"""
    n = len(pattern)
    lps = [0] * n
    length = 0
    i = 1
    while i < n:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            # 回退到上一个可能的前缀长度，不推进 i
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def find_all(text: str, pattern: str) -> list[int]:
    """返回 pattern 在 text 中全部出现的起始下标（含重叠），升序。

    KMP 扫描；命中后用 lps[k-1] 回退以捕获重叠出现。
    空 pattern 抛 ValueError；任一非 str 入参抛 TypeError。
    """
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError(
            "find_all() requires str arguments, got text=%r pattern=%r"
            % (type(text).__name__, type(pattern).__name__)
        )
    if pattern == "":
        raise ValueError("pattern must be a non-empty string")

    n, m = len(text), len(pattern)
    if m > n:
        return []

    lps = _lps(pattern)
    result: list[int] = []
    j = 0  # pattern 中已匹配的字符数
    i = 0  # text 游标
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                # 命中；用 lps[j-1] 回退以捕获重叠出现
                result.append(i - j)
                j = lps[j - 1]
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
    return result
