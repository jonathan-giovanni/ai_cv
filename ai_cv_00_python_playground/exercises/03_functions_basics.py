# 03_functions_basics.py

# This file introduces:
# - defining functions
# - parameters
# - return values
# - default values
# - keyword-only arguments
# - lambda
# - mutable vs immutable behavior in functions

from typing import Callable

def add(a: float, b: float) -> float:
    """Add two integers."""
    return a + b

def normalize_score(score: float, *,max_score: float = 1.0) -> float:
    """Normalize a score to the range [0, 1]."""
    if max_score <= 0:
        raise ValueError("max_score must be greater than 0")
    return score / max_score

def apply_to_values(values: list[float], operation: Callable[[float], float]) -> list[float]:
    """Apply a function to a list of values."""
    return [operation(value) for value in values]

def reassign_immutable(x: int) -> None:
    """Demonstrate that reassigning an immutable variable does not affect the caller."""
    x = 999  # This does not change the original variable passed to the function
    print("x:", x)

def main() -> None:
    # Basic function usage
    result = add(3.5, 2.5)
    print("Add Result:", result)

    # Using default and keyword-only arguments
    normalized = normalize_score(0.85)
    print("Normalized Score (default max):", normalized)

    normalized_custom = normalize_score(85, max_score=100)
    print("Normalized Score (custom max):", normalized_custom)

    # Using a lambda function to apply an operation
    values = [1, 2, 3, 4, 5]
    squared_values = apply_to_values(values, lambda x: x ** 2)
    print("Squared Values:", squared_values)

    # Demonstrating mutable vs immutable behavior
    original_value = 10
    reassign_immutable(original_value)
    print("Original Value after function call:", original_value)

if __name__ == "__main__":
    main()