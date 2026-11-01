"""
QUESTION 6 (DAA):
Write a recursive program to solve the Tower of Hanoi problem.

HOW IT WORKS
    Three pegs: A (source), B (auxiliary), C (destination). Move n disks from
    A to C so that only the top disk moves at a time and a larger disk never
    rests on a smaller one.

    To move n disks from source to destination:
        1. move the top n-1 disks from source to auxiliary (using destination),
        2. move the largest disk from source to destination,
        3. move the n-1 disks from auxiliary to destination (using source).

    Base case: n = 1 is a single direct move. The peg names rotate in every
    recursive call, so the function takes them as arguments instead of
    hard-coding A, B and C.

COMPLEXITY
    Recurrence : T(n) = 2 * T(n - 1) + 1, with T(1) = 1
    Moves      : T(n) = 2^n - 1
    Time       : O(2^n) - the output alone has 2^n - 1 lines
    Space      : O(n)   - one stack frame per disk

STEPS
    1. Move list container
    2. Input number of disks
    3. Recursive algorithm
    4. Print the moves for n disks
    5. Show the peg state after every move
    6. Compare the move count with 2^n - 1
    7. Observation

RUN
    python3 daa/py6_TowerOfHanoi.py

    In Jupyter, open py6_TowerOfHanoi.ipynb or split this file at the
    "# %%" markers. This practical needs no imports.
"""

# %% Step 1: Move list container
# Every solved move is stored as (disk, from_peg, to_peg) so the recursion can
# be printed afterwards without mixing printing into the algorithm.
MOVE_LOG = []

# %% Step 2: Input number of disks
# Change n and re-run this cell plus the steps below it. Try 3 first: it gives
# the classic 7-move solution. Above ~20 the output becomes very long.
disks = 3

# %% Step 3: Recursive algorithm
def tower_of_hanoi(n, source="A", auxiliary="B", destination="C", moves=None):
    """Move n disks source -> destination via auxiliary; return the move list."""
    if moves is None:
        moves = []

    if n == 1:
        moves.append((1, source, destination))
        return moves

    tower_of_hanoi(n - 1, source, destination, auxiliary, moves)
    moves.append((n, source, destination))
    tower_of_hanoi(n - 1, auxiliary, source, destination, moves)
    return moves

# %% Step 4: Print the moves for n disks
solution = tower_of_hanoi(disks)

print(f"Moving {disks} disks from A to C")
print()
for number, (disk, source, destination) in enumerate(solution, start=1):
    print(f"{number:>3}. Move disk {disk} from {source} to {destination}")

print(f"\nTotal moves = {len(solution)}  (= 2^{disks} - 1 = {2 ** disks - 1})")

# %% Step 5: Show the peg state after every move
# The bottom of each list is the largest disk, just like a real peg.
def show_trace(n):
    """Replay the solution and print the three pegs after each move."""
    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    print(f"\nStart   A: {pegs['A']}  B: {pegs['B']}  C: {pegs['C']}")

    for step, (disk, source, destination) in enumerate(
            tower_of_hanoi(n), start=1):
        pegs[destination].append(pegs[source].pop())
        print(f"{step:>3}. disk {disk}: {source} -> {destination}   "
              f"A: {pegs['A']}  B: {pegs['B']}  C: {pegs['C']}")


show_trace(disks)

# %% Step 6: Compare the move count with 2^n - 1
print(f"\n{'disks':>5} {'moves':>8} {'2^n - 1':>8} {'match':>7}")
for n in range(1, 16):
    counted = len(tower_of_hanoi(n))
    expected = 2 ** n - 1
    print(f"{n:>5} {counted:>8,} {expected:>8,} {str(counted == expected):>7}")

# %% Step 7: Observation
print("\nObservation")
print("  The number of moves doubles plus one for every extra disk, so the")
print("  count is exactly 2^n - 1. The recursion only needs n stack frames,")
print("  which is why the space complexity is O(n) even though the time is")
print("  exponential.")
