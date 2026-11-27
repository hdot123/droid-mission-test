"""huffman：规范 Huffman 编码（第五十九轮 D 单 · 池外同构新题 R55）。

三个层次分明的步骤：

1. ``huffman_code_lengths`` —— 按 Huffman 合并求各符号码长。合并序钉死：
   每步取权重最小的两者合并；权重并列时取「子树最小符号」小者先出
   （叶子子树的最小符号即符号本身）。单符号码长 1，空表返回 {}。
   码长由合并序唯一确定，并列规则不钉死，教科书锚的码长组就会漂移。
2. ``huffman_codes`` —— 由码长赋**规范码**（canonical，DEFLATE 式）：
   按（码长, 符号）升序排队，同长内按符号序码值递增，变长时左移补零。
   规范码赋值与建树是两步：绝不拿建树时的左右分支路径直接当码字。
3. ``huffman_encode`` / ``huffman_decode`` —— 按给定码表编码／解码。

只用标准库；不 import 同轮的 natsort、happy。
"""

import heapq

__all__ = [
    "huffman_code_lengths",
    "huffman_codes",
    "huffman_encode",
    "huffman_decode",
]


def _validate_freqs(freqs):
    """入参体检：freqs 必须是 dict[str, 正 int]。"""
    if not isinstance(freqs, dict):
        raise TypeError("freqs must be a dict, got %r" % (type(freqs).__name__,))
    for symbol, weight in freqs.items():
        if not isinstance(symbol, str) or symbol == "":
            raise TypeError("symbols must be non-empty str, got %r" % (symbol,))
        if not isinstance(weight, int):
            raise TypeError(
                "frequency must be int, got %r" % (type(weight).__name__,)
            )
        if weight <= 0:
            raise ValueError("frequency must be > 0, got %r" % (weight,))


def _merge_node_lengths(root):
    """遍历合并树求各叶深度（码长）。"""
    lengths = {}
    stack = [(root, 0)]
    while stack:
        node, depth = stack.pop()
        kind = node[0]
        if kind == "leaf":
            lengths[node[1]] = depth
        else:
            stack.append((node[1], depth + 1))
            stack.append((node[2], depth + 1))
    return lengths


def huffman_code_lengths(freqs: dict) -> dict:
    """按 Huffman 合并求各符号码长。

    合并序钉死：每步取权重最小两者合并，权重并列时取子树最小符号小者先出。
    单符号码长 1，空表返回 {}。频次 <= 0 抛 ValueError；
    频次非 int、符号非 str 或为空串、freqs 非 dict 抛 TypeError。
    """
    _validate_freqs(freqs)
    if not freqs:
        return {}
    if len(freqs) == 1:
        only = next(iter(freqs))
        return {only: 1}

    # 堆项：(权重, 子树最小符号, 节点)。符号唯一 ⇒ 前两键唯一，节点永不参与比较。
    heap = [(weight, symbol, ("leaf", symbol)) for symbol, weight in freqs.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        w1, min1, n1 = heapq.heappop(heap)
        w2, min2, n2 = heapq.heappop(heap)
        merged_min = min1 if min1 < min2 else min2
        heapq.heappush(heap, (w1 + w2, merged_min, ("node", n1, n2)))
    _, _, root = heap[0]
    return _merge_node_lengths(root)


def huffman_codes(freqs: dict) -> dict:
    """由码长赋规范码：按（码长, 符号）升序、DEFLATE 式赋值。

    同长内按符号序、码值递增、变长时左移补零。入参体检同
    :func:`huffman_code_lengths`。
    """
    lengths = huffman_code_lengths(freqs)
    if not lengths:
        return {}
    ordered = sorted(lengths.items(), key=lambda kv: (kv[1], kv[0]))
    codes = {}
    code = 0
    prev_len = ordered[0][1]
    for symbol, length in ordered:
        code <<= length - prev_len
        codes[symbol] = format(code, "b").zfill(length)
        code += 1
        prev_len = length
    return codes


def huffman_encode(text: str, codes: dict) -> str:
    """按给定码表把 text 编码为比特串。

    text 非 str、codes 非 dict 抛 TypeError；遇无码符号抛 ValueError。
    """
    if not isinstance(text, str):
        raise TypeError("text must be str, got %r" % (type(text).__name__,))
    if not isinstance(codes, dict):
        raise TypeError("codes must be dict, got %r" % (type(codes).__name__,))
    out = []
    for ch in text:
        if ch not in codes:
            raise ValueError("no code for symbol %r" % (ch,))
        out.append(codes[ch])
    return "".join(out)


def _build_trie(codes: dict) -> dict:
    trie = {}
    for symbol, code in codes.items():
        node = trie
        for bit in code:
            node = node.setdefault(bit, {})
        node[""] = symbol  # 终止标记："" 不会与 '0'/'1' 冲突
    return trie


def huffman_decode(bits: str, codes: dict) -> str:
    """按给定码表把比特串解码回文本。

    bits 非 str、codes 非 dict 抛 TypeError；bits 含非 0/1 字符、
    路径不存在或尾部残码抛 ValueError。
    """
    if not isinstance(bits, str):
        raise TypeError("bits must be str, got %r" % (type(bits).__name__,))
    if not isinstance(codes, dict):
        raise TypeError("codes must be dict, got %r" % (type(codes).__name__,))
    trie = _build_trie(codes)
    node = trie
    out = []
    for ch in bits:
        if ch not in "01":
            raise ValueError("bits must contain only '0'/'1', got %r" % (ch,))
        if ch not in node:
            raise ValueError("nonexistent path in code trie at %r" % (ch,))
        node = node[ch]
        if "" in node:
            out.append(node[""])
            node = trie
    if node is not trie:
        raise ValueError("trailing partial code in bits")
    return "".join(out)
