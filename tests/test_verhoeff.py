import pytest

from verhoeff import checksum, validate


def test_checksum_known_values():
    assert checksum("236") == 3
    assert checksum("12345") == 1
    assert checksum("042") == 8


def test_validate_known_values():
    assert validate("2363") is True
    assert validate("2364") is False
    assert validate("123451") is True


def test_checksum_empty_raises():
    with pytest.raises(ValueError):
        checksum("")


def test_checksum_non_digit_raises():
    with pytest.raises(ValueError):
        checksum("12a")


def test_validate_empty_raises():
    with pytest.raises(ValueError):
        validate("")


def test_checksum_roundtrip_with_validate():
    # 每个 checksum 的结果拼到原串后，validate 应通过。
    for body in ("236", "12345", "042", "0", "999999999"):
        check = checksum(body)
        assert 0 <= check <= 9
        assert validate(body + str(check)) is True


def test_validate_detects_single_digit_corruption():
    body = "4937725"
    good = body + str(checksum(body))
    assert validate(good) is True
    # 逐位破坏，均应校验失败。
    for i, ch in enumerate(good):
        bad = "1234567890"[(int(ch) + 1) % 10]
        corrupted = good[:i] + bad + good[i + 1:]
        assert validate(corrupted) is False
