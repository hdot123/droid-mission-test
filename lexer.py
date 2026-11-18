"""lexer: 文本切词元（链条第一环，链首，不依赖任何本仓模块）。"""

_PUNCT = ".,;:!?\"'()"


def tokenize(text):
    """把文本切成词元列表。

    统一转小写，按空白切分，剥离每个词首尾的标点字符 .,;:!?"'()，
    空词元丢弃。
    """
    tokens = []
    for raw in text.lower().split():
        token = raw.strip(_PUNCT)
        if token:
            tokens.append(token)
    return tokens
