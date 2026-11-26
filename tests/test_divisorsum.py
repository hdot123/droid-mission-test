import pytest

from divisorsum import classify_abundance, divisor_count, divisor_sum


def test_divisor_sum_acceptance():
    assert divisor_sum(1) == 1
    assert divisor_sum(2) == 3
    assert divisor_sum(6) == 12
    assert divisor_sum(12) == 28
    assert divisor_sum(28) == 56
    assert divisor_sum(36) == 91
    assert divisor_sum(97) == 98
    assert divisor_sum(100) == 217
    assert divisor_sum(360) == 1170
    assert divisor_sum(496) == 992
    assert divisor_sum(1024) == 2047


def test_divisor_count_acceptance():
    assert divisor_count(1) == 1
    assert divisor_count(12) == 6
    assert divisor_count(36) == 9
    assert divisor_count(97) == 2
    assert divisor_count(360) == 24


def test_classify_abundance_perfect():
    assert classify_abundance(6) == "perfect"
    assert classify_abundance(28) == "perfect"
    assert classify_abundance(496) == "perfect"


def test_classify_abundance_abundant():
    assert classify_abundance(12) == "abundant"
    assert classify_abundance(18) == "abundant"
    assert classify_abundance(945) == "abundant"


def test_classify_abundance_deficient():
    assert classify_abundance(8) == "deficient"
    assert classify_abundance(97) == "deficient"
    assert classify_abundance(1) == "deficient"


def test_divisor_sum_value_error():
    for bad in (0, -5):
        with pytest.raises(ValueError):
            divisor_sum(bad)


def test_divisor_sum_type_error():
    for bad in (2.5, True):
        with pytest.raises(TypeError):
            divisor_sum(bad)


def test_divisor_count_and_classify_input_contracts():
    with pytest.raises(TypeError):
        divisor_count(True)
    with pytest.raises(TypeError):
        classify_abundance(2.5)
    with pytest.raises(ValueError):
        divisor_count(0)
    with pytest.raises(ValueError):
        classify_abundance(-1)
