"""base32 验收测试：覆盖第四十轮 A 单 base32-codec 的全部验收要点。"""

import pytest

from base32 import decode, encode


def test_encode_empty():
    assert encode(b"") == ""


def test_encode_vectors():
    assert encode(b"f") == "MY======"
    assert encode(b"fo") == "MZXQ===="
    assert encode(b"foo") == "MZXW6==="
    assert encode(b"foob") == "MZXW6YQ="
    assert encode(b"fooba") == "MZXW6YTB"
    assert encode(b"foobar") == "MZXW6YTBOI======"


def test_decode_vectors():
    assert decode("MZXW6YTBOI======") == b"foobar"
    assert decode("MY======") == b"f"


def test_decode_out_of_alphabet_raises():
    with pytest.raises(ValueError):
        decode("MZXW6YT*")


def test_decode_lowercase_raises():
    # 小写字母属于字母表外字符，必须抛 ValueError。
    with pytest.raises(ValueError):
        decode("my======")


def test_decode_bad_length_raises():
    # 长度不合规（非 8 的倍数）。
    with pytest.raises(ValueError):
        decode("MZXW6YT")


def test_decode_bad_padding_raises():
    # 整块都是填充：填充不合规。
    with pytest.raises(ValueError):
        decode("========")
    # '=' 出现在中间：填充不合规。
    with pytest.raises(ValueError):
        decode("MZX=6YTB")
    # 尾部填充位非零：填充不合规。
    with pytest.raises(ValueError):
        decode("MZXW6YT=")


def test_roundtrip_binary():
    data = b"\x00\xff\x10"
    assert decode(encode(data)) == data


def test_roundtrip_lengths():
    data = bytes(range(64))
    for n in range(len(data) + 1):
        chunk = data[:n]
        assert decode(encode(chunk)) == chunk
