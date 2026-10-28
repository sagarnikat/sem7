/*
 * PROBLEM STATEMENT : 0/1 Knapsack using Dynamic Programming
 *
 * Given n items (each with a value and a weight) and a knapsack of integer
 * capacity W, choose a SUBSET of items (you can either take an item fully or
 * not at all - no fractions) so that the total value is maximum and the total
 * weight does not exceed W.
 *
 * HOW IT WORKS (BOTTOM-UP DYNAMIC PROGRAMMING):
 *   1. Build a table dp[i][w] = maximum value achievable using only the first
 *      i items and a knapsack capacity of w.
 *   2. Recurrence for every item i and every capacity w:
 *        dp[i][w] = dp[i-1][w]                                (skip item i)
 *        dp[i][w] = max(dp[i][w], value[i] + dp[i-1][w - weight[i]])
 *                                                             (take item i)
 *   3. dp[n][W] is the answer (best value with all items and full capacity).
 *   4. To find WHICH items were chosen, walk the table backwards:
 *      if dp[i][w] != dp[i-1][w], item i was taken; jump to dp[i-1][w-weight[i]].
 *
 * COMPLEXITY:
 *   - Time  : O(n * W)  (pseudo-polynomial; fills the whole table once)
 *   - Space : O(n * W)  (full table kept so the selected items can be traced)
 *
 * NOTES / INFO:
 *   - Greedy does NOT work here (a high-ratio item may block several small
 *     items whose total value is larger), which is why DP is required.
 *   - Weights must be integers because they index the table columns.
 *   - Unlike the plain DP, this version also prints the chosen item numbers.
 */

#include <iostream>
#include <vector>

using namespace std;

// Read all item values and weights from standard input.
void readItems(int itemCount, vector<long long>& value, vector<int>& weight) {
    cout << "Enter value and weight of each item:\n";
    for (int i = 0; i < itemCount; ++i) {
        cout << "Item " << (i + 1) << " value: ";
        cin >> value[i];
        cout << "Item " << (i + 1) << " weight: ";
        cin >> weight[i];
    }
}

// Fill the DP table and return dp[n][capacity] (the maximum value).
long long buildTable(const vector<long long>& value, const vector<int>& weight,
                     vector<vector<long long>>& dp, int itemCount, int capacity) {
    for (int i = 1; i <= itemCount; ++i) {
        for (int w = 0; w <= capacity; ++w) {
            if (weight[i - 1] <= w) {
                // Option A: keep the best without item i.
                long long without = dp[i - 1][w];
                // Option B: take item i (its weight must come out of w first).
                long long with_ = value[i - 1] + dp[i - 1][w - weight[i - 1]];
                dp[i][w] = max(without, with_);
            } else {
                // Item i is too heavy for capacity w: cannot take it.
                dp[i][w] = dp[i - 1][w];
            }
        }
    }
    return dp[itemCount][capacity];
}

// Walk the table backwards and print the indices of the selected items.
void printSelectedItems(const vector<long long>& value, const vector<int>& weight,
                        const vector<vector<long long>>& dp, int itemCount,
                        int capacity) {
    cout << "Selected items:\n";
    int w = capacity;
    for (int i = itemCount; i > 0; --i) {
        // Value changed between row i-1 and row i => item i was taken.
        if (dp[i][w] != dp[i - 1][w]) {
            cout << "Item " << i << " (value=" << value[i - 1]
                 << ", weight=" << weight[i - 1] << ")\n";
            w -= weight[i - 1];  // free the space the item occupied
        }
    }
}

// Drives the whole practical; main() only calls this.
void run() {
    int itemCount;
    cout << "Enter number of items: ";
    cin >> itemCount;

    vector<long long> value(itemCount);
    vector<int> weight(itemCount);
    readItems(itemCount, value, weight);

    int capacity;
    cout << "Enter knapsack capacity: ";
    cin >> capacity;

    // dp[i][w] has n+1 rows (0 items ... n items) and W+1 columns (0 ... W).
    vector<vector<long long>> dp(itemCount + 1,
                                 vector<long long>(capacity + 1, 0));

    long long maxValue = buildTable(value, weight, dp, itemCount, capacity);

    cout << "\nMaximum value = " << maxValue << "\n";
    printSelectedItems(value, weight, dp, itemCount, capacity);
}

int main() {
    run();
    return 0;
}
