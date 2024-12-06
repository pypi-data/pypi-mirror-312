def add(a, b):
    "Adds a and b."
    return a + b


def subtract(a, b):
    """Subtracts b from a."""
    return a - b


def multiply(a, b):
    """Multiplies a and b."""
    return a * b


def divide(a, b):
    """Divides a by b. Checks for division by zero."""
    if b == 0:
        raise ZeroDivisionError("Error: cannot divide by zero!")
    return a / b
