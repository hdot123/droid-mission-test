import pytest

from trie import Trie


def make_trie():
    t = Trie()
    for w in ("apple", "app", "application", "banana", "band", "bandana", "cat"):
        t.insert(w)
    return t


def test_search_hits():
    t = make_trie()
    assert t.search("app") is True
    assert t.search("banana") is True
    assert t.search("cat") is True


def test_search_misses():
    t = make_trie()
    assert t.search("appl") is False
    assert t.search("ban") is False
    assert t.search("dog") is False


def test_starts_with():
    t = make_trie()
    assert t.starts_with("app") is True
    assert t.starts_with("ban") is True
    assert t.starts_with("dog") is False


def test_count_prefix():
    t = make_trie()
    assert t.count_prefix("app") == 3
    assert t.count_prefix("ban") == 3
    assert t.count_prefix("band") == 2
    assert t.count_prefix("c") == 1
    assert t.count_prefix("z") == 0


def test_words_with_prefix():
    t = make_trie()
    assert t.words_with_prefix("app") == ["app", "apple", "application"]
    assert t.words_with_prefix("ban") == ["banana", "band", "bandana"]
    assert t.words_with_prefix("z") == []


def test_duplicate_insert_idempotent():
    t = make_trie()
    t.insert("app")
    assert t.count_prefix("app") == 3
    assert t.search("app") is True
    assert t.words_with_prefix("app") == ["app", "apple", "application"]


@pytest.mark.parametrize("method", ["insert", "search", "starts_with", "count_prefix", "words_with_prefix"])
def test_empty_string_raises(method):
    t = Trie()
    with pytest.raises(ValueError):
        getattr(t, method)("")


@pytest.mark.parametrize("method", ["insert", "search", "starts_with", "count_prefix", "words_with_prefix"])
def test_non_str_raises(method):
    t = Trie()
    with pytest.raises(TypeError):
        getattr(t, method)(123)
