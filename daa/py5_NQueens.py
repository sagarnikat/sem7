"""
QUESTION 5 (DAA):
Design an n-Queens matrix having the first Queen placed. Use backtracking
to place the remaining Queens and generate the final n-queen's matrix.

HOW IT WORKS (BACKTRACKING):
1. Place queens one ROW at a time - each row must hold exactly one queen.
2. The FIRST queen is permanently fixed at square (0, 0) (the question's
   constraint). For some N that makes the puzzle unsolvable even when
   solutions exist with the first queen elsewhere (e.g. N = 6).
3. For every other row, try each column: keep it only if no queen above
   shares the column, the "\\" diagonal or the "/" diagonal.
4. Recurse to the next row; if a later row fails everywhere, REMOVE the
   queen (backtrack) and try the next column in this row.
5. Solved when all N rows hold queens.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 daa/py5_NQueens.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
# none - this program needs only the standard built-ins


# ============================================================
# STEP 2 : BACKTRACKING ALGORITHM (board held in module globals)
# ============================================================
N = 0                       # board size, set by run()
QUEENS = []                 # QUEENS[row] = column of the queen in that row


def is_safe(row, column):
    """Check the column and both diagonals against queens placed above."""
    for above in range(row):
        same_column = QUEENS[above] == column
        same_slash = above + QUEENS[above] == row + column       # "/" diagonal
        same_backslash = above - QUEENS[above] == row - column   # "\" diagonal
        if same_column or same_slash or same_backslash:
            return False
    return True


def place_queens(row):
    """Try to place a queen in every row from `row` onward; True = solved."""
    if row == N:
        return True                       # all rows have a queen
    if row == 0:                          # first queen fixed at (0, 0)
        return place_queens(row + 1)

    for column in range(N):
        if is_safe(row, column):
            QUEENS[row] = column          # place (choose)
            if place_queens(row + 1):     # explore
                return True
            QUEENS[row] = -1              # remove (backtrack)
    return False                          # exhausted this row -> fail upward


def print_board():
    """Print the solution matrix; 1 = queen, 0 = empty square."""
    print("\nSolution Matrix:")
    for row in range(N):
        line = " ".join("1" if QUEENS[row] == column else "0"
                        for column in range(N))
        print(line)


# ============================================================
# STEP 3 : DRIVER - read N, fix first queen, backtrack, print
# ============================================================
def run():
    global N
    N = int(input("Enter the value of N: "))
    if N < 1:
        print("N must be at least 1.")
        return

    QUEENS[:] = [-1] * N
    QUEENS[0] = 0                         # queen fixed at top-left

    if place_queens(0):
        print_board()
    else:
        print("No solution exists with the first queen at (0, 0).")


if __name__ == "__main__":
    run()
