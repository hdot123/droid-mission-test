"""Singly linked list implementation (standard library only)."""


class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class SinglyLinkedList:
    """A singly linked list. Elements may be of any type; equality uses ==."""

    def __init__(self, values=None):
        self._head = None
        self._tail = None
        self._size = 0
        if values is not None:
            for value in values:
                self.append(value)

    def __len__(self):
        return self._size

    def to_list(self):
        result = []
        node = self._head
        while node is not None:
            result.append(node.value)
            node = node.next
        return result

    def append(self, value):
        node = _Node(value)
        if self._tail is None:
            self._head = node
            self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, value):
        self._head = _Node(value, self._head)
        if self._tail is None:
            self._tail = self._head
        self._size += 1

    @staticmethod
    def _validate_index(index, length):
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError(f"index must be an integer, not {type(index).__name__}")
        if index < 0 or index >= length:
            raise IndexError(f"index {index} out of range for list of length {length}")

    def get(self, index):
        self._validate_index(index, self._size)
        node = self._head
        for _ in range(index):
            node = node.next
        return node.value

    def find(self, value):
        index = 0
        node = self._head
        while node is not None:
            if node.value == value:
                return index
            node = node.next
            index += 1
        return -1

    def remove(self, value):
        prev = None
        node = self._head
        while node is not None:
            if node.value == value:
                if prev is None:
                    self._head = node.next
                else:
                    prev.next = node.next
                if self._tail is node:
                    self._tail = prev
                self._size -= 1
                return True
            prev = node
            node = node.next
        return False

    def remove_at(self, index):
        self._validate_index(index, self._size)
        prev = None
        node = self._head
        for _ in range(index):
            prev = node
            node = node.next
        if prev is None:
            self._head = node.next
        else:
            prev.next = node.next
        if self._tail is node:
            self._tail = prev
        self._size -= 1
        return node.value

    def reverse(self):
        prev = None
        node = self._head
        self._tail = self._head
        while node is not None:
            nxt = node.next
            node.next = prev
            prev = node
            node = nxt
        self._head = prev

    def clear(self):
        self._head = None
        self._tail = None
        self._size = 0
