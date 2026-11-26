"""jaro: 原版 Jaro 字符串相似度（不含 Winkler 前缀加权）。

本族是相似度族里的**原版 Jaro**：只做匹配窗内的贪心配对与半换位惩罚，
**不加任何 Winkler 前缀奖励项**。市面流传的 DWAYNE/DUANE = 0.84、
DIXON/DICKSONX = 0.8133 是 Jaro–Winkler 值，本模块不产出那些数字。
"""

__all__ = ["jaro_similarity"]


def jaro_similarity(s1: str, s2: str) -> float:
    """返回原版 Jaro 相似度，取值恒在 [0, 1]。

    匹配窗 = max(len(s1), len(s2)) // 2 - 1（下限 0）；两空串返回 1.0、
    一空返回 0.0、全同返回 1.0；非 str 入参抛 TypeError。
    公式：(m/len1 + m/len2 + (m - t) / m) / 3，其中 t 为半换位数
    （匹配子序列逐位不一致对数的一半）。
    """
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError(
            "jaro_similarity() expects str arguments, got %s and %s"
            % (type(s1).__name__, type(s2).__name__)
        )
    if s1 == s2:
        return 1.0
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0

    window = max(len1, len2) // 2 - 1
    if window < 0:
        window = 0

    flags1 = [False] * len1
    flags2 = [False] * len2
    matches = 0
    for i in range(len1):
        start = max(0, i - window)
        end = min(len2, i + window + 1)
        for j in range(start, end):
            if not flags2[j] and s1[i] == s2[j]:
                flags1[i] = True
                flags2[j] = True
                matches += 1
                break

    if matches == 0:
        return 0.0

    # 半换位数：把两侧匹配子序列按位对齐，数不一致的位置，再折半。
    k = 0
    mismatches = 0
    for i in range(len1):
        if flags1[i]:
            while not flags2[k]:
                k += 1
            if s1[i] != s2[k]:
                mismatches += 1
            k += 1
    transpositions = mismatches / 2.0

    return (
        matches / len1 + matches / len2 + (matches - transpositions) / matches
    ) / 3.0
