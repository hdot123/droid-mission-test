"""semvercmp: 语义版本三段比较工具（第三十六轮交付件）。

compare(a, b) 比较恰好三段以 '.' 分隔的非负整数版本号，按数值比较，
返回 -1 / 0 / 1。前导零允许（"1.02.3" 等价于 "1.2.3"）。格式不合
（段数不对、含非数字、负号、空串，或出现预发布/构建后缀 '-' / '+'）
一律抛 ValueError。本模块只用标准库，且不依赖其他交付模块。
"""

__all__ = ["compare"]


def _parse(version):
    """把版本串解析为三元整数组；格式不合抛 ValueError。"""
    if not isinstance(version, str):
        raise ValueError("invalid version: %r" % (version,))
    # 预发布/构建后缀不处理：出现 '-' 或 '+' 即格式不合。
    if "-" in version or "+" in version:
        raise ValueError("invalid version: %r" % (version,))
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError("invalid version: %r" % (version,))
    numbers = []
    for part in parts:
        if not part or not part.isdigit():
            raise ValueError("invalid version: %r" % (version,))
        numbers.append(int(part))
    return tuple(numbers)


def compare(a, b):
    """比较两个三段版本号，返回 -1 / 0 / 1；格式不合抛 ValueError。"""
    left = _parse(a)
    right = _parse(b)
    if left < right:
        return -1
    if left > right:
        return 1
    return 0
