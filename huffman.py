"""huffman: 规范 Huffman 编码工具（第五十九轮 D 单）。

三个独立函数：

- ``huffman_code_lengths(freqs)``: 按钉死合并序求各符号码长。
  合并序：每步取权重最小两者合并；权重并列时，取子树最小符号小者先出
  （叶子子树的最小符号即符号本身）。单符号码长 1，空表返回 {}。
- ``huffman_codes(freqs)``: 由码长赋 DEFLATE 式规范码——按（码长，符号）
  升序、同长内按符号序、码值递增、变长时左移补零。规范码赋值与建树是
  两步，不使用建树时的左右分支路径当码字。
- ``huffman_encode(text, codes)`` / ``huffman_decode(bits, codes)``:
  按给定码表编码／解码。

与 eliasgamma／deltaenc 同编码族但函数全异：本模块是数据依赖最优前缀码，
那两个是固定规则编码。
"""

import heapq

__all__ = [
    "huffman_code_lengths",
    "huffman_codes",
    "huffman_encode",
    "huffman_decode",
]

# 解码 trie 的终结标记（与 '0'/'1' 字符键不冲突）
_TERM = object()


def _validate_freqs(freqs):
    """校验频次表，返回 (符号, 频次) 列表。

    freqs 非 dict、符号非 str 或为空串、频次非 int 抛 TypeError；
    频次 <= 0 抛 ValueError。
    """
    if not isinstance(freqs, dict):
        raise TypeError("freqs must be a dict, got %s" % type(freqs).__name__)
    items = []
    for symbol, freq in freqs.items():
        if not isinstance(symbol, str) or symbol == "":
            raise TypeError("symbol must be a non-empty str, got %r" % (symbol,))
        if isinstance(freq, bool) or not isinstance(freq, int):
            raise TypeError("freq must be an int, got %r" % (freq,))
        if freq <= 0:
            raise ValueError("freq must be positive, got %r" % (freq,))
        items.append((symbol, freq))
    return items


def _lengths_from_root(root):
    """对合并出的树做 DFS，叶子深度即码长（单符号根深度 0 记为 1）。"""
    lengths = {}
    stack = [(root, 0)]
    while stack:
        node, depth = stack.pop()
        if node[0] == "leaf":
            lengths[node[1]] = depth if depth > 0 else 1
        else:
            stack.append((node[1], depth + 1))
            stack.append((node[2], depth + 1))
    return lengths


def huffman_code_lengths(freqs: dict) -> dict:
    """按 Huffman 合并求各符号码长（合并序钉死：权重小者先，权重并列取子树最小符号小者先）。"""
    items = _validate_freqs(freqs)
    if not items:
        return {}
    # 堆元素 (权重, 子树最小符号, 子树)。符号在活节点间互不相同，
    # 故 (权重, 最小符号) 不会并列，第三元永不参与比较。
    heap = [(freq, symbol, ("leaf", symbol)) for symbol, freq in items]
    heapq.heapify(heap)
    while len(heap) > 1:
        w1, m1, n1 = heapq.heappop(heap)
        w2, m2, n2 = heapq.heappop(heap)
        merged = ("node", n1, n2)
        heapq.heappush(heap, (w1 + w2, m1 if m1 < m2 else m2, merged))
    return _lengths_from_root(heap[0][2])


def huffman_codes(freqs: dict) -> dict:
    """由码长赋 DEFLATE 式规范码（按（码长，符号）升序，与建树两步分离）。"""
    lengths = huffman_code_lengths(freqs)
    if not lengths:
        return {}
    order = sorted(lengths.items(), key=lambda kv: (kv[1], kv[0]))
    code = 0
    prev_len = order[0][1]
    codes = {}
    for symbol, length in order:
        if length != prev_len:
            code <<= length - prev_len
            prev_len = length
        codes[symbol] = bin(code)[2:].zfill(length)
        code += 1
    return codes


def huffman_encode(text: str, codes: dict) -> str:
    """按给定码表编码 text。

    text 非 str 或 codes 非 dict 抛 TypeError；遇无码符号抛 ValueError。
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str, got %s" % type(text).__name__)
    if not isinstance(codes, dict):
        raise TypeError("codes must be a dict, got %s" % type(codes).__name__)
    parts = []
    for ch in text:
        if ch not in codes:
            raise ValueError("no code for symbol %r" % (ch,))
        parts.append(codes[ch])
    return "".join(parts)


def huffman_decode(bits: str, codes: dict) -> str:
    """按给定码表解码 bits。

    bits 非 str 或 codes 非 dict 抛 TypeError；bits 含非 0/1 字符、
    路径不存在或尾部残码抛 ValueError。
    """
    if not isinstance(bits, str):
        raise TypeError("bits must be a str, got %s" % type(bits).__name__)
    if not isinstance(codes, dict):
        raise TypeError("codes must be a dict, got %s" % type(codes).__name__)
    root = {}
    for symbol, code in codes.items():
        node = root
        for bit in code:
            node = node.setdefault(bit, {})
        node[_TERM] = symbol
    out = []
    node = root
    for ch in bits:
        if ch != "0" and ch != "1":
            raise ValueError("bits must contain only '0'/'1', got %r" % (ch,))
        if ch not in node:
            raise ValueError("no code path for bit %r" % (ch,))
        node = node[ch]
        if _TERM in node:
            out.append(node[_TERM])
            node = root
    if node is not root:
        raise ValueError("trailing partial code in %r" % (bits,))
    return "".join(out)
