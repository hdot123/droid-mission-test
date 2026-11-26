"""stirling2.py 的验收测试：逐项比对每个 S(n, k)，不用行和凑数捷径。"""

import pytest

from stirling2 import stirling2, stirling2_row

# 逐项验收要点：每个 S(n, k) 单独断言（非行和捷径）
EXACT_VALUES = [
    (0, 0, 1),
    (5, 0, 0),
    (0, 3, 0),
    (3, 5, 0),
    (1, 1, 1),
    (2, 1, 1),
    (2, 2, 1),
    (3, 2, 3),
    (4, 2, 7),
    (4, 3, 6),
    (5, 2, 15),
    (5, 3, 25),
    (5, 4, 10),
    (6, 3, 90),
    (6, 4, 65),
    (7, 3, 301),
    (8, 4, 1701),
    (9, 3, 3025),
    (10, 5, 42525),
    (15, 5, 210766920),
]


@pytest.mark.parametrize("n,k,expected", EXACT_VALUES)
def test_stirling2_exact_values(n, k, expected):
    result = stirling2(n, k)
    assert result == expected
    assert isinstance(result, int)


def test_stirling2_zero_cases():
    assert stirling2(0, 0) == 1
    assert stirling2(5, 0) == 0
    assert stirling2(0, 3) == 0
    assert stirling2(3, 5) == 0


def test_stirling2_large_value_is_exact_int():
    result = stirling2(15, 5)
    assert result == 210766920
    assert isinstance(result, int)


def test_stirling2_row_small():
    assert stirling2_row(0) == [1]


def test_stirling2_row_four():
    assert stirling2_row(4) == [0, 1, 7, 6, 1]


def test_stirling2_row_matches_individual_values():
    """行的每一项与其独立计算的 S(n, k) 逐项一致（非行和比对）。"""
    for n in range(0, 12):
        row = stirling2_row(n)
        assert len(row) == n + 1
        for k in range(0, n + 1):
            assert row[k] == stirling2(n, k)


def test_negative_raises_value_error():
    with pytest.raises(ValueError):
        stirling2(-1, 0)
    with pytest.raises(ValueError):
        stirling2(3, -1)
    with pytest.raises(ValueError):
        stirling2_row(-2)


def test_non_int_raises_type_error():
    with pytest.raises(TypeError):
        stirling2(3.0, 1)
    with pytest.raises(TypeError):
        stirling2(3, True)
    with pytest.raises(TypeError):
        stirling2_row("3")
