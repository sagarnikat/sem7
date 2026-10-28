/*
 * QUESTION 3 (DAA) : Solve the fractional Knapsack problem using a greedy method.
 *
 * Given n items, each with a value and a weight, and a knapsack of a fixed
 * capacity, fill the knapsack so that the total value is maximum. Unlike the
 * 0/1 knapsack, here we are ALLOWED to cut an item and take only a fraction
 * of it (taking a fraction f of an item gives f * value and weighs f * weight).
 *
 * HOW IT WORKS (GREEDY STRATEGY):
 *   1. Compute value/weight ratio for every item.
 *   2. Sort items in DECREASING order of this ratio. The item with the highest
 *      ratio gives the most value per kilogram, so it is the "best deal".
 *   3. Walk through the sorted list:
 *        - If the whole item fits in the remaining capacity, take it fully.
 *        - Otherwise take only the fraction that fits, then stop.
 *   This greedy choice is provably OPTIMAL for the fractional version.
 *
 * COMPLEXITY:
 *   - Sorting dominates : O(n log n)
 *   - Single linear scan: O(n)
 *   - Total             : O(n log n) time, O(n) space.
 *
 * NOTES / INFO:
 *   - Input is entered item by item (value, then weight), same as the lab
 *     exercise, followed by the knapsack capacity.
 *   - Works with integer or fractional values and weights (uses double).
 *   - Contrast with 0/1 knapsack: greedy fails for 0/1 version, DP is needed.
  *
 * COMMANDS (run from inside this folder):
 *   install dependencies : sudo apt install g++
 *   compile and run      : g++ -std=c++17 -Wall q3_FractionalKnapsack.cpp -o q3_FractionalKnapsack && ./q3_FractionalKnapsack
*/

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>

using namespace std;

// One knapsack item: its value, its weight, and its value-per-unit ratio.
struct Item {
    double value;
    double weight;
    double ratio;
};

// Read all items and the capacity from standard input.
vector<Item> readItems(int itemCount) {
    vector<Item> items(itemCount);

    cout << "Enter value and weight of each item:\n";
    for (int i = 0; i < itemCount; ++i) {
        cout << "Item " << (i + 1) << " value: ";
        cin >> items[i].value;
        cout << "Item " << (i + 1) << " weight: ";
        cin >> items[i].weight;
        items[i].ratio = items[i].value / items[i].weight;  // the "deal quality"
    }
    return items;
}

// Sort items so the best value/weight ratio comes first (greedy order).
void sortByRatio(vector<Item>& items) {
    sort(items.begin(), items.end(),
         [](const Item& a, const Item& b) { return a.ratio > b.ratio; });
}

// Core greedy algorithm: take whole items while they fit, then a fraction.
double fillKnapsack(vector<Item> items, double capacity) {
    sortByRatio(items);

    double totalValue = 0.0;
    double remaining = capacity;

    cout << "\nSelected Items:\n";
    for (size_t i = 0; i < items.size(); ++i) {
        if (remaining <= 0) break;  // knapsack is full -> stop

        if (items[i].weight <= remaining) {
            // Whole item fits: take 100% of it.
            remaining -= items[i].weight;
            totalValue += items[i].value;
            cout << "Item " << (i + 1) << " -> 100% selected\n";
        } else {
            // Item does not fit: take the fraction of it that fits.
            double fraction = remaining / items[i].weight;
            totalValue += items[i].value * fraction;
            cout << "Item " << (i + 1) << " -> " << fixed << setprecision(2)
                 << fraction * 100 << "% selected\n";
            remaining = 0;
        }
    }
    return totalValue;
}

// Drives the whole practical; main() only calls this.
void run() {
    int itemCount;
    cout << "Enter number of items: ";
    cin >> itemCount;

    vector<Item> items = readItems(itemCount);

    double capacity;
    cout << "Enter knapsack capacity: ";
    cin >> capacity;

    double maxValue = fillKnapsack(items, capacity);

    cout << fixed << setprecision(2);
    cout << "\nMaximum value = " << maxValue << "\n";
}

int main() {
    run();
    return 0;
}
