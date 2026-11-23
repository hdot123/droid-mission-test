"""damm.py 的验收测试：覆盖规格中每一个验收要点。"""

import pytest

from damm import damm_check_digit, damm_validate


def test_public_example_check_digit():
    assert damm_check_digit("572") == "4"


def test_public_example_validate():
    assert damm_validate("5724") is True


def test_transposition_detected():
    assert damm_validate("5742") is False


def test_check_digit_123():
    assert damm_check_digit("123") == "4"


def test_check_digit_single_zero():
    assert damm_check_digit("0") == "0"


def test_check_digit_42():
    assert damm_check_digit("42") == "7"


def test_check_digit_987654321():
    assert damm_check_digit("987654321") == "5"


def test_check_digit_2024():
    assert damm_check_digit("2024") == "0"


def test_validate_1234_true():
    assert damm_validate("1234") is True


def test_validate_1235_false():
    assert damm_validate("1235") is False


def test_validate_427_true():
    assert damm_validate("427") is True


def test_check_digit_rejects_non_str():
    with pytest.raises(TypeError):
        damm_check_digit(572)


def test_check_digit_rejects_empty():
    with pytest.raises(ValueError):
        damm_check_digit("")


def test_check_digit_rejects_non_ascii_digit():
    with pytest.raises(ValueError):
        damm_check_digit("57a")


def test_validate_rejects_space():
    with pytest.raises(ValueError):
        damm_validate("57 24")


def test_validate_rejects_non_str():
    with pytest.raises(TypeError):
        damm_validate(5724)


def test_validate_rejects_empty():
    with pytest.raises(ValueError):
        damm_validate("")


def test_validate_rejects_non_ascii_digit_chars():
    for bad in ("５７２４", "57²4", "57\t24", "57-24"):
        with pytest.raises(ValueError):
            damm_validate(bad)
