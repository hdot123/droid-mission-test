"""tests/test_fenwick.py: FenwickTree 验收测试（逐条对应工单验收要点）。"""

import random

import pytest

from fenwick import FenwickTree


# ---------------------------------------------------------------------------
# 验收示例
# ---------------------------------------------------------------------------

def test_basic_example_prefix_sum():
    assert FenwickTree([3, 1, 4, 1, 5]).prefix_sum(2) == 8


def test_basic_example_range_and_total():
    tree = FenwickTree([3, 1, 4, 1, 5])
    assert tree.range_sum(1, 3) == 6
    assert tree.total() == 14


def test_empty_tree():
    assert FenwickTree([]).total() == 0
    assert len(FenwickTree([])) == 0


# ---------------------------------------------------------------------------
# 性质测试：与朴素列表模型 / 独立 0-based BIT 逐 op 一致
# ---------------------------------------------------------------------------

def _naive_prefix(arr, index):
    return sum(arr[: index + 1])


def _zero_based_bit_prefix(arr, index):
    """独立 0-based BIT 实现（build 时 i |= i + 1，查询时 i -= i & -i 风格的另一路）。"""
    n = len(arr)
    bit = [0] * n

    def internal_add(i, delta):
        while i < n:
            bit[i] += delta
            i |= i + 1

    def build(src):
        for i, v in enumerate(src):
            internal_add(i, v)

    def query(i):
        # 查询 [0..i]：从 i 往下走 i & (i+1) 位。
        total = 0
        while i >= 0:
            total += bit[i]
            i &= i + 1
            i -= 1
        return total

    build(arr)
    return query(index)


def test_property_agrees_with_naive_and_independent_bit():
    rng = random.Random(5906)
    for _ in range(60):
        n = rng.randint(0, 20)
        values = [rng.randint(-50, 50) if rng.random() < 0.5
                  else round(rng.uniform(-10, 10), 3) for _ in range(n)]
        tree = FenwickTree(list(values))
        naive = list(values)
        bit_values = list(values)

        if n:
            for _ in range(50):
                op = rng.random()
                if op < 0.45:
                    idx = rng.randrange(n)
                    delta = rng.randint(-20, 20)
                    tree.add(idx, delta)
                    naive[idx] += delta
                    bit_values[idx] += delta
                else:
                    idx = rng.randrange(n)
                    got = tree.prefix_sum(idx)
                    assert got == pytest.approx(_naive_prefix(naive, idx), rel=1e-9, abs=1e-9)
                    assert got == pytest.approx(
                        _zero_based_bit_prefix(bit_values, idx), rel=1e-9, abs=1e-9)
            lo = rng.randint(0, n - 1)
            hi = rng.randint(lo, n - 1)
            assert tree.range_sum(lo, hi) == pytest.approx(
                sum(naive[lo: hi + 1]), rel=1e-9, abs=1e-9)
            assert tree.range_sum(0, n - 1) == pytest.approx(sum(naive), rel=1e-9, abs=1e-9)
        assert tree.total() == pytest.approx(sum(naive), rel=1e-9, abs=1e-9)
        assert tree.to_list() == naive
        assert len(tree) == n


def test_prefix_sum_matches_independent_zero_based_bit_fixed():
    # 钉死一个非随机对照点，覆盖独立 0-based BIT 实现一致性。
    values = [3, 1, 4, 1, 5, 9, 2, 6]
    tree = FenwickTree(list(values))
    for i in range(len(values)):
        assert tree.prefix_sum(i) == pytest.approx(
            _zero_based_bit_prefix(values, i), rel=1e-9, abs=1e-9)


# ---------------------------------------------------------------------------
# 内部拷贝：构造后修改原列表不影响树
# ---------------------------------------------------------------------------

def test_construction_copies_input_list():
    original = [1, 2, 3]
    tree = FenwickTree(original)
    original.append(100)
    original[0] = -999
    assert tree.to_list() == [1, 2, 3]
    assert tree.total() == 6
    assert len(tree) == 3


# ---------------------------------------------------------------------------
# TypeError 口径
# ---------------------------------------------------------------------------

def test_constructor_non_list_raises_type_error():
    with pytest.raises(TypeError):
        FenwickTree("123")


def test_constructor_non_numeric_element_raises_type_error():
    with pytest.raises(TypeError):
        FenwickTree([1, "a"])


def test_constructor_bool_element_raises_type_error():
    with pytest.raises(TypeError):
        FenwickTree([True])


def test_add_non_numeric_delta_raises_type_error():
    with pytest.raises(TypeError):
        FenwickTree([1]).add(0, "x")


def test_index_type_errors():
    tree = FenwickTree([1, 2, 3])
    with pytest.raises(TypeError):
        tree.add(True, 1)
    with pytest.raises(TypeError):
        tree.prefix_sum(False)
    with pytest.raises(TypeError):
        tree.range_sum(0, 1.0)


# ---------------------------------------------------------------------------
# IndexError / ValueError 口径
# ---------------------------------------------------------------------------

def test_add_index_out_of_bounds_raises_index_error():
    with pytest.raises(IndexError):
        FenwickTree([1]).add(1, 5)


def test_prefix_sum_negative_index_raises_index_error():
    with pytest.raises(IndexError):
        FenwickTree([1]).prefix_sum(-1)


def test_range_sum_bounds_raise_index_error():
    tree = FenwickTree([1, 2, 3])
    with pytest.raises(IndexError):
        tree.range_sum(-1, 1)
    with pytest.raises(IndexError):
        tree.range_sum(0, 3)


def test_range_sum_lo_gt_hi_raises_value_error():
    with pytest.raises(ValueError):
        FenwickTree([1, 2]).range_sum(1, 0)


# ---------------------------------------------------------------------------
# 杂项行为面：add 后各查询仍正确、空树操作
# ---------------------------------------------------------------------------

def test_add_then_queries():
    tree = FenwickTree([0, 0, 0, 0])
    tree.add(0, 2)
    tree.add(3, 5)
    tree.add(1, -1)
    assert tree.to_list() == [2, -1, 0, 5]
    assert tree.prefix_sum(1) == 1
    assert tree.range_sum(1, 3) == 4
    assert tree.total() == 6


def test_empty_tree_queries():
    tree = FenwickTree([])
    assert tree.total() == 0
    assert tree.to_list() == []
    with pytest.raises(IndexError):
        tree.prefix_sum(0)
    with pytest.raises(IndexError):
        tree.add(0, 1)


def test_float_values_supported():
    tree = FenwickTree([1.5, 2.5, 3.0])
    assert tree.prefix_sum(2) == pytest.approx(7.0)
    tree.add(2, 0.5)
    assert tree.total() == pytest.approx(7.5)
