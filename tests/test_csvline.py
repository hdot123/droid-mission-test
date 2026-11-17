import csvline


def test_parse_example():
    assert csvline.parse('a,"b,c","d""e"') == ["a", "b,c", 'd"e']


def test_parse_simple_unquoted():
    assert csvline.parse("a,b,c") == ["a", "b", "c"]
    assert csvline.parse("") == [""]
    assert csvline.parse("only") == ["only"]


def test_parse_quoted_comma():
    assert csvline.parse('"hello, world",x') == ["hello, world", "x"]


def test_parse_doubled_quote_decoding():
    assert csvline.parse('"d""e"') == ['d"e']
    assert csvline.parse('""""') == ['"']
    assert csvline.parse('a,"""",b') == ["a", '"', "b"]


def test_parse_quoted_field_with_doubled_quote_and_comma():
    assert csvline.parse('"say ""hi"", now",next') == ['say "hi", now', "next"]


def test_join_quotes_comma():
    assert csvline.join(["a", "b,c"]) == 'a,"b,c"'


def test_join_quotes_double_quote():
    assert csvline.join(['d"e']) == '"d""e"'


def test_join_quotes_newline():
    assert csvline.join(["line1\nline2"]) == '"line1\nline2"'


def test_join_bare_fields():
    assert csvline.join(["a", "b", "c"]) == "a,b,c"


def test_join_empty_fields():
    assert csvline.join([]) == ""
    assert csvline.join(["", ""]) == ","


def test_roundtrip():
    cases = [
        ["a", "b,c", 'd"e'],
        ["x"],
        [""],
        ["", "empty"],
        ["has\nnewline", "plain"],
        ['quote "" doubled', "trail,"],
        ["中文", "unicodé"],
    ]
    for fields in cases:
        assert csvline.parse(csvline.join(fields)) == fields
