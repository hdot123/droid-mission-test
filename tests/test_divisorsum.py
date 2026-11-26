"""Tests for divisorsum: sigma(n), tau(n) and abundance classification."""

import pytest

import divisorsum
from divisorsum import classify_abundance, divisor_count, divisor_sum


# --- divisor_sum -----------------------------------------------------------

def test_divisor_sum_1():
    assert divisor_sum(1) == 1


def test_divisor_sum_2():
    assert divisor_sum(2) == 3


def test_divisor_sum_6():
    assert divisor_sum(6) == 12


def test_divisor_sum_12():
    assert divisor_sum(12) == 28


def test_divisor_sum_28():
    assert divisor_sum(28) == 56


def test_divisor_sum_36():
    assert divisor_sum(36) == 91


def test_divisor_sum_97():
    assert divisor_sum(97) == 98


def test_divisor_sum_100():
    assert divisor_sum(100) == 217


def test_divisor_sum_360():
    assert divisor_sum(360) == 1170


def test_divisor_sum_496():
    assert divisor_sum(496) == 992


def test_divisor_sum_1024():
    assert divisor_sum(1024) == 2047


# --- divisor_count ---------------------------------------------------------

def test_divisor_count_1():
    assert divisor_count(1) == 1


def test_divisor_count_12():
    assert divisor_count(12) == 6


def test_divisor_count_36():
    assert divisor_count(36) == 9


def test_divisor_count_97():
    assert divisor_count(97) == 2


def test_divisor_count_360():
    assert divisor_count(360) == 24


# --- classify_abundance ----------------------------------------------------

def test_classify_perfect_6():
    assert classify_abundance(6) == "perfect"


def test_classify_perfect_28():
    assert classify_abundance(28) == "perfect"


def test_classify_perfect_496():
    assert classify_abundance(496) == "perfect"


def test_classify_abundant_12():
    assert classify_abundance(12) == "abundant"


def test_classify_abundant_18():
    assert classify_abundance(18) == "abundant"


def test_classify_abundant_945():
    assert classify_abundance(945) == "abundant"


def test_classify_deficient_8():
    assert classify_abundance(8) == "deficient"


def test_classify_deficient_97():
    assert classify_abundance(97) == "deficient"


def test_classify_deficient_1():
    assert classify_abundance(1) == "deficient"


# --- input contract --------------------------------------------------------

def test_divisor_sum_zero_raises_value_error():
    with pytest.raises(ValueError):
        divisor_sum(0)


def test_divisor_sum_negative_raises_value_error():
    with pytest.raises(ValueError):
        divisor_sum(-5)


def test_divisor_sum_float_raises_type_error():
    with pytest.raises(TypeError):
        divisor_sum(2.5)


def test_divisor_count_bool_raises_type_error():
    with pytest.raises(TypeError):
        divisor_count(True)


def test_divisor_count_zero_raises_value_error():
    with pytest.raises(ValueError):
        divisor_count(0)


def test_divisor_count_float_raises_type_error():
    with pytest.raises(TypeError):
        divisor_count(1.5)


def test_classify_abundance_zero_raises_value_error():
    with pytest.raises(ValueError):
        classify_abundance(0)


def test_classify_abundance_negative_raises_value_error():
    with pytest.raises(ValueError):
        classify_abundance(-3)


def test_classify_abundance_bool_raises_type_error():
    with pytest.raises(TypeError):
        classify_abundance(False)


def test_classify_abundance_str_raises_type_error():
    with pytest.raises(TypeError):
        classify_abundance("6")


# --- caliber: sigma includes n itself (not aliquot sum) --------------------

def test_sigma_includes_n_itself_not_aliquot_sum():
    # Aliquot sums would be 0, 1, 6 for n = 1, 2, 12; sigma includes n.
    assert divisor_sum(1) == 1
    assert divisor_sum(2) == 3
    assert divisor_sum(12) == 28
    assert divisor_sum(12) - 12 == 16  # aliquot sum of 12


def test_sigma_consistency_with_count():
    for n in (1, 2, 6, 12, 28, 36, 97, 100, 360, 496, 1024):
        divs = [d for d in range(1, n + 1) if n % d == 0]
        assert divisor_sum(n) == sum(divs)
        assert divisor_count(n) == len(divs)


def test_module_exports():
    for name in ("divisor_sum", "divisor_count", "classify_abundance"):
        assert callable(getattr(divisorsum, name))
