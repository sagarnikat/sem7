"""
N-Queens matrix with the first queen fixed at (0, 0), solved by backtracking.

Run with:
    python3 daa/py5_NQueens.py
"""

def is_safe(board, row, column):
    """Check the column and both diagonals against queens placed above."""
    for above in range(row):
        if board[above][column]:
            return False

    above = row - 1
    left = column - 1
    while above >= 0 and left >= 0:
        if board[above][left]:
            return False
        above -= 1
        left -= 1

    above = row - 1
    right = column + 1
    while above >= 0 and right < len(board):
        if board[above][right]:
            return False
        above -= 1
        right += 1

    return True


def place_queens(board, row):
    """Place one queen per row, returning True when the board is solved."""
    size = len(board)
    if row == size:
        return True

    if row == 0:
        return place_queens(board, row + 1)

    for column in range(size):
        if is_safe(board, row, column):
            board[row][column] = 1
            if place_queens(board, row + 1):
                return True
            board[row][column] = 0

    return False


def print_board(board):
    """Print the solution matrix, matching the C++ program's output."""
    print("\nSolution Matrix:")
    for row in board:
        print("".join(f"{cell} " for cell in row))


def run():
    size = int(input("Enter the value of N: "))
    if size < 1:
        print("N must be at least 1.")
        return

    board = [[0] * size for _ in range(size)]
    board[0][0] = 1

    if place_queens(board, 0):
        print_board(board)
    else:
        print("No solution exists with the first queen at (0, 0).")


if __name__ == "__main__":
    run()
