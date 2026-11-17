"""FizzBuzz sequence generation."""


def generate(n):
    """Return the FizzBuzz sequence for numbers 1 to n as a list of strings.

    Multiples of 3 become "Fizz", multiples of 5 become "Buzz", multiples of
    both (i.e. 15) become "FizzBuzz", and everything else becomes the decimal
    string of the number. For n < 1, return an empty list.
    """
    result = []
    for i in range(1, int(n) + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result
