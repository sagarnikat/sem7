"""
QUESTION 1 (DAA):
Write a non-recursive and recursive program to calculate Fibonacci numbers
and analyze their time and space complexity.

HOW IT WORKS
    F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2).

    Recursive version: direct translation of the formula. It recomputes the
    same subproblems, so the time is about O(2^n) and the space is O(n) for
    the call stack.

    Iterative version: keep only the last two values and slide the window
    forward. Every term is computed once, so the time is O(n) and the space
    is O(1).

STEPS
    1. Imports
    2. Input value
    3. Recursive version
    4. Iterative version
    5. Run both versions and measure time
    6. Complexity analysis
    7. Observation

RUN
    python3 daa/py1_Fibonacci.py

    In Jupyter, open py1_Fibonacci.ipynb or split this file at the "# %%"
    markers. Each block is one cell and runs in order.
"""

# %% Step 1: Imports
import time

# %% Step 2: Input value
# Change n and re-run this cell plus the steps below it. Use 30 or 35 to see
# the recursive version slow down.
n = 25

# %% Step 3: Recursive version
def fibonacci_recursive(n):
    """Naive recursion straight from the definition: exponential time."""
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# %% Step 4: Iterative version
def fibonacci_iterative(n):
    """Loop version: O(n) time, O(1) space, each term computed once."""
    if n <= 1:
        return n
    previous, current = 0, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current

# %% Step 5: Run both versions and measure time
start = time.perf_counter()
result_iterative = fibonacci_iterative(n)
time_iterative = time.perf_counter() - start

start = time.perf_counter()
result_recursive = fibonacci_recursive(n)
time_recursive = time.perf_counter() - start

print(f"Iterative : F({n}) = {result_iterative}  ({time_iterative:.6f} s)")
print(f"Recursive : F({n}) = {result_recursive}  ({time_recursive:.6f} s)")

if time_iterative > 0:
    ratio = time_recursive / time_iterative
    print(f"Recursive / iterative time ratio: {ratio:,.0f}x")

# %% Step 6: Complexity analysis
print("\nComplexity analysis")
print("  Iterative -> time O(n), space O(1)")
print("  Recursive -> time ~O(2^n), space O(n) call stack")

# %% Step 7: Observation
print("\nObservation")
print("  The iterative result becomes instant as n grows, while the recursive")
print("  result slows down exponentially because the same subproblems are")
print("  solved again and again.")
