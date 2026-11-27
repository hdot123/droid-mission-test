import pytest

from base62 import base62_decode, base62_encode


# ---- encode 基本要点 ----

def test_encode_zero_and_single_digits():
    assert base62_encode(0) == "0"
    assert base62_encode(1) == "1"
    assert base62_encode(9) == "9"


def test_encode_alpha_boundaries():
    assert base62_encode(10) == "A"
    assert base62_encode(35) == "Z"
    assert base62_encode(36) == "a"
    assert base62_encode(61) == "z"


def test_encode_two_and_three_digit_carry():
    assert base62_encode(62) == "10"
    assert base62_encode(63) == "11"
    assert base62_encode(3843) == "zz"
    assert base62_encode(238327) == "zzz"


def test_encode_sample_values():
    assert base62_encode(12345) == "3D7"
    assert base62_encode(987654321) == "14q60P"


# ---- decode 基本要点 ----

def test_decode_zero_and_samples():
    assert base62_decode("0") == 0
    assert base62_decode("3D7") == 12345
    assert base62_decode("zzz") == 238327
    assert base62_decode("14q60P") == 987654321


# ---- 往返 ----

@pytest.mark.parametrize(
    "n",
    [0, 1, 61, 62, 3844, 10**12, 2**63 - 1],
)
def test_roundtrip(n):
    assert base62_decode(base62_encode(n)) == n


# ---- encode 错误 ----

def test_encode_negative_raises_value_error():
    with pytest.raises(ValueError):
        base62_encode(-1)


@pytest.mark.parametrize("bad", [1.5, True, "12"])
def test_encode_non_int_raises_type_error(bad):
    with pytest.raises(TypeError):
        base62_encode(bad)


# ---- decode 错误 ----

@pytest.mark.parametrize("bad", ["", "!", "a b"])
def test_decode_invalid_string_raises_value_error(bad):
    with pytest.raises(ValueError):
        base62_decode(bad)


@pytest.mark.parametrize("bad", [123, None])
def test_decode_non_str_raises_type_error(bad):
    with pytest.raises(TypeError):
        base62_decode(bad)
