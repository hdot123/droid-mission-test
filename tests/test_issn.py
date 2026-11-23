import pytest

from issn import issn_check_digit, issn_validate


def test_check_digit_real_issn():
    # 真实 ISSN 0378-5955 的前 7 位
    assert issn_check_digit("0378595") == "5"


def test_check_digit_known_values():
    assert issn_check_digit("2049363") == "0"
    assert issn_check_digit("1234567") == "9"
    assert issn_check_digit("0000000") == "0"
    assert issn_check_digit("9999999") == "4"
    assert issn_check_digit("1000002") == "X"


def test_validate_true_forms():
    assert issn_validate("03785955") is True
    assert issn_validate("0378-5955") is True
    assert issn_validate("1000002X") is True
    assert issn_validate("1000-002X") is True


def test_validate_false_forms():
    assert issn_validate("03785954") is False
    assert issn_validate("1000002x") is False
    assert issn_validate("0378595") is False
    assert issn_validate("0378-595") is False
    assert issn_validate("abcdefgh") is False


def test_check_digit_type_error():
    with pytest.raises(TypeError):
        issn_check_digit(378595)


def test_validate_type_error():
    with pytest.raises(TypeError):
        issn_validate(None)


def test_check_digit_value_error():
    with pytest.raises(ValueError):
        issn_check_digit("037859")
    with pytest.raises(ValueError):
        issn_check_digit("03785955")
    with pytest.raises(ValueError):
        issn_check_digit("0378a95")
