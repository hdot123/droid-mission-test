"""fenwick: Fenwick 树（树状数组）前缀和数据结构。

0-based 对外下标；内部同时保存数组拷贝与 1-based BIT。
所有入参按验收口径做类型与边界校验：
- 容器非 list、元素/delta 非数值（int/float，bool 不算）、index 非 int（bool 不算）：TypeError
- 下标越界（add / prefix_sum / range_sum 任一端点）：IndexError
- range_sum 的 lo > hi：ValueError
"""

__all__ = ["FenwickTree"]


def _is_number(value):
    """数值判定：int/float 且非 bool。"""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check_index(index, name="index"):
    """index 必须是 int（bool 不算），否则 TypeError。"""
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError("%s must be int, got %r" % (name, index))


class FenwickTree:
    """树状数组：支持点加、前缀和、闭区间和、全和与还原。"""

    def __init__(self, values):
        if not isinstance(values, list):
            raise TypeError("values must be list, got %r" % (type(values).__name__,))
        for i, v in enumerate(values):
            if not _is_number(v):
                raise TypeError("values[%d] must be numeric, got %r" % (i, v))
        # 内部拷贝：外部后续修改原列表不影响树。
        self._data = list(values)
        n = len(self._data)
        # 1-based BIT，长度 n+1，下标 0 不用。
        self._bit = [0] * (n + 1)
        for i, v in enumerate(self._data):
            self._bit[i + 1] += v
        for i in range(1, n + 1):
            j = i + (i & -i)
            if j <= n:
                self._bit[j] += self._bit[i]

    def _check_bounds(self, index, name="index"):
        """先类型后边界：index 必须为 int 且在 [0, n-1]。"""
        _check_index(index, name)
        if index < 0 or index >= len(self._data):
            raise IndexError("%s %d out of range for size %d"
                             % (name, index, len(self._data)))

    def _check_delta(self, delta):
        """delta 必须是数值（bool 不算）。"""
        if not _is_number(delta):
            raise TypeError("delta must be numeric, got %r" % (delta,))

    def add(self, index, delta):
        """下标 index 处加 delta（0-based）。"""
        self._check_bounds(index, "index")
        self._check_delta(delta)
        self._data[index] += delta
        i = index + 1
        n = len(self._bit) - 1
        while i <= n:
            self._bit[i] += delta
            i += i & -i

    def _bit_prefix(self, end):
        """1-based BIT 上前 end 个元素之和（end ∈ [0, n]）。"""
        total = 0
        i = end
        while i > 0:
            total += self._bit[i]
            i -= i & -i
        return total

    def prefix_sum(self, index):
        """下标 [0..index] 之和（0-based，含端点）。"""
        self._check_bounds(index, "index")
        return self._bit_prefix(index + 1)

    def range_sum(self, lo, hi):
        """闭区间 [lo, hi] 之和（0-based）。"""
        self._check_bounds(lo, "lo")
        self._check_bounds(hi, "hi")
        if lo > hi:
            raise ValueError("lo > hi: %d > %d" % (lo, hi))
        return self._bit_prefix(hi + 1) - self._bit_prefix(lo)

    def total(self):
        """全和；空树返回 0。"""
        return self._bit_prefix(len(self._data))

    def to_list(self):
        """还原当前数组（返回新列表）。"""
        return list(self._data)

    def __len__(self):
        return len(self._data)
