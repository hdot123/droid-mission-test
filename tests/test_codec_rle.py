"""codec_rle 测试：只测 codec_rle 自身的编码、解码、往返与目录流水线行为。"""

import codec_rle
import codecbox


def test_rle_encode_examples():
    encode, decode = codecbox.get_codec("rle")
    assert encode("aaab") == "a3b1"
    assert encode("abc") == "a1b1c1"
    assert encode("") == ""


def test_rle_decode_examples():
    encode, decode = codecbox.get_codec("rle")
    assert decode("a3b1") == "aaab"
    assert decode("a1b1c1") == "abc"
    assert decode("") == ""


def test_rle_roundtrip():
    encode, decode = codecbox.get_codec("rle")
    for text in ["", "a", "aaab", "abc", "aabbccca", "zzzzz"]:
        assert decode(encode(text)) == text
        assert encode(decode(encode(text))) == encode(text)


def test_rle_registered():
    assert "rle" in codecbox.codec_names()


def test_rle_pipeline_encode():
    # 导入本模块后，目录流水线编码 "aaab" 的结果恰为 rle 单独工作的结果。
    assert codecbox.pipeline_encode("aaab") == "a3b1"
