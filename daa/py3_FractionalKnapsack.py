"""
QUESTION 3 (DAA):
Write a program to solve a fractional Knapsack problem using a greedy method.

HOW IT WORKS
    1. Compute the value/weight ratio of every item.
    2. Sort the items by that ratio in decreasing order.
    3. Take whole items while they fit. When the next item does not fit, take
       the fraction that fills the remaining capacity and stop.

    Taking the best deal first is optimal for the fractional version because
    any solution can be improved by swapping a worse deal for a better one.

STEPS
    1. Imports
    2. Input items and capacity
    3. Greedy algorithm
    4. Run and print the selection
    5. Observation

RUN
    python3 daa/py3_FractionalKnapsack.py

    In Jupyter, open py3_FractionalKnapsack.ipynb or split this file at the
    "# %%" markers.
"""

# %% Step 1: Imports
from collections import namedtuple

# %% Step 2: Input items and capacity
# Each item is (index, value, weight, value/weight). Change the list or the
# capacity and re-run this cell plus the steps below it.
Item = namedtuple("Item", ["index", "value", "weight", "ratio"])

items = [
    Item(1, 60, 10, 60 / 10),
    Item(2, 100, 20, 100 / 20),
    Item(3, 120, 30, 120 / 30),
]
capacity = 50

for item in items:
    print(f"Item {item.index}: value={item.value}, weight={item.weight}, "
          f"ratio={item.ratio:.2f}")
print("Capacity:", capacity)

# %% Step 3: Greedy algorithm
def fractional_knapsack(items, capacity):
    """Greedy fill: best-ratio items first, fraction at the end."""
    items = sorted(items, key=lambda item: item.ratio, reverse=True)

    total_value, remaining = 0.0, capacity
    print("\nSelected Items:")
    for item in items:
        if remaining <= 0:
            break
        if item.weight <= remaining:
            remaining -= item.weight
            total_value += item.value
            print(f"Item {item.index} -> 100% selected")
        else:
            fraction = remaining / item.weight
            total_value += item.value * fraction
            print(f"Item {item.index} -> {fraction * 100:.2f}% selected")
            remaining = 0
    return total_value

# %% Step 4: Run and print the selection
total = fractional_knapsack(items, capacity)
print(f"\nMaximum value = {total:.2f}")

# %% Step 5: Observation
print("\nObservation")
print("  Items with the highest value per unit weight are taken first. Only")
print("  the last item is split, so the knapsack is filled exactly.")
