"""
QUESTION 5 (DAA):
Design an n-Queens matrix having the first Queen placed. Use backtracking
to place the remaining Queens and generate the final n-queen's matrix.

HOW IT WORKS
    1. Place queens one row at a time; each row holds exactly one queen.
    2. The first queen is fixed at (0, 0), as the question requires.
    3. For every other row, try each column and keep it only if no queen
       above shares the column or either diagonal.
    4. Recurse to the next row. If a later row fails everywhere, remove the
       current queen (backtrack) and try the next column.
    5. Solved when all N rows hold a queen.

    With the first queen fixed at (0, 0), some sizes have no solution even
    though a solution exists when the first queen may move (for example N=6).

STEPS
    1. Board variables
    2. Safety check
    3. Backtracking search
    4. Print the matrix
    5. Solve for N = 4
    6. Try several board sizes
    7. Observation

RUN
    python3 daa/py5_NQueens.py

    In Jupyter, open py5_NQueens.ipynb or split this file at the "# %%"
    markers. This practical needs no imports.
"""

# %% Step 1: Board variables
N = 4
QUEENS = []

# %% Step 2: Safety check
def is_safe(row, column):
    """Check the column and both diagonals against queens placed above."""
    for above in range(row):
        same_column = QUEENS[above] == column
        same_slash = above + QUEENS[above] == row + column
        same_backslash = above - QUEENS[above] == row - column
        if same_column or same_slash or same_backslash:
            return False
    return True

# %% Step 3: Backtracking search
def place_queens(row):
    """Try to place a queen in every row from row onward; True = solved."""
    if row == N:
        return True
    if row == 0:
        return place_queens(row + 1)

    for column in range(N):
        if is_safe(row, column):
            QUEENS[row] = column
            if place_queens(row + 1):
                return True
            QUEENS[row] = -1
    return False

# %% Step 4: Print the matrix
def print_board():
    """Print the solution matrix; 1 = queen, 0 = empty square."""
    print("\nSolution Matrix:")
    for row in range(N):
        line = " ".join("1" if QUEENS[row] == column else "0"
                        for column in range(N))
        print(line)

# %% Step 5: Solve for N = 4
QUEENS[:] = [-1] * N
QUEENS[0] = 0

if place_queens(0):
    print_board()
else:
    print("No solution exists with the first queen at (0, 0).")

# %% Step 6: Try several board sizes
for size in range(1, 9):
    N = size
    QUEENS[:] = [-1] * N
    QUEENS[0] = 0
    solved = place_queens(0)
    result = "solution found" if solved else "no solution with first queen at (0, 0)"
    print(f"N = {N}: {result}")

# %% Step 7: Observation
print("\nObservation")
print("  Fixing the first queen can make the puzzle impossible for some N.")
print("  Backtracking removes a queen as soon as no safe column remains.")
