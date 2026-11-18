import pytest

from base32hex import decode, encode


def test_encode_examples():
    assert encode(b"") == ""
    assert encode(b"f") == "CO======"
    assert encode(b"fo") == "CPNG===="
    assert encode(b"foo") == "CPNMU==="
    assert encode(b"foob") == "CPNMUOG="
    assert encode(b"fooba") == "CPNMUOJ1"
    assert encode(b"foobar") == "CPNMUOJ1E8======"


def test_decode_examples():
    assert decode("") == b""
    assert decode("CO======") == b"f"
    assert decode("CPNG====") == b"fo"
    assert decode("CPNMU===") == b"foo"
    assert decode("CPNMUOG=") == b"foob"
    assert decode("CPNMUOJ1") == b"fooba"
    assert decode("CPNMUOJ1E8======") == b"foobar"


def test_encode_output_length_multiple_of_8():
    for n in range(0, 24):
        out = encode(bytes((i * 7 + 3) % 256 for i in range(n)))
        assert len(out) % 8 == 0


def test_roundtrip():
    for n in range(0, 40):
        data = bytes((i * 37 + 5) % 256 for i in range(n))
        assert decode(encode(data)) == data


def test_decode_length_not_multiple_of_8():
    for bad in ("A", "CO=====", "CPNMUOJ", "CPNMUOJ1E", "CO======X"):
        with pytest.raises(ValueError):
            decode(bad)


def test_decode_outside_alphabet():
    # 小写与字母表外字符（W、@、空格）均非法，长度仍为 8 的倍数。
    for bad in ("cpnmuoj1", "CPNMUOJW", "CPNMUOJ@", "CPNMUOJ "):
        with pytest.raises(ValueError):
            decode(bad)


def test_decode_equals_not_at_end():
    for bad in ("=PNMUOJ1", "CP=NMUO1", "C=NMUOJ1"):
        with pytest.raises(ValueError):
            decode(bad)


def test_decode_invalid_pad_count():
    # 合法补齐个数只有 0、1、3、4、6；7、5、2、8 均非法。
    for bad in ("C=======", "CPN=====", "CPNMUO==", "========"):
        with pytest.raises(ValueError):
            decode(bad)


def test_decode_valid_pad_counts():
    assert decode("CO======") == b"f"  # pad 6
    assert decode("CPNG====") == b"fo"  # pad 4
    assert decode("CPNMU===") == b"foo"  # pad 3
    assert decode("CPNMUOG=") == b"foob"  # pad 1
    assert decode("CPNMUOJ1E8======") == b"foobar"  # pad 0 的整块
