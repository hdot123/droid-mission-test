"""codec_flip 测试：只验 codec_flip 自己的登记与翻转行为。"""

import codec_flip  # noqa: F401  导入即触发向 codecbox 登记 flip
import codecbox


def test_flip_name_in_codec_names():
    assert "flip" in codecbox.codec_names()


def test_flip_encode_reverses():
    encode, _ = codecbox.get_codec("flip")
    assert encode("abc") == "cba"


def test_flip_decode_reverses():
    _, decode = codecbox.get_codec("flip")
    assert decode("abc") == "cba"


def test_flip_roundtrip():
    encode, decode = codecbox.get_codec("flip")
    assert decode(encode("abc")) == "abc"
    assert encode(decode("abc")) == "abc"
