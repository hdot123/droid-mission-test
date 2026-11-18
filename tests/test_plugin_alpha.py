"""plugin_alpha 测试：只验 alpha 插件自身的注册与大写行为。"""

import importlib

import plugin_alpha
import registry


def test_alpha_is_only_handler_after_import():
    registry.clear()
    importlib.reload(plugin_alpha)
    assert registry.names() == ["alpha"]


def test_alpha_uppercases_text():
    registry.clear()
    importlib.reload(plugin_alpha)
    assert registry.get("alpha")("abc") == "ABC"
