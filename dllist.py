"""dllist: 双向链表工具模块。

实现 `DoublyLinkedList`：元素以值相等（`==`）比较，支持头尾追加、
按值删除首个匹配元素、头尾弹出，以及正序/逆序导出列表。
"""


class _Node:
    __slots__ = ("value", "prev", "next")

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """双向链表，元素按值相等（==）比较。"""

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def append(self, value):
        """在尾部追加一个元素。"""
        node = _Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, value):
        """在头部追加一个元素。"""
        node = _Node(value)
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._size += 1

    def __len__(self):
        """返回元素个数。"""
        return self._size

    def to_list(self):
        """返回从头到尾的值列表。"""
        values = []
        node = self._head
        while node is not None:
            values.append(node.value)
            node = node.next
        return values

    def to_list_reversed(self):
        """返回从尾到头的值列表。"""
        values = []
        node = self._tail
        while node is not None:
            values.append(node.value)
            node = node.prev
        return values

    def remove_first(self, value):
        """删除第一个与 value 相等的元素；删除成功返回 True，不存在返回 False。"""
        node = self._head
        while node is not None:
            if node.value == value:
                self._unlink(node)
                return True
            node = node.next
        return False

    def pop_front(self):
        """移除并返回头元素；链表为空时抛 IndexError。"""
        if self._head is None:
            raise IndexError("pop from empty DoublyLinkedList")
        node = self._head
        self._unlink(node)
        return node.value

    def pop_back(self):
        """移除并返回尾元素；链表为空时抛 IndexError。"""
        if self._tail is None:
            raise IndexError("pop from empty DoublyLinkedList")
        node = self._tail
        self._unlink(node)
        return node.value

    def _unlink(self, node):
        prev_node = node.prev
        next_node = node.next
        if prev_node is None:
            self._head = next_node
        else:
            prev_node.next = next_node
        if next_node is None:
            self._tail = prev_node
        else:
            next_node.prev = prev_node
        node.prev = None
        node.next = None
        self._size -= 1
