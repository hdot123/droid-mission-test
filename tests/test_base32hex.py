import pytest

from base32hex import decode, encode


# --- 验收要点：RFC 4648 测试向量 -----------------------------------------

def test_encode_empty():
    assert encode(b"") == ""


def test_encode_f():
    assert encode(b"f") == "CO======"


def test_encode_fo():
    assert encode(b"fo") == "CPNG===="


def test_encode_foo():
    assert encode(b"foo") == "CPNMU==="


def test_encode_foob():
    assert encode(b"foob") == "CPNMUOG="


def test_encode_fooba():
    assert encode(b"fooba") == "CPNMUOJ1"


def test_encode_foobar():
    assert encode(b"foobar") == "CPNMUOJ1E8======"


# --- 验收要点：解码与往返 -------------------------------------------------

def test_decode_foobar():
    assert decode("CPNMUOJ1E8======") == b"foobar"


def test_roundtrip_binary_identity():
    data = b"\x00\xff\x10"
    assert decode(encode(data)) == data


def test_roundtrip_various_lengths():
    for data in (b"", b"a", b"ab", b"abc", b"abcd", b"abcde", b"abcdef", b"abcdefg"):
        assert decode(encode(data)) == data


# --- 验收要点：非法输入抛 ValueError --------------------------------------

def test_decode_out_of_alphabet():
    # W 不在 0-9A-V 字母表内；长度合规以隔离字母表错误。
    with pytest.raises(ValueError):
        decode("0000000W")


def test_decode_non_conforming_padding():
    # 填充位置错误（= 出现在数据中间）。
    with pytest.raises(ValueError):
        decode("CP=NMU==")
    # 数据字符数模 8 为 3，填充位数不合规。
    with pytest.raises(ValueError):
        decode("CPN=====")
    # 数据字符数模 8 为 6，填充位数不合规。
    with pytest.raises(ValueError):
        decode("CPNMUO==")


def test_decode_non_conforming_length():
    # 总长度不是 8 的倍数。
    with pytest.raises(ValueError):
        decode("CPNMUOJ1E8=====")
    with pytest.raises(ValueError):
        decode("ABC")


def test_decode_empty():
    assert decode("") == b""


def test_decode_rejects_non_zero_trailing_bits():
    # RFC 4648 要求末字符的不可用比特置 0；"9" 的低 2 比特为 01，非全零。
    with pytest.raises(ValueError):
        decode("CPNMUOJ1E9======")
