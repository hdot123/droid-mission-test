"""Longest common subsequence (LCS) helpers for two strings.

Only the Python standard library is used, and this module does not
import any sibling module.
"""


def lcs_length(a, b):
    """Return the length of the longest common subsequence of ``a`` and ``b``."""
    n, m = len(a), len(b)
    # dp[i][j] = LCS length of a[:i] and b[:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        ai = a[i - 1]
        row = dp[i]
        prev = dp[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                row[j] = prev[j - 1] + 1
            else:
                up = prev[j]
                left = row[j - 1]
                row[j] = up if up >= left else left
    return dp[n][m]


def lcs_string(a, b):
    """Return one longest common subsequence of ``a`` and ``b``.

    The length table is built bottom-up, then the ends of both strings are
    backtracked: equal characters are taken; otherwise the walk moves toward
    the side with the larger length, and on a tie it skips ``a``'s current
    character (so ``b``'s characters are preferred).
    """
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        ai = a[i - 1]
        row = dp[i]
        prev = dp[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                row[j] = prev[j - 1] + 1
            else:
                up = prev[j]
                left = row[j - 1]
                row[j] = up if up >= left else left

    out = []
    i, j = n, m
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            # Tie goes here: skip a's current character.
            i -= 1
        else:
            j -= 1
    out.reverse()
    return "".join(out)
