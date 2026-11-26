"""punycode 组件测试（第五十五轮并发 D 单 · 验收要点全覆盖）。"""

import punycode
from punycode import puny_encode, puny_decode

# 多语种与 emoji 样本集，用于往返性与标准库对照。
ROUNDTRIP_SAMPLES = [
    "日本語",
    "Москва",
    "αβγ",
    "😀",
    "3年B組金八先生",
    "bücher",
    "mañana",
    "münchen",
    "中文",
    "abc",
    "",
    "ABC-123",
    "a" * 50 + "é",
    "hello world",
    "Ωmega-Ω",
]


def _stdlib_encode(s):
    return s.encode("punycode").decode("ascii")


def _stdlib_decode(s):
    return s.encode("ascii").decode("punycode")


class TestPunyEncode:
    def test_empty_string(self):
        assert puny_encode("") == ""

    def test_ascii_gets_trailing_hyphen(self):
        assert puny_encode("abc") == "abc-"

    def test_bucher(self):
        assert puny_encode("bücher") == "bcher-kva"

    def test_manana(self):
        assert puny_encode("mañana") == "maana-pta"

    def test_munchen(self):
        assert puny_encode("münchen") == "mnchen-3ya"

    def test_japanese(self):
        assert puny_encode("日本語") == "wgv71a119e"

    def test_chinese(self):
        assert puny_encode("中文") == "fiq228c"

    def test_non_str_raises_type_error(self):
        try:
            puny_encode(123)
        except TypeError:
            pass
        else:
            raise AssertionError("puny_encode(123) should raise TypeError")

    def test_non_str_raises_type_error_for_none(self):
        try:
            puny_encode(None)
        except TypeError:
            pass
        else:
            raise AssertionError("puny_encode(None) should raise TypeError")


class TestPunyDecode:
    def test_empty_string(self):
        assert puny_decode("") == ""

    def test_ascii_with_trailing_hyphen(self):
        assert puny_decode("abc-") == "abc"

    def test_bucher(self):
        assert puny_decode("bcher-kva") == "bücher"

    def test_non_ascii_input_raises_value_error(self):
        try:
            puny_decode("bücher")
        except ValueError:
            pass
        else:
            raise AssertionError('puny_decode("bücher") should raise ValueError')

    def test_illegal_digit_raises_value_error(self):
        try:
            puny_decode("abc!")
        except ValueError:
            pass
        else:
            raise AssertionError('puny_decode("abc!") should raise ValueError')

    def test_truncated_input_raises_value_error(self):
        try:
            puny_decode("bcher-kv")
        except ValueError:
            pass
        else:
            raise AssertionError("truncated punycode should raise ValueError")

    def test_non_str_raises_type_error(self):
        try:
            puny_decode(123)
        except TypeError:
            pass
        else:
            raise AssertionError("puny_decode(123) should raise TypeError")


class TestRoundTripAndStdlibParity:
    def test_roundtrip(self):
        for sample in ROUNDTRIP_SAMPLES:
            assert puny_decode(puny_encode(sample)) == sample, sample

    def test_encode_matches_stdlib(self):
        for sample in ROUNDTRIP_SAMPLES:
            assert puny_encode(sample) == _stdlib_encode(sample), sample

    def test_decode_matches_stdlib(self):
        for sample in ROUNDTRIP_SAMPLES:
            encoded = _stdlib_encode(sample)
            assert puny_decode(encoded) == _stdlib_decode(encoded), sample

    def test_mixed_corpus_matches_stdlib(self):
        corpus = [
            "例子",
            "例え",
            "παράδειγμα",
            "ИСПЫТАНИЕ",
            "🇺🇸🇯🇵",
            "àéîõü",
            "Ⅻ",
            "com.example.测试",
            "a-",
            "-",
            "0",
            "z" * 100,
        ]
        for sample in corpus:
            encoded = _stdlib_encode(sample)
            assert puny_encode(sample) == encoded, sample
            assert puny_decode(encoded) == sample, sample
            assert puny_decode(puny_encode(sample)) == sample, sample

    def test_every_acceptance_example(self):
        # 逐条验收要点回放（与验收清单逐字对应）。
        assert puny_encode("") == ""
        assert puny_encode("abc") == "abc-"
        assert puny_encode("bücher") == "bcher-kva"
        assert puny_encode("mañana") == "maana-pta"
        assert puny_encode("münchen") == "mnchen-3ya"
        assert puny_encode("日本語") == "wgv71a119e"
        assert puny_encode("中文") == "fiq228c"
        assert puny_decode("") == ""
        assert puny_decode("abc-") == "abc"
        assert puny_decode("bcher-kva") == "bücher"
