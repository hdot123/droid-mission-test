"""registry 存量测试：只验自己登记的 stock-* 键，对注册表全局内容不作断言。"""

from registry import get, names, register


def test_stock_red_roundtrip():
    def handler(text):
        return "red:" + text

    register("stock-red", handler)
    assert get("stock-red") is handler
    assert get("stock-red")("x") == "red:x"


def test_stock_green_membership():
    register("stock-green", lambda text: text)
    assert "stock-green" in names()


def test_stock_blue_roundtrip_and_membership():
    register("stock-blue", lambda text: text.upper())
    assert get("stock-blue")("abc") == "ABC"
    assert "stock-blue" in names()
