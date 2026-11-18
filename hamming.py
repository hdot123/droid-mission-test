"""hamming: 字符串汉明距离计算。"""


def distance(a: str, b: str) -> int:
    """返回两个等长字符串在相同位置上字符不同的个数。

    长度不等时抛出 ValueError。
    """
    if len(a) != len(b):
        raise ValueError("strings must be of equal length")
    return sum(ch_a != ch_b for ch_a, ch_b in zip(a, b))
