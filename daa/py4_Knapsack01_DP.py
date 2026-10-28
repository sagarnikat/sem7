"""
QUESTION 4 (DAA):
Write a program to solve a 0-1 Knapsack problem using dynamic programming
(or branch and bound strategy).

HOW IT WORKS (BOTTOM-UP DYNAMIC PROGRAMMING):
1. dp[i][w] = best value using only the first i items with capacity w.
2. Recurrence for each item i and capacity w:
       skip item i  : dp[i][w] = dp[i-1][w]
       take item i  : dp[i][w] = value[i] + dp[i-1][w - weight[i]]
       dp[i][w]     = max(skip, take)     (take only if weight[i] <= w)
3. dp[n][W] is the answer.
4. TRACE-BACK for which items were chosen: walking backwards, if
   dp[i][w] != dp[i-1][w] then item i was taken - subtract its weight and
   continue from dp[i-1][w - weight[i]].

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 daa/py4_Knapsack01_DP.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
from collections import namedtuple

# One knapsack item (0/1: an item is taken fully or not at all).
Item = namedtuple("Item", ["index", "value", "weight"])


# ============================================================
# STEP 2 : INPUT + DYNAMIC PROGRAMMING FUNCTIONS (no files needed)
# ============================================================
def read_items(n):
    """Read value and weight of each of the n items (integers)."""
    items = []
    for i in range(n):
        value = int(input(f"Item {i + 1} value: "))
        weight = int(input(f"Item {i + 1} weight: "))
        items.append(Item(i + 1, value, weight))
    return items


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
                dp[i][w] = dp[i - 1][w]   # item too heavy for this capacity
    return dp, dp[len(items)][capacity]


def selected_items(items, dp, capacity):
    """Walk the table backwards and collect the item indices chosen."""
    chosen, w = [], capacity
    for i in range(len(items), 0, -1):
        if dp[i][w] != dp[i - 1][w]:      # value changed => item i was taken
            chosen.append(items[i - 1])
            w -= items[i - 1].weight
    return chosen


# ============================================================
# STEP 3 : DRIVER - read input, run DP, print value + chosen items
# ============================================================
def run():
    n = int(input("Enter number of items: "))
    items = read_items(n)
    capacity = int(input("Enter knapsack capacity: "))

    dp, best = knapsack_dp(items, capacity)

    print(f"\nMaximum value = {best}")
    print("Selected items:")
    for item in selected_items(items, dp, capacity):
        print(f"  Item {item.index} (value={item.value}, weight={item.weight})")


if __name__ == "__main__":
    run()
