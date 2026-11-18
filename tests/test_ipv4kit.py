"""tests for ipv4kit: IPv4 点分十进制互转。"""

import pytest

import ipv4kit


# --- 验收要点：parse 正例 ---

def test_parse_192_168_0_1():
    assert ipv4kit.parse("192.168.0.1") == 3232235521


def test_parse_all_zero():
    assert ipv4kit.parse("0.0.0.0") == 0


def test_parse_all_255():
    assert ipv4kit.parse("255.255.255.255") == 4294967295


# --- 验收要点：format 正例 ---

def test_format_192_168_0_1():
    assert ipv4kit.format(3232235521) == "192.168.0.1"


# --- 验收要点：parse 反例（均抛 ValueError） ---

def test_parse_leading_zero_rejected():
    with pytest.raises(ValueError):
        ipv4kit.parse("01.2.3.4")


def test_parse_octet_out_of_range_rejected():
    with pytest.raises(ValueError):
        ipv4kit.parse("256.0.0.1")


def test_parse_too_few_segments_rejected():
    with pytest.raises(ValueError):
        ipv4kit.parse("1.2.3")


def test_parse_trailing_space_rejected():
    with pytest.raises(ValueError):
        ipv4kit.parse("1.2.3.4 ")


# --- 验收要点：往返恒等 ---

def test_roundtrip_10_20_30_40():
    text = "10.20.30.40"
    assert ipv4kit.format(ipv4kit.parse(text)) == text


# --- 补充边界：前导零在任意段、更多/更少段、空串、非数字 ---

def test_parse_leading_zero_in_middle_segment():
    with pytest.raises(ValueError):
        ipv4kit.parse("1.02.3.4")


def test_parse_too_many_segments_rejected():
    with pytest.raises(ValueError):
        ipv4kit.parse("1.2.3.4.5")


def test_parse_empty_string_rejected():
    with pytest.raises(ValueError):
        ipv4kit.parse("")


def test_parse_non_digit_rejected():
    with pytest.raises(ValueError):
        ipv4kit.parse("1.2.3.a")


def test_parse_plus_sign_rejected():
    with pytest.raises(ValueError):
        ipv4kit.parse("+1.2.3.4")


def test_parse_internal_space_rejected():
    with pytest.raises(ValueError):
        ipv4kit.parse("1.2. 3.4")


def test_parse_empty_segment_rejected():
    with pytest.raises(ValueError):
        ipv4kit.parse("1..3.4")


# --- 补充边界：format 越界 ---

def test_format_negative_rejected():
    with pytest.raises(ValueError):
        ipv4kit.format(-1)


def test_format_too_large_rejected():
    with pytest.raises(ValueError):
        ipv4kit.format(4294967296)


def test_format_bounds_ok():
    assert ipv4kit.format(0) == "0.0.0.0"
    assert ipv4kit.format(4294967295) == "255.255.255.255"


# --- 补充：全值域抽样往返恒等 ---

@pytest.mark.parametrize(
    "value",
    [0, 1, 255, 256, 65535, 65536, 16777215, 16777216, 3232235521, 4294967295],
)
def test_roundtrip_sampled_values(value):
    assert ipv4kit.parse(ipv4kit.format(value)) == value
