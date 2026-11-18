"""plugin_beta: 导入即向存量 registry 注册名为 beta 的小写处理器。"""

import registry


def _lowercase(text):
    """把文本转小写。"""
    return text.lower()


registry.register("beta", _lowercase)
