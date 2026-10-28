"""
QUESTION 1 (DAA):
Write a non-recursive and recursive program to calculate Fibonacci numbers
and analyze their time and space complexity.

HOW IT WORKS:
- The Fibonacci sequence: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).
- RECURSIVE version : direct translation of the formula. Beautiful but
  exponential - the call tree recomputes the same subproblems (~1.618^n
  calls), so time ~O(2^n), space O(n) (call stack).
- ITERATIVE version : keep only the last two values and slide a window
  forward. Time O(n), space O(1).
- COMPARISON (the analysis part of the question):
      version    time      space    note
      recursive  O(2^n)    O(n)     recomputes subproblems (no memo)
      iterative  O(n)      O(1)     each F(k) computed exactly once
- Try n = 40: iterative is instant, recursive visibly pauses. That pause
  IS the practical proof of exponential vs linear complexity.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 daa/py1_Fibonacci.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import time          # only for the timing comparison in the analysis


# ============================================================
# STEP 2 : ALGORITHM FUNCTIONS (no files/datasets needed)
# ============================================================
def fibonacci_recursive(n):
    """Naive recursion straight from the definition. Exponential time."""
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n):
    """Loop version: O(n) time, O(1) space, each term computed once."""
    if n <= 1:
        return n
    previous, current = 0, 1          # F(i-2) and F(i-1)
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current


# ============================================================
# STEP 3 : DRIVER - ask n, run both versions, print the analysis
# ============================================================
def run():
    n = int(input("Enter n (use <= 35 for the recursive version): "))

    start = time.perf_counter()                       # time the iterative one
    result_iterative = fibonacci_iterative(n)
    time_iterative = time.perf_counter() - start

    start = time.perf_counter()                       # time the recursive one
    result_recursive = fibonacci_recursive(n)
    time_recursive = time.perf_counter() - start

    print(f"\nIterative : F({n}) = {result_iterative}  ({time_iterative:.6f} s)")
    print(f"Recursive : F({n}) = {result_recursive}  ({time_recursive:.6f} s)")
    print("\nComplexity analysis:")
    print("  Iterative -> time O(n), space O(1)")
    print("  Recursive -> time ~O(2^n), space O(n) call stack")


if __name__ == "__main__":
    run()
