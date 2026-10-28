"""
QUESTION 6 (DAA):
Write a recursive program to solve the Tower of Hanoi problem.

HOW IT WORKS (DIVIDE AND CONQUER / RECURSION):
Three pegs A (source), B (auxiliary), C (destination). Move n disks from
A to C so that only the top disk moves at a time and a large disk never
sits on a smaller one. To move n disks:
    step 1: move the top n-1 disks A -> B  (using C)   [uncover the largest]
    step 2: move the largest disk      A -> C  [direct move]
    step 3: move those n-1 disks       B -> C  (using A)  [rebuild on top]
Base case: n == 1 -> a single direct move.
Number of moves T(n) = 2*T(n-1) + 1  =>  T(n) = 2^n - 1.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 daa/py6_TowerOfHanoi.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
# none - this program needs only the standard built-ins


# ============================================================
# STEP 2 : RECURSIVE ALGORITHM
# ============================================================
MOVE_LOG = []   # collected "Move disk k from X to Y" strings


def tower_of_hanoi(n, source, auxiliary, destination):
    """Move n disks source -> destination using auxiliary (recursive)."""
    if n == 1:                                        # base case
        MOVE_LOG.append(f"Move disk 1 from {source} to {destination}")
        return
    tower_of_hanoi(n - 1, source, destination, auxiliary)   # step 1
    MOVE_LOG.append(f"Move disk {n} from {source} to {destination}")  # step 2
    tower_of_hanoi(n - 1, auxiliary, source, destination)   # step 3


# ============================================================
# STEP 3 : DRIVER - read n, run recursion, print moves + count
# ============================================================
def run():
    n = int(input("Enter number of disks: "))
    if n < 1:
        print("Number of disks must be at least 1.")
        return

    tower_of_hanoi(n, "A", "B", "C")

    for line in MOVE_LOG:
        print(line)
    print(f"\nTotal moves = {len(MOVE_LOG)}  (= 2^{n} - 1)")


if __name__ == "__main__":
    run()
