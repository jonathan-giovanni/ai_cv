# 07_matrix_basics.py

# This file introduces:
# - representing a matrix with nested lists
# - matrix shape
# - transpose
# - scalar multiplication
# - matrix addition

from typing import TypeAlias

Matrix: TypeAlias = list[list[float]]  # A matrix is a list of lists of floats

def matrix_shape(matrix: Matrix) -> tuple[int, int]:
    """Return the shape of a matrix as (rows, columns)."""
    if not matrix:
        return 0, 0  # Handle empty matrix case
    return len(matrix), len(matrix[0])

def transpose(matrix: Matrix) -> Matrix:
    rows, cols = matrix_shape(matrix)

    result: Matrix = []

    for col_index in range(cols):
        new_row: list[float] = []

        for row_index in range(rows):
            new_row.append(matrix[row_index][col_index])

        result.append(new_row)

    return result

def scalar_multiply(matrix: Matrix, scalar: float) -> Matrix:
    rows, cols = matrix_shape(matrix)

    result: Matrix = []

    for row_index in range(rows):
        new_row: list[float] = []

        for col_index in range(cols):
            new_row.append(matrix[row_index][col_index] * scalar)

        result.append(new_row)

    return result

def matrix_addition(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
    rows_a, cols_a = matrix_shape(matrix_a)
    rows_b, cols_b = matrix_shape(matrix_b)

    if (rows_a, cols_a) != (rows_b, cols_b):
        raise ValueError("Matrices must have the same shape for addition")

    result: Matrix = []

    for row_index in range(rows_a):
        new_row: list[float] = []

        for col_index in range(cols_a):
            new_row.append(matrix_a[row_index][col_index] + matrix_b[row_index][col_index])

        result.append(new_row)

    return result

def main() -> None:
    matrix_a: Matrix = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0]
    ]

    matrix_b: Matrix = [
        [7.0, 8.0, 9.0],
        [10.0, 11.0, 12.0]
    ]

    print("Matrix A:", matrix_a)
    print("Matrix B:", matrix_b)

    print("Shape of Matrix A:", matrix_shape(matrix_a))
    print("Shape of Matrix B:", matrix_shape(matrix_b))

    print("Transpose of Matrix A:", transpose(matrix_a))
    print("Transpose of Matrix B:", transpose(matrix_b))

    scalar = 2.0
    print(f"Matrix A multiplied by scalar {scalar}:", scalar_multiply(matrix_a, scalar))
    print(f"Matrix B multiplied by scalar {scalar}:", scalar_multiply(matrix_b, scalar))

    print("Matrix A + Matrix B:", matrix_addition(matrix_a, matrix_b))

if __name__ == "__main__":
    main()