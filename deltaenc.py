"""deltaenc: 整数序列差分编码/解码工具（第四十五轮 · 并发 C 单）。

`delta_encode` 把首元原样保留、其后每元存与前一元之差；
`delta_decode` 通过累加还原原序列，两者互为逆运算。
"""


def _check(nums):
    """校验入参：必须是 list，且每个元素都是 int（拒 bool），否则抛 TypeError。"""
    if not isinstance(nums, list):
        raise TypeError("expected a list, got %r" % type(nums).__name__)
    for item in nums:
        if isinstance(item, bool) or not isinstance(item, int):
            raise TypeError("expected int elements, got %r" % type(item).__name__)


def delta_encode(nums):
    """把整数序列差分编码：首元原样，其后每元为与前一元之差；空表返回空表。"""
    _check(nums)
    if not nums:
        return []
    result = [nums[0]]
    for prev, cur in zip(nums, nums[1:]):
        result.append(cur - prev)
    return result


def delta_decode(deltas):
    """把差分序列累加还原为原整数序列；空表返回空表。"""
    _check(deltas)
    result = []
    total = 0
    for item in deltas:
        total += item
        result.append(total)
    return result
