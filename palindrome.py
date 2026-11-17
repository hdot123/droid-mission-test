def is_palindrome(s):
    """Return True if s is a palindrome, comparing only English letters
    and digits while ignoring case and all other characters."""
    filtered = [c.lower() for c in s if c.isalnum()]
    return filtered == filtered[::-1]
