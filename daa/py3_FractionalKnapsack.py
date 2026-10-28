"""
QUESTION 3 (DAA):
Write a program to solve a fractional Knapsack problem using a greedy method.

HOW IT WORKS (GREEDY STRATEGY):
1. Compute the value/weight ratio of every item ("value per kilogram").
2. Sort items by that ratio in DECREASING order.
3. Walk the sorted list:
   - if the whole item fits in the remaining capacity, take it fully;
   - otherwise take the FRACTION that fits, then stop (knapsack full).
   Taking the best deal first is optimal because any other choice could be
   improved by swapping a worse deal for a better one.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 daa/py3_FractionalKnapsack.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
from collections import namedtuple

# One knapsack item: index, value, weight, and value/weight ratio.
Item = namedtuple("Item", ["index", "value", "weight", "ratio"])


# ============================================================
# STEP 2 : INPUT + GREEDY ALGORITHM FUNCTIONS (no files needed)
# ============================================================
def read_items(n):
    """Read value and weight of each item; store the ratio alongside."""
    items = []
    for i in range(n):
        value = float(input(f"Item {i + 1} value: "))
        weight = float(input(f"Item {i + 1} weight: "))
        items.append(Item(i + 1, value, weight, value / weight))
    return items


def fractional_knapsack(items, capacity):
    """Greedy fill: best-ratio items first, fraction at the end."""
    items = sorted(items, key=lambda item: item.ratio, reverse=True)

    total_value, remaining = 0.0, capacity
    print("\nSelected Items:")
    for item in items:
        if remaining <= 0:
            break
        if item.weight <= remaining:
            remaining -= item.weight                 # take 100%
            total_value += item.value
            print(f"Item {item.index} -> 100% selected")
        else:
            fraction = remaining / item.weight       # take the fraction that fits
            total_value += item.value * fraction
            print(f"Item {item.index} -> {fraction * 100:.2f}% selected")
            remaining = 0
    return total_value


# ============================================================
# STEP 3 : DRIVER - read items + capacity, run greedy, print result
# ============================================================
def run():
    n = int(input("Enter number of items: "))
    items = read_items(n)
    capacity = float(input("Enter knapsack capacity: "))

    total = fractional_knapsack(items, capacity)
    print(f"\nMaximum value = {total:.2f}")


if __name__ == "__main__":
    run()
