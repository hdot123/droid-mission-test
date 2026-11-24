"""Prefix tree (trie) with word counting and lexicographic listing."""


class _Node:
    __slots__ = ("children", "is_word")

    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    """A trie supporting insert, exact/prefix lookup, counting, and listing.

    Duplicate inserts are idempotent: inserting the same word twice does not
    change any counts. All public methods reject empty strings (ValueError)
    and non-str inputs (TypeError).
    """

    def __init__(self):
        self._root = _Node()

    @staticmethod
    def _check(value):
        if not isinstance(value, str):
            raise TypeError("expected str, got " + type(value).__name__)
        if value == "":
            raise ValueError("string must not be empty")

    def insert(self, word):
        self._check(word)
        node = self._root
        for ch in word:
            node = node.children.setdefault(ch, _Node())
        node.is_word = True

    def search(self, word):
        self._check(word)
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix):
        self._check(prefix)
        return self._walk(prefix) is not None

    def count_prefix(self, prefix):
        self._check(prefix)
        node = self._walk(prefix)
        if node is None:
            return 0
        return self._collect(node)[0]

    def words_with_prefix(self, prefix):
        self._check(prefix)
        node = self._walk(prefix)
        if node is None:
            return []
        return [prefix + w for w in self._collect(node)[1]]

    def _walk(self, prefix):
        node = self._root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    @classmethod
    def _collect(cls, node):
        count = 0
        words = []

        def visit(n, path):
            nonlocal count
            if n.is_word:
                count += 1
                words.append("".join(path))
            for ch in sorted(n.children):
                visit(n.children[ch], path + [ch])

        visit(node, [])
        return count, sorted(words)
