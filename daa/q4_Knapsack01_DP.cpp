/*
 * QUESTION 4 (DAA) : Solve the 0-1 Knapsack problem using dynamic programming.
 *
 * Given n items (each with a value and a weight) and a knapsack of integer
 * capacity W, choose a SUBSET of items (you can either take an item fully or
 * not at all - no fractions) so that the total value is maximum and the total
 * weight does not exceed W.
 *
 * HOW IT WORKS (TOP-DOWN DYNAMIC PROGRAMMING):
 *   1. Define solve(i, w) as the maximum value achievable using the first i
 *      items and a knapsack capacity of w.
 *   2. Recursively consider skipping item i or taking it when it fits, then
 *      memoize the result so each (i, w) state is solved only once.
 *   3. solve(n, W) is the answer. The memo table is also used to trace the
 *      chosen items backwards.
 *
 * COMPLEXITY:
 *   - Time  : O(n * W)  (pseudo-polynomial; each state is solved once)
 *   - Space : O(n * W)  (memo table plus O(n) recursion depth)
 *
 * NOTES / INFO:
 *   - Greedy does NOT work here (a high-ratio item may block several small
 *     items whose total value is larger), which is why DP is required.
 *   - Weights must be integers because they index the table columns.
 *   - Unlike the plain DP, this version also prints the chosen item numbers.
  *
 * COMMANDS (run from inside this folder):
 *   install dependencies : sudo apt install g++
 *   compile and run      : g++ -std=c++17 -Wall q4_Knapsack01_DP.cpp -o q4_Knapsack01_DP && ./q4_Knapsack01_DP
*/

#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

void readItems(int itemCount, vector<long long>& value, vector<int>& weight) {
    cout << "Enter value and weight of each item:\n";
    for (int i = 0; i < itemCount; ++i) {
        cout << "Item " << (i + 1) << " value: ";
        cin >> value[i];
        cout << "Item " << (i + 1) << " weight: ";
        cin >> weight[i];
    }
}

long long solveKnapsack(const vector<long long>& value,
                        const vector<int>& weight,
                        vector<vector<long long>>& memo,
                        int itemCount, int capacity) {
    if (itemCount == 0) return 0;
    if (memo[itemCount][capacity] != -1) return memo[itemCount][capacity];

    long long best = solveKnapsack(value, weight, memo, itemCount - 1, capacity);
    if (weight[itemCount - 1] <= capacity) {
        long long withItem = value[itemCount - 1] +
                             solveKnapsack(value, weight, memo, itemCount - 1,
                                           capacity - weight[itemCount - 1]);
        best = max(best, withItem);
    }

    memo[itemCount][capacity] = best;
    return best;
}

void printSelectedItems(const vector<long long>& value, const vector<int>& weight,
                        vector<vector<long long>>& memo, int itemCount,
                        int capacity) {
    cout << "Selected items:\n";
    int w = capacity;
    for (int i = itemCount; i > 0; --i) {
        long long withItems = solveKnapsack(value, weight, memo, i, w);
        long long withoutItem = solveKnapsack(value, weight, memo, i - 1, w);
        if (withItems != withoutItem) {
            cout << "Item " << i << " (value=" << value[i - 1]
                 << ", weight=" << weight[i - 1] << ")\n";
            w -= weight[i - 1];
        }
    }
}

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

    vector<vector<long long>> memo(itemCount + 1,
                                   vector<long long>(capacity + 1, -1));

    long long maxValue = solveKnapsack(value, weight, memo, itemCount, capacity);

    cout << "\nMaximum value = " << maxValue << "\n";
    printSelectedItems(value, weight, memo, itemCount, capacity);
}

int main() {
    run();
    return 0;
}
