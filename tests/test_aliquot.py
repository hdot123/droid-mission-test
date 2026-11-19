import pytest

from aliquot import aliquot_sequence, aliquot_sum, classify


def test_aliquot_sum_known_values():
    assert aliquot_sum(1) == 0
    assert aliquot_sum(2) == 1
    assert aliquot_sum(6) == 6
    assert aliquot_sum(8) == 7
    assert aliquot_sum(12) == 16
    assert aliquot_sum(28) == 28
    assert aliquot_sum(100) == 117
    assert aliquot_sum(220) == 284
    assert aliquot_sum(284) == 220
    assert aliquot_sum(496) == 496


def test_classify():
    assert classify(6) == "perfect"
    assert classify(28) == "perfect"
    assert classify(12) == "abundant"
    assert classify(8) == "deficient"
    assert classify(1) == "deficient"


def test_sequence_basic():
    assert aliquot_sequence(12, 6) == [12, 16, 15, 9, 4, 3]
    assert aliquot_sequence(6, 4) == [6, 6, 6, 6]
    assert aliquot_sequence(220, 3) == [220, 284, 220]
    assert aliquot_sequence(25, 4) == [25, 6, 6, 6]


def test_sequence_stops_early_at_zero():
    assert aliquot_sequence(1, 3) == [1]


def test_aliquot_sum_rejects_non_positive():
    with pytest.raises(ValueError):
        aliquot_sum(0)
    with pytest.raises(ValueError):
        aliquot_sum(-6)


def test_aliquot_sum_rejects_non_int():
    with pytest.raises(TypeError):
        aliquot_sum(6.0)
    with pytest.raises(TypeError):
        aliquot_sum(True)


def test_sequence_rejects_bad_count():
    with pytest.raises(ValueError):
        aliquot_sequence(6, 0)
    with pytest.raises(TypeError):
        aliquot_sequence(6, 2.5)
