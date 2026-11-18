"""registry: 存量插件注册表（模块级单例）。

仓库既有的处理器注册表：插件模块在导入时调用 register() 把自己登记进来，
调用方用 get() 按名取回处理器、names() 查看已注册名单。
"""

_handlers = {}


def register(name, handler):
    """把 handler 以 name 登记进注册表；同名重复登记以最后一次为准。"""
    _handlers[name] = handler


def get(name):
    """按名取回已注册的处理器；未注册时抛 KeyError。"""
    return _handlers[name]


def names():
    """返回全部已注册处理器名的排序列表。"""
    return sorted(_handlers)


def clear():
    """清空注册表中的全部处理器。"""
    _handlers.clear()
