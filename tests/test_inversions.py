import random

import pytest

from inversions import count_inversions


def _brute(seq):
    """O(n^2) 逐对暴力计数（仅严格大于，等值不计），作为独立参照。"""
    count = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                count += 1
    return count


# ---- 验收要点：逐字示例 ----


def test_empty():
    assert count_inversions([]) == 0


def test_single():
    assert count_inversions([1]) == 0


def test_sorted():
    assert count_inversions([1, 2, 3]) == 0


def test_reversed():
    assert count_inversions([3, 2, 1]) == 3


def test_partial():
    assert count_inversions([3, 1, 2]) == 2


def test_equal_elements_not_counted():
    # 等值不计：[2, 2, 1] 只有 (0, 2)、(1, 2) 两对，不是 3
    assert count_inversions([2, 2, 1]) == 2


def test_five_reversed():
    assert count_inversions([5, 4, 3, 2, 1]) == 10


def test_float_elements():
    assert count_inversions([1.5, 1.0]) == 1


def test_tuple_input():
    assert count_inversions((2, 1)) == 1


# ---- 入参约定：TypeError ----


def test_str_input_raises():
    with pytest.raises(TypeError):
        count_inversions("321")


def test_non_sequence_input_raises():
    with pytest.raises(TypeError):
        count_inversions(321)


def test_non_numeric_element_raises():
    with pytest.raises(TypeError):
        count_inversions([1, "a"])


def test_bool_element_raises():
    with pytest.raises(TypeError):
        count_inversions([1, True])


# ---- 性质：与暴力计数逐例一致 ----


def test_random_small_lists_match_brute_force():
    rng = random.Random(20261126)
    for _ in range(300):
        n = rng.randint(0, 12)
        seq = [rng.randint(0, 6) for _ in range(n)]
        assert count_inversions(seq) == _brute(seq), seq


def test_random_tuple_small_match_brute_force():
    rng = random.Random(58)
    for _ in range(100):
        n = rng.randint(0, 12)
        seq = tuple(rng.randint(0, 6) for _ in range(n))
        assert count_inversions(seq) == _brute(seq), seq


def test_large_list_matches_brute_force():
    rng = random.Random(936)
    for _ in range(3):
        seq = [rng.randint(0, 10**6) for _ in range(200)]
        assert count_inversions(seq) == _brute(seq)


def test_random_float_list_matches_brute_force():
    rng = random.Random(7)
    for _ in range(50):
        n = rng.randint(0, 12)
        seq = [rng.random() for _ in range(n)]
        assert count_inversions(seq) == _brute(seq), seq


def test_does_not_mutate_input():
    seq = [3, 1, 2]
    count_inversions(seq)
    assert seq == [3, 1, 2]
