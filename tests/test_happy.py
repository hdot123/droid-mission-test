"""tests/test_happy.py —— happy.py 快乐数验收要点逐条覆盖。"""

import pytest

import happy
from happy import happy_numbers, is_happy


# ---------------------------------------------------------------------------
# 基本判定
# ---------------------------------------------------------------------------

def test_is_happy_19_true():
    assert is_happy(19) is True


def test_is_happy_4_false():
    assert is_happy(4) is False


def test_is_happy_2_false():
    assert is_happy(2) is False


def test_is_happy_1_true_boundary():
    assert is_happy(1) is True


# ---------------------------------------------------------------------------
# 枚举
# ---------------------------------------------------------------------------

def test_happy_numbers_100_listed_one_by_one():
    assert happy_numbers(100) == [
        1, 7, 10, 13, 19, 23, 28, 31, 32, 44,
        49, 68, 70, 79, 82, 86, 91, 94, 97, 100,
    ]


def test_happy_numbers_100_count_is_20():
    assert len(happy_numbers(100)) == 20


def test_happy_numbers_1000_count_is_143():
    assert len(happy_numbers(1000)) == 143


def test_happy_numbers_ascending_and_in_range():
    result = happy_numbers(500)
    assert result == sorted(result)
    assert all(1 <= x <= 500 for x in result)


# ---------------------------------------------------------------------------
# 性质：[1, 2000] 见证集与 Floyd 判环逐个一致；happy_numbers 与共享记忆分类一致
# ---------------------------------------------------------------------------

def test_visited_vs_floyd_agree_over_full_range_1_2000():
    for n in range(1, 2001):
        visited = happy._is_happy_visited(n)
        floyd = happy._is_happy_floyd(n)
        assert visited == floyd, f"disagreement at n={n}: visited={visited} floyd={floyd}"


def test_happy_numbers_agrees_with_shared_memory_classification():
    shared = {}
    for n in range(1, 2001):
        # 共享记忆：每个数的快乐性按其后继缓存推导（有环则当前链回溯到已知值）
        seen_path = []
        cur = n
        while cur not in shared and cur not in seen_path:
            seen_path.append(cur)
            cur = sum(int(d) ** 2 for d in str(cur))
        if cur in shared:
            verdict = shared[cur]
        else:
            verdict = cur == 1
        for node in seen_path:
            shared[node] = verdict
    expected = [n for n in range(1, 2001) if shared[n]]
    assert happy_numbers(2000) == expected


# ---------------------------------------------------------------------------
# 入参契约：ValueError
# ---------------------------------------------------------------------------

def test_is_happy_zero_raises_value_error():
    with pytest.raises(ValueError):
        is_happy(0)


def test_happy_numbers_zero_raises_value_error():
    with pytest.raises(ValueError):
        happy_numbers(0)


def test_is_happy_negative_raises_value_error():
    with pytest.raises(ValueError):
        is_happy(-7)


def test_happy_numbers_negative_raises_value_error():
    with pytest.raises(ValueError):
        happy_numbers(-1)


# ---------------------------------------------------------------------------
# 入参契约：TypeError（含 bool）
# ---------------------------------------------------------------------------

def test_is_happy_float_raises_type_error():
    with pytest.raises(TypeError):
        is_happy(1.5)


def test_is_happy_bool_raises_type_error():
    with pytest.raises(TypeError):
        is_happy(True)


def test_happy_numbers_float_raises_type_error():
    with pytest.raises(TypeError):
        happy_numbers(10.0)


def test_happy_numbers_bool_raises_type_error():
    with pytest.raises(TypeError):
        happy_numbers(False)


def test_is_happy_none_raises_type_error():
    with pytest.raises(TypeError):
        is_happy(None)


def test_happy_numbers_str_raises_type_error():
    with pytest.raises(TypeError):
        happy_numbers("100")
