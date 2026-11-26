"""radixsort: LSD 基数排序（列表/元组整数入参，支持负数）。

约定：
- ``radix_sort(values)`` 返回升序**新表**（list），不修改入参；
- 入参为 list 或 tuple，元素必须是 int（bool／float 均不算）；
- 支持负数：负数按绝对值做基数排序后再整体取负回插。
"""


def _lsd_radix_nonnegative(nums):
    """对非负整数列表做基数排序（基 256，按字节位分桶），返回新表。"""
    if not nums:
        return []
    result = list(nums)
    exp = 1
    max_val = max(nums)
    while max_val // exp > 0:
        buckets = [[] for _ in range(256)]
        for n in result:
            buckets[(n // exp) % 256].append(n)
        result = [x for bucket in buckets for x in bucket]
        exp *= 256
    return result


def radix_sort(values):
    """LSD 基数排序：返回升序新表；入参 list/tuple、元素 int，支持负数。"""
    if not isinstance(values, (list, tuple)):
        raise TypeError(
            "radix_sort expects a list or tuple, got %s" % type(values).__name__
        )
    for v in values:
        if isinstance(v, bool) or not isinstance(v, int):
            raise TypeError(
                "radix_sort expects int elements, got %s" % type(v).__name__
            )
    negatives = []
    nonnegatives = []
    for v in values:
        if v < 0:
            negatives.append(-v)
        else:
            nonnegatives.append(v)
    sorted_neg_abs = _lsd_radix_nonnegative(negatives)
    sorted_negatives = [-x for x in reversed(sorted_neg_abs)]
    return sorted_negatives + _lsd_radix_nonnegative(nonnegatives)
