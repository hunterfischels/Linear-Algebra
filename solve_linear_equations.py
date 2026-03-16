"""
Solve a system of linear equations using matrix methods.

System:
  2x -  y = 0
  -x + 2y = 3

Matrix form: Ax = b
  A = [[ 2, -1],
       [-1,  2]]
  b = [0, 3]
"""


def solve(A, b):
    """Solve a 2x2 system Ax = b using Cramer's rule."""
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if det == 0:
        raise ValueError("System has no unique solution (determinant is zero).")
    x = (b[0] * A[1][1] - b[1] * A[0][1]) / det
    y = (A[0][0] * b[1] - A[1][0] * b[0]) / det
    return x, y


if __name__ == "__main__":
    A = [[2, -1],
         [-1, 2]]
    b = [0, 3]

    x, y = solve(A, b)
    print(f"Solution: x = {x}, y = {y}")
