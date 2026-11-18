"""rangemerge: 整数闭区间合并工具。

merge 按起点升序返回合并后的区间列表，重叠或相邻（下一区间的 start
不大于当前 end 加 1）的区间合并为一段；total 返回合并后各区间长度
（闭区间长度为 end - start + 1）之和。任一区间 start 大于 end 时，
两个函数均抛 ValueError。
"""


def _validate(ranges):
    for start, end in ranges:
        if start > end:
            raise ValueError("invalid range: (%r, %r)" % (start, end))


def merge(ranges):
    """合并闭区间列表，返回按起点升序的合并结果；start > end 抛 ValueError。"""
    _validate(ranges)
    ordered = sorted(ranges, key=lambda r: (r[0], r[1]))
    merged = []
    for start, end in ordered:
        if merged and start <= merged[-1][1] + 1:
            if end > merged[-1][1]:
                merged[-1] = (merged[-1][0], end)
        else:
            merged.append((start, end))
    return merged


def total(ranges):
    """合并后各闭区间长度之和；入参校验同 merge。"""
    return sum(end - start + 1 for start, end in merge(ranges))
