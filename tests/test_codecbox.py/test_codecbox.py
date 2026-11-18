"""codecbox 存量测试：只验自己登记的 stock-* 编解码器，对目录全局内容不作断言。"""

from codecbox import add_codec, codec_names, get_codec


def test_stock_red_roundtrip():
    add_codec("stock-red", lambda t: "red:" + t, lambda t: t[4:])
    encode, decode = get_codec("stock-red")
    assert encode("x") == "red:x"
    assert decode(encode("x")) == "x"


def test_stock_green_membership():
    add_codec("stock-green", lambda t: t, lambda t: t)
    assert "stock-green" in codec_names()


def test_stock_blue_roundtrip_and_membership():
    add_codec("stock-blue", lambda t: t.upper(), lambda t: t.lower())
    encode, _ = get_codec("stock-blue")
    assert encode("abc") == "ABC"
    assert "stock-blue" in codec_names()
