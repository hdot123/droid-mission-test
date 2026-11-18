"""codecbox: 存量编解码器目录（模块级单例）。

仓库既有的编解码器目录：编解码器模块在导入时调用 add_codec() 把自己登记进来，
调用方用 get_codec() 按名取回编解码对、codec_names() 查看已登记名单，
pipeline_encode() 按登记顺序把全部已登记编解码器串成流水线编码。
"""

_codecs = {}
_order = []


def add_codec(name, encode, decode):
    """把 (encode, decode) 以 name 登记进目录；同名重复登记以最后一次为准。"""
    if name not in _codecs:
        _order.append(name)
    _codecs[name] = (encode, decode)


def get_codec(name):
    """按名取回已登记的 (encode, decode) 对；未登记时抛 KeyError。"""
    return _codecs[name]


def codec_names():
    """返回全部已登记编解码器名（按登记先后顺序）。"""
    return list(_order)


def pipeline_encode(text):
    """按登记顺序依次用每个编解码器的 encode 处理 text，返回最终结果。"""
    for name in _order:
        text = _codecs[name][0](text)
    return text


def reset():
    """清空目录中的全部编解码器。"""
    _codecs.clear()
    _order.clear()
