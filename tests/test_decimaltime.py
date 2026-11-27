"""decimaltime 验收测试：逐条对应工单验收要点。"""

import pytest

from decimaltime import from_decimal, to_decimal


# --- to_decimal 验收要点 ---

def test_to_decimal_midnight():
    assert to_decimal(0, 0, 0) == (0, 0, 0)


def test_to_decimal_noon():
    assert to_decimal(12, 0, 0) == (5, 0, 0)


def test_to_decimal_six():
    assert to_decimal(6, 0, 0) == (2, 50, 0)


def test_to_decimal_eighteen():
    assert to_decimal(18, 0, 0) == (7, 50, 0)


def test_to_decimal_one_second_truncation():
    assert to_decimal(0, 0, 1) == (0, 0, 1)


def test_to_decimal_end_of_day():
    assert to_decimal(23, 59, 59) == (9, 99, 98)


def test_to_decimal_one_hour():
    assert to_decimal(1, 0, 0) == (0, 41, 66)


def test_to_decimal_thirty_six_minutes():
    assert to_decimal(0, 36, 0) == (0, 25, 0)


# --- from_decimal 验收要点 ---

def test_from_decimal_zero():
    assert from_decimal(0, 0, 0) == (0, 0, 0)


def test_from_decimal_five_decimal_hours():
    assert from_decimal(5, 0, 0) == (12, 0, 0)


def test_from_decimal_two_fifty():
    assert from_decimal(2, 50, 0) == (6, 0, 0)


def test_from_decimal_end_of_day():
    assert from_decimal(9, 99, 99) == (23, 59, 59)


def test_from_decimal_one_decimal_second_truncation():
    assert from_decimal(0, 0, 1) == (0, 0, 0)


def test_from_decimal_one_decimal_hour():
    assert from_decimal(1, 0, 0) == (2, 24, 0)


# --- 往返 ---

def test_roundtrip_from_to_noon():
    assert from_decimal(*to_decimal(12, 0, 0)) == (12, 0, 0)


def test_roundtrip_to_from_five():
    assert to_decimal(*from_decimal(5, 0, 0)) == (5, 0, 0)


def test_roundtrip_to_from_twenty_five():
    assert to_decimal(*from_decimal(0, 25, 0)) == (0, 25, 0)


# --- 越界 ValueError ---

def test_to_decimal_hour_upper_bound():
    with pytest.raises(ValueError):
        to_decimal(24, 0, 0)


def test_to_decimal_minute_upper_bound():
    with pytest.raises(ValueError):
        to_decimal(0, 60, 0)


def test_to_decimal_second_upper_bound():
    with pytest.raises(ValueError):
        to_decimal(0, 0, 60)


def test_to_decimal_negative_hour():
    with pytest.raises(ValueError):
        to_decimal(-1, 0, 0)


def test_from_decimal_decimal_hour_upper_bound():
    with pytest.raises(ValueError):
        from_decimal(10, 0, 0)


def test_from_decimal_decimal_minute_upper_bound():
    with pytest.raises(ValueError):
        from_decimal(0, 100, 0)


def test_from_decimal_negative_decimal_second():
    with pytest.raises(ValueError):
        from_decimal(0, 0, -1)


# --- 类型 TypeError ---

def test_to_decimal_rejects_str():
    with pytest.raises(TypeError):
        to_decimal("12", 0, 0)


def test_to_decimal_rejects_bool():
    with pytest.raises(TypeError):
        to_decimal(True, 0, 0)


def test_from_decimal_rejects_float():
    with pytest.raises(TypeError):
        from_decimal(1.5, 0, 0)


# --- 规格补充：其余参数位与其余拒绝形态 ---

def test_to_decimal_rejects_non_numeric_in_each_position():
    with pytest.raises(TypeError):
        to_decimal(0, "0", 0)
    with pytest.raises(TypeError):
        to_decimal(0, 0, None)


def test_from_decimal_rejects_bool_and_str():
    with pytest.raises(TypeError):
        from_decimal(True, 0, 0)
    with pytest.raises(TypeError):
        from_decimal("1", 0, 0)


def test_to_decimal_accepts_float_inputs():
    assert to_decimal(12.0, 0, 0) == (5, 0, 0)


def test_to_decimal_negative_minute_and_second():
    with pytest.raises(ValueError):
        to_decimal(0, -1, 0)
    with pytest.raises(ValueError):
        to_decimal(0, 0, -1)


def test_from_decimal_negative_decimal_hour_and_minute():
    with pytest.raises(ValueError):
        from_decimal(-1, 0, 0)
    with pytest.raises(ValueError):
        from_decimal(0, -1, 0)
