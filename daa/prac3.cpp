#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>

using namespace std;

struct Item {
    double value;
    double weight;
    double ratio;
};

int main() {
    int count;
    double capacity;
    cout << "Enter number of items and knapsack capacity: ";
    if (!(cin >> count >> capacity) || count < 0 || capacity < 0) {
        cerr << "Item count and capacity must be non-negative.\n";
        return 1;
    }

    vector<Item> items(count);
    for (int i = 0; i < count; ++i) {
        cout << "Enter value and weight for item " << i + 1 << ": ";
        if (!(cin >> items[i].value >> items[i].weight) ||
            items[i].value < 0 || items[i].weight <= 0) {
            cerr << "Values must be non-negative and weights must be positive.\n";
            return 1;
        }
        items[i].ratio = items[i].value / items[i].weight;
    }

    sort(items.begin(), items.end(), [](const Item& first, const Item& second) {
        return first.ratio > second.ratio;
    });

    double totalValue = 0;
    double remainingCapacity = capacity;
    for (const Item& item : items) {
        if (remainingCapacity <= 0) {
            break;
        }
        const double fraction = min(1.0, remainingCapacity / item.weight);
        totalValue += fraction * item.value;
        remainingCapacity -= fraction * item.weight;
    }

    cout << fixed << setprecision(2);
    cout << "Maximum value: " << totalValue << '\n';
    cout << "Complexity: O(n log n) time and O(n) space for n items\n";
}
