import pytest

from baseconv import from_base, to_base


def test_to_base_basic():
    assert to_base(255, 16) == "ff"
    assert to_base(35, 36) == "z"
    assert to_base(36, 36) == "10"
    assert to_base(0, 2) == "0"


def test_from_base_basic():
    assert from_base("ff", 16) == 255
    assert from_base("1010", 2) == 10
    assert from_base("z", 36) == 35
    assert from_base("10", 36) == 36


def test_to_base_zero():
    for base in range(2, 37):
        assert to_base(0, base) == "0"


def test_uppercase_rejected():
    with pytest.raises(ValueError):
        from_base("FF", 16)


def test_to_base_invalid_base():
    for bad in (0, 1, 37, -2):
        with pytest.raises(ValueError):
            to_base(10, bad)


def test_to_base_negative():
    with pytest.raises(ValueError):
        to_base(-1, 10)


def test_from_base_invalid():
    with pytest.raises(ValueError):
        from_base("", 10)
    with pytest.raises(ValueError):
        from_base("2", 2)
    with pytest.raises(ValueError):
        from_base("g", 16)
    with pytest.raises(ValueError):
        from_base("ff", 1)
    with pytest.raises(ValueError):
        from_base("ff", 37)


def test_roundtrip_123456():
    for base in (2, 8, 16, 36):
        assert from_base(to_base(123456, base), base) == 123456
