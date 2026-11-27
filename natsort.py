"""natsort: 字符串自然序排序（第五十九轮 D 单）。

比较口径（钉死）：字符串切成数字段与非数字段交替的段列、逐段比较——
数字段按数值比较、数值同则位数少者先（前导零少者先）；数字段与非数字段
相遇时数字段先；非数字段按码点序；一方段列为另一方前缀时短者先。

返回新表，不改入参；容器非 list 或元素非 str 抛 TypeError（无 ValueError 面）。
"""

import re

_SEGMENT_RE = re.compile(r"\d+|\D+")


def _segments(text: str) -> list:
    """把字符串切成数字段/非数字段交替的段列。"""
    return _SEGMENT_RE.findall(text)


def _sort_key(text: str):
    """键函数：每段编码为可直接比较的元组。

    数字段 -> (0, 数值, 位数, "")：数值先比，同值比位数（少者先）；
    非数字段 -> (1, 0, 0, 段文本)：按码点序。
    类型标签在首位，保证数字段恒排在非数字段之前。
    """
    key = []
    for seg in _segments(text):
        if seg[0].isdigit():
            key.append((0, int(seg), len(seg), ""))
        else:
            key.append((1, 0, 0, seg))
    return key


def _compare(a: str, b: str) -> int:
    """显式比较器，与 _sort_key 完全同口径（随机验收逐个一致）。"""
    segs_a = _segments(a)
    segs_b = _segments(b)
    for seg_x, seg_y in zip(segs_a, segs_b):
        num_x = seg_x[0].isdigit()
        num_y = seg_y[0].isdigit()
        if num_x and num_y:
            val_x, val_y = int(seg_x), int(seg_y)
            if val_x != val_y:
                return -1 if val_x < val_y else 1
            if len(seg_x) != len(seg_y):
                return -1 if len(seg_x) < len(seg_y) else 1
        elif num_x:
            return -1  # 数字段遇非数字段：数字段先
        elif num_y:
            return 1
        else:
            if seg_x != seg_y:
                return -1 if seg_x < seg_y else 1
    # 一方段列是另一方前缀：短者先
    if len(segs_a) != len(segs_b):
        return -1 if len(segs_a) < len(segs_b) else 1
    # 段列完全相同但原串不同只可能是空串情形；保守归为相等
    if a == b:
        return 0
    return -1 if a < b else 1


def natural_sort(items: list) -> list:
    """返回 items 的自然序新表（不改入参）。

    容器非 list 或元素非 str 抛 TypeError。
    """
    if not isinstance(items, list):
        raise TypeError("natural_sort expects a list, got %r" % (type(items).__name__,))
    for item in items:
        if not isinstance(item, str):
            raise TypeError("natural_sort expects str items, got %r" % (type(item).__name__,))
    return sorted(items, key=_sort_key)
