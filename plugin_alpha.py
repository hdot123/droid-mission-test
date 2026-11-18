"""plugin_alpha: 导入即向 registry 注册名为 alpha 的大写处理器。"""

import registry


def _upper(text):
    return text.upper()


registry.register("alpha", _upper)
