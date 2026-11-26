"""kaprekar 例程测试：覆盖验收单全部 13 个验收要点。"""

import pytest

from kaprekar import kaprekar_steps, kaprekar_trajectory

REPDIGITS = {1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999}


def test_steps_6174_is_zero():
    assert kaprekar_steps(6174) == 0


def test_trajectory_6174_is_start_only():
    assert kaprekar_trajectory(6174) == [6174]


def test_steps_1000_is_five():
    assert kaprekar_steps(1000) == 5


def test_trajectory_1000_records_integer_values():
    assert kaprekar_trajectory(1000) == [1000, 999, 8991, 8082, 8532, 6174]


def test_trajectory_2111_shares_tail_from_999():
    assert kaprekar_trajectory(2111) == [2111, 999, 8991, 8082, 8532, 6174]


def test_domain_every_legal_number_reaches_6174_within_seven_steps():
    """全域性质：任意合法四位数（非四位全同）必到 6174 且步数 ≤ 7。"""
    for n in range(1000, 10000):
        if n in REPDIGITS:
            continue
        steps = kaprekar_steps(n)
        assert isinstance(steps, int)
        assert 0 <= steps <= 7, n
        trajectory = kaprekar_trajectory(n)
        assert trajectory[0] == n
        assert trajectory[-1] == 6174
        assert len(trajectory) - 1 == steps
        assert all(isinstance(value, int) for value in trajectory)


def test_steps_999_raises_value_error():
    with pytest.raises(ValueError):
        kaprekar_steps(999)


def test_steps_10000_raises_value_error():
    with pytest.raises(ValueError):
        kaprekar_steps(10000)


def test_steps_1111_raises_value_error():
    with pytest.raises(ValueError):
        kaprekar_steps(1111)


def test_steps_7777_raises_value_error():
    with pytest.raises(ValueError):
        kaprekar_steps(7777)


def test_trajectory_2222_raises_value_error():
    with pytest.raises(ValueError):
        kaprekar_trajectory(2222)


def test_steps_str_raises_type_error():
    with pytest.raises(TypeError):
        kaprekar_steps("1000")


def test_steps_bool_raises_type_error():
    with pytest.raises(TypeError):
        kaprekar_steps(True)


@pytest.mark.parametrize("bad", [0, -1, 999, 10000, 12345])
def test_both_functions_out_of_range_raise_value_error(bad):
    with pytest.raises(ValueError):
        kaprekar_steps(bad)
    with pytest.raises(ValueError):
        kaprekar_trajectory(bad)


@pytest.mark.parametrize("bad", sorted(REPDIGITS))
def test_both_functions_repdigit_raise_value_error(bad):
    with pytest.raises(ValueError):
        kaprekar_steps(bad)
    with pytest.raises(ValueError):
        kaprekar_trajectory(bad)


@pytest.mark.parametrize("bad", ["1000", True, False, 1000.0, None, [1000]])
def test_both_functions_non_int_raise_type_error(bad):
    with pytest.raises(TypeError):
        kaprekar_steps(bad)
    with pytest.raises(TypeError):
        kaprekar_trajectory(bad)


def test_steps_and_trajectory_consistency():
    for n in (1000, 2111, 1234, 6174, 8991, 9876):
        trajectory = kaprekar_trajectory(n)
        assert len(trajectory) - 1 == kaprekar_steps(n)
