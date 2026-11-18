"""A simple Last-In-First-Out (LIFO) stack."""


class Stack:
    """A stack backed by a list, with LIFO ordering."""

    def __init__(self):
        self._items = []

    def push(self, x):
        """Push an element onto the stack."""
        self._items.append(x)

    def pop(self):
        """Pop and return the top element; raise IndexError if empty."""
        if not self._items:
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top element without removing it; raise IndexError if empty."""
        if not self._items:
            raise IndexError("peek from an empty stack")
        return self._items[-1]

    def is_empty(self):
        """Return True if the stack has no elements."""
        return not self._items

    def size(self):
        """Return the number of elements in the stack."""
        return len(self._items)
