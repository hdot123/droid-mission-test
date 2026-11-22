"""Stack class and reverse-Polish (RPN) expression evaluation."""

_OPERATORS = {"+", "-", "*", "/"}


class Stack:
    """A simple last-in-first-out stack."""

    def __init__(self):
        self._items = []

    def push(self, x):
        """Push x onto the top of the stack."""
        self._items.append(x)

    def pop(self):
        """Remove and return the top item; raise IndexError if empty."""
        if not self._items:
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it; raise IndexError if empty."""
        if not self._items:
            raise IndexError("peek from an empty stack")
        return self._items[-1]

    def is_empty(self):
        """Return True when the stack has no items."""
        return not self._items

    def __len__(self):
        return len(self._items)


def eval_rpn(tokens):
    """Evaluate a reverse-Polish expression given as a list of strings.

    Each token is an integer string or one of the operators "+-*/".
    Division truncates toward zero. Results are ints.

    Raises:
        ValueError: empty tokens, a non-integer/non-operator token, or an
            invalid expression (not enough operands, or leftover operands).
        ZeroDivisionError: division by zero.
    """
    if not tokens:
        raise ValueError("empty expression")

    stack = Stack()
    for token in tokens:
        if token in _OPERATORS:
            if len(stack) < 2:
                raise ValueError("not enough operands for operator %r" % token)
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.push(a + b)
            elif token == "-":
                stack.push(a - b)
            elif token == "*":
                stack.push(a * b)
            else:  # "/"
                if b == 0:
                    raise ZeroDivisionError("division by zero")
                # Truncate toward zero (// floors toward negative infinity).
                stack.push(int(a / b))
        else:
            try:
                value = int(token)
            except (TypeError, ValueError):
                raise ValueError("invalid token %r" % (token,))
            stack.push(value)

    if len(stack) != 1:
        raise ValueError("invalid expression: leftover operands")

    return stack.pop()
