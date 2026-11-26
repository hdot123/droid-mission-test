"""tests/test_decibel.py: decibel 模块验收测试。"""

import math

import pytest

from decibel import (
    amplitude_ratio_to_db,
    db_to_amplitude_ratio,
    db_to_power_ratio,
    power_ratio_to_db,
)

REL = 1e-9


# ---- power_ratio_to_db 验收要点 ----

def test_power_ratio_to_db_2():
    assert power_ratio_to_db(2) == pytest.approx(3.0102999566398121, rel=REL)


def test_power_ratio_to_db_10():
    assert power_ratio_to_db(10) == pytest.approx(10.0, rel=REL)


def test_power_ratio_to_db_100():
    assert power_ratio_to_db(100) == pytest.approx(20.0, rel=REL)


def test_power_ratio_to_db_1():
    assert power_ratio_to_db(1) == pytest.approx(0.0, rel=REL)


def test_power_ratio_to_db_half():
    assert power_ratio_to_db(0.5) == pytest.approx(-3.0102999566398121, rel=REL)


# ---- amplitude_ratio_to_db 验收要点 ----

def test_amplitude_ratio_to_db_2():
    assert amplitude_ratio_to_db(2) == pytest.approx(6.020599913279624, rel=REL)


def test_amplitude_ratio_to_db_10():
    assert amplitude_ratio_to_db(10) == pytest.approx(20.0, rel=REL)


# ---- db 反解验收要点 ----

def test_db_to_power_ratio_10():
    assert db_to_power_ratio(10) == pytest.approx(10.0, rel=REL)


def test_db_to_amplitude_ratio_20():
    assert db_to_amplitude_ratio(20) == pytest.approx(10.0, rel=REL)


def test_db_to_power_ratio_0():
    assert db_to_power_ratio(0) == pytest.approx(1.0, rel=REL)


# ---- 性质：往返恒等 ----

@pytest.mark.parametrize("x", [0.1, 0.5, 1.0, 2.0, 3.5, 10.0, 100.0, 1234.5])
def test_roundtrip_power(x):
    assert db_to_power_ratio(power_ratio_to_db(x)) == pytest.approx(x, rel=REL)


@pytest.mark.parametrize("x", [0.1, 0.5, 1.0, 2.0, 3.5, 10.0, 100.0, 1234.5])
def test_roundtrip_amplitude(x):
    assert db_to_amplitude_ratio(amplitude_ratio_to_db(x)) == pytest.approx(x, rel=REL)


# ---- 性质：同一比值振幅 dB = 2 × 功率 dB ----

@pytest.mark.parametrize("x", [0.25, 0.5, 1.0, 2.0, 7.0, 10.0, 55.0])
def test_amplitude_is_twice_power(x):
    assert amplitude_ratio_to_db(x) == pytest.approx(
        2 * power_ratio_to_db(x), rel=REL
    )


# ---- ValueError：ratio ≤ 0 ----

def test_power_ratio_zero_value_error():
    with pytest.raises(ValueError):
        power_ratio_to_db(0)


def test_power_ratio_negative_value_error():
    with pytest.raises(ValueError):
        power_ratio_to_db(-3)


def test_amplitude_ratio_zero_value_error():
    with pytest.raises(ValueError):
        amplitude_ratio_to_db(0)


# ---- TypeError：非数值（含 bool） ----

def test_power_ratio_string_type_error():
    with pytest.raises(TypeError):
        power_ratio_to_db("2")


def test_power_ratio_bool_type_error():
    with pytest.raises(TypeError):
        power_ratio_to_db(True)


def test_db_to_power_ratio_string_type_error():
    with pytest.raises(TypeError):
        db_to_power_ratio("3")


def test_amplitude_ratio_bool_type_error():
    with pytest.raises(TypeError):
        amplitude_ratio_to_db(False)


def test_db_to_amplitude_ratio_bool_type_error():
    with pytest.raises(TypeError):
        db_to_amplitude_ratio(True)
