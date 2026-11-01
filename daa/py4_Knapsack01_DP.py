"""
QUESTION 4 (DAA):
Write a program to solve a 0-1 Knapsack problem using dynamic programming
(or branch and bound strategy).

HOW IT WORKS
    dp[i][w] = best value using only the first i items with capacity w.

    For every item and capacity:
        skip item i : dp[i][w] = dp[i-1][w]
        take item i : dp[i][w] = value[i] + dp[i-1][w - weight[i]]
        dp[i][w]     = max(skip, take)   (take only if weight[i] <= w)

    dp[n][capacity] is the answer. To find which items were chosen, walk the
    table backwards: if dp[i][w] differs from dp[i-1][w], item i was taken.

STEPS
    1. Imports
    2. Input items and capacity
    3. Build the DP table
    4. Trace back the chosen items
    5. Run and print the result
    6. Inspect the DP table
    7. Observation

RUN
    python3 daa/py4_Knapsack01_DP.py

    In Jupyter, open py4_Knapsack01_DP.ipynb or split this file at the
    "# %%" markers.
"""

# %% Step 1: Imports
from collections import namedtuple

# %% Step 2: Input items and capacity
# Each item is (index, value, weight). Change the list or the capacity and
# re-run this cell plus the steps below it.
Item = namedtuple("Item", ["index", "value", "weight"])

items = [
    Item(1, 60, 10),
    Item(2, 100, 20),
    Item(3, 120, 30),
]
capacity = 50

for item in items:
    print(f"Item {item.index}: value={item.value}, weight={item.weight}")
print("Capacity:", capacity)

# %% Step 3: Build the DP table
def knapsack_dp(items, capacity):
    """Fill the DP table; return (dp table, maximum value)."""
    dp = [[0] * (capacity + 1) for _ in range(len(items) + 1)]

    for i, item in enumerate(items, start=1):
        for w in range(capacity + 1):
            if item.weight <= w:
                take = item.value + dp[i - 1][w - item.weight]
                skip = dp[i - 1][w]
                dp[i][w] = max(take, skip)
            else:
                dp[i][w] = dp[i - 1][w]
    return dp, dp[len(items)][capacity]

# %% Step 4: Trace back the chosen items
def selected_items(items, dp, capacity):
    """Walk the table backwards and collect the item indices chosen."""
    chosen, w = [], capacity
    for i in range(len(items), 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(items[i - 1])
            w -= items[i - 1].weight
    return chosen

# %% Step 5: Run and print the result
dp, best = knapsack_dp(items, capacity)

print(f"\nMaximum value = {best}")
print("Selected items:")
for item in selected_items(items, dp, capacity):
    print(f"  Item {item.index} (value={item.value}, weight={item.weight})")

# %% Step 6: Inspect the DP table
# Rows are items (row 0 = no items), columns are capacities from 0 to 50.
print("\nDP table (rows = items, columns = capacity):")
for row in dp:
    print(row)

# %% Step 7: Observation
print("\nObservation")
print("  Each cell stores the best value for that item prefix and capacity.")
print("  The final cell is the answer, and the trace-back finds the items.")
