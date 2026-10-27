#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

int main() {
    int count;
    int capacity;
    cout << "Enter number of items and integer capacity: ";
    if (!(cin >> count >> capacity) || count < 0 || capacity < 0) {
        cerr << "Item count and capacity must be non-negative integers.\n";
        return 1;
    }

    vector<int> weights(count);
    vector<long long> values(count);
    for (int i = 0; i < count; ++i) {
        cout << "Enter weight and value for item " << i + 1 << ": ";
        if (!(cin >> weights[i] >> values[i]) ||
            weights[i] <= 0 || values[i] < 0) {
            cerr << "Weights must be positive and values must be non-negative.\n";
            return 1;
        }
    }

    vector<long long> bestValue(capacity + 1, 0);
    for (int i = 0; i < count; ++i) {
        for (int currentCapacity = capacity; currentCapacity >= weights[i];
             --currentCapacity) {
            bestValue[currentCapacity] = max(
                bestValue[currentCapacity],
                bestValue[currentCapacity - weights[i]] + values[i]);
        }
    }

    cout << "Maximum value: " << bestValue[capacity] << '\n';
    cout << "Complexity: O(nW) time and O(W) space for n items and capacity W\n";
}
