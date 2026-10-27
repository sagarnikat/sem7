#include <chrono>
#include <iostream>
#include <random>
#include <vector>

using namespace std;

struct SortStats {
    unsigned long long comparisons = 0;
    unsigned long long swaps = 0;
};

int partition(vector<int>& values, int low, int high, SortStats& stats) {
    int pivot = values[high];
    int boundary = low;
    for (int i = low; i < high; ++i) {
        ++stats.comparisons;
        if (values[i] <= pivot) {
            swap(values[i], values[boundary]);
            ++stats.swaps;
            ++boundary;
        }
    }
    swap(values[boundary], values[high]);
    ++stats.swaps;
    return boundary;
}

int randomizedPartition(vector<int>& values, int low, int high,
                        SortStats& stats, mt19937& generator) {
    uniform_int_distribution<int> distribution(low, high);
    int pivotIndex = distribution(generator);
    swap(values[pivotIndex], values[high]);
    ++stats.swaps;
    return partition(values, low, high, stats);
}

void deterministicQuickSort(vector<int>& values, int low, int high,
                            SortStats& stats) {
    if (low >= high) {
        return;
    }
    int pivotIndex = partition(values, low, high, stats);
    deterministicQuickSort(values, low, pivotIndex - 1, stats);
    deterministicQuickSort(values, pivotIndex + 1, high, stats);
}

void randomizedQuickSort(vector<int>& values, int low, int high,
                         SortStats& stats, mt19937& generator) {
    if (low >= high) {
        return;
    }
    int pivotIndex = randomizedPartition(values, low, high, stats, generator);
    randomizedQuickSort(values, low, pivotIndex - 1, stats, generator);
    randomizedQuickSort(values, pivotIndex + 1, high, stats, generator);
}

void printResults(const char* label, const vector<int>& values,
                  const SortStats& stats, chrono::nanoseconds elapsed) {
    cout << label << ": ";
    for (int value : values) {
        cout << value << ' ';
    }
    cout << "\nComparisons: " << stats.comparisons
         << ", swaps: " << stats.swaps
         << ", elapsed: " << elapsed.count() << " ns\n";
}

int main() {
    int count;
    cout << "Enter number of elements: ";
    if (!(cin >> count) || count < 0) {
        cerr << "The element count must be non-negative.\n";
        return 1;
    }

    vector<int> original(count);
    cout << "Enter " << count << " integers: ";
    for (int& value : original) {
        if (!(cin >> value)) {
            cerr << "Invalid input value.\n";
            return 1;
        }
    }

    vector<int> deterministic = original;
    vector<int> randomized = original;
    SortStats deterministicStats;
    SortStats randomizedStats;
    mt19937 generator(random_device{}());

    auto start = chrono::steady_clock::now();
    deterministicQuickSort(deterministic, 0, count - 1, deterministicStats);
    auto deterministicElapsed = chrono::steady_clock::now() - start;

    start = chrono::steady_clock::now();
    randomizedQuickSort(randomized, 0, count - 1, randomizedStats, generator);
    auto randomizedElapsed = chrono::steady_clock::now() - start;

    printResults("Deterministic quick sort", deterministic, deterministicStats,
                 chrono::duration_cast<chrono::nanoseconds>(deterministicElapsed));
    printResults("Randomized quick sort", randomized, randomizedStats,
                 chrono::duration_cast<chrono::nanoseconds>(randomizedElapsed));
    cout << "Deterministic: average O(n log n), worst O(n^2) time; "
            "average O(log n), worst O(n) stack space.\n";
    cout << "Randomized: expected O(n log n), worst O(n^2) time; "
            "expected O(log n), worst O(n) stack space.\n";
}
