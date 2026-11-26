"""inversions: 序列逆序对计数（第五十八轮 C 单 · 独立小组件）。

`count_inversions(seq)` 返回序列中满足 i < j 且 a[i] > a[j] 的下标对个数。
**等值不计**——只有严格大于才计数。入参必须是列表或元组，元素必须是
int／float（bool 不算数值）；违反约定抛 TypeError。
"""


def count_inversions(seq):
    """返回序列 seq 的逆序对个数（等值不计）。

    入参为列表或元组，元素为 int／float；str、非序列形态、非数值元素
    （含 bool）一律抛 TypeError。
    """
    if isinstance(seq, (str, bytes)) or not isinstance(seq, (list, tuple)):
        raise TypeError("expected list or tuple, got %r" % (type(seq).__name__,))
    values = list(seq)
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                "expected int/float elements, got %r" % (type(value).__name__,)
            )
    return _count(values)


def _count(values):
    """归并排序计数逆序对（严格大于才计，等值不计）。"""
    n = len(values)
    if n < 2:
        return 0
    mid = n // 2
    left = values[:mid]
    right = values[mid:]
    inversions = _count(left) + _count(right)
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        # left[i] <= right[j] 时不产生逆序（等值不计）
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    values[:] = merged
    return inversions
