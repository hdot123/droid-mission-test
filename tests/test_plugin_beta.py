"""plugin_beta 测试：只验 beta 插件自身的行为。"""

import registry
import plugin_beta  # noqa: F401  导入即注册


def test_beta_registered():
    assert "beta" in registry.names()


def test_beta_lowercases_text():
    assert registry.get("beta")("ABC") == "abc"
