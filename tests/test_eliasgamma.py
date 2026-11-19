import pytest

from eliasgamma import elias_decode, elias_decode_list, elias_encode, elias_encode_list


def test_encode_known_values():
    assert elias_encode(1) == "1"
    assert elias_encode(2) == "010"
    assert elias_encode(3) == "011"
    assert elias_encode(4) == "00100"
    assert elias_encode(5) == "00101"
    assert elias_encode(6) == "00110"
    assert elias_encode(7) == "00111"
    assert elias_encode(8) == "0001000"
    assert elias_encode(9) == "0001001"
    assert elias_encode(10) == "0001010"
    assert elias_encode(15) == "0001111"
    assert elias_encode(16) == "000010000"


def test_decode_known_values():
    assert elias_decode("1") == 1
    assert elias_decode("010") == 2
    assert elias_decode("011") == 3
    assert elias_decode("00100") == 4
    assert elias_decode("00101") == 5
    assert elias_decode("00110") == 6
    assert elias_decode("00111") == 7
    assert elias_decode("0001000") == 8
    assert elias_decode("0001001") == 9
    assert elias_decode("0001010") == 10
    assert elias_decode("0001111") == 15
    assert elias_decode("000010000") == 16


def test_roundtrip_1_to_199():
    for n in range(1, 200):
        assert elias_decode(elias_encode(n)) == n


def test_encode_list_known_value():
    assert elias_encode_list([1, 2, 3]) == "1010011"


def test_decode_list_known_value():
    assert elias_decode_list("1010011") == [1, 2, 3]


def test_decode_list_empty_string():
    assert elias_decode_list("") == []


def test_list_roundtrip():
    nums = [5, 1, 9, 16]
    assert elias_decode_list(elias_encode_list(nums)) == nums


def test_encode_list_accepts_tuple():
    assert elias_encode_list((1, 2, 3)) == "1010011"


def test_encode_zero_and_negative_raise_value_error():
    with pytest.raises(ValueError):
        elias_encode(0)
    with pytest.raises(ValueError):
        elias_encode(-3)


def test_encode_float_raises_type_error():
    with pytest.raises(TypeError):
        elias_encode(2.0)


def test_encode_rejects_bool():
    with pytest.raises(TypeError):
        elias_encode(True)
    with pytest.raises(TypeError):
        elias_encode(False)


def test_decode_empty_and_invalid_raise_value_error():
    with pytest.raises(ValueError):
        elias_decode("")
    with pytest.raises(ValueError):
        elias_decode("0")
    with pytest.raises(ValueError):
        elias_decode("01")
    with pytest.raises(ValueError):
        elias_decode("0101")
    with pytest.raises(ValueError):
        elias_decode("012")


def test_decode_list_invalid_raise_value_error():
    with pytest.raises(ValueError):
        elias_decode_list("0100")


def test_decode_non_str_raises_type_error():
    with pytest.raises(TypeError):
        elias_decode(10)


def test_decode_list_non_str_raises_type_error():
    with pytest.raises(TypeError):
        elias_decode_list(10)


def test_encode_list_non_list_tuple_raises_type_error():
    with pytest.raises(TypeError):
        elias_encode_list("123")
    with pytest.raises(TypeError):
        elias_encode_list(10)
