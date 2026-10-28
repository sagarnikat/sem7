/*
 * PROBLEM STATEMENT : MapReduce demonstration (IR)
 *
 * Show the three classic stages of the MapReduce programming model on the
 * embedded sample string, counting how often every alphabetic character
 * occurs. This is the "word count is the Hello World of MapReduce" exercise;
 * here the unit is a single character instead of a word.
 *
 * THE THREE PHASES:
 *   1. MAP      - every mapper sees a small slice of the input and emits
 *                 (key, value) pairs. Here each alphabetic character emits
 *                 (lowercased letter, 1). Mappers are independent and can
 *                 run on different machines in a real cluster.
 *   2. SHUFFLE & SORT - all pairs sharing a key are routed and grouped
 *                 together: 'a' -> [1,1,1], 'b' -> [1], ...  The framework
 *                 does the routing; here one grouped structure shows it.
 *   3. REDUCE   - every key is reduced once: sum its list of values
 *                 (here always adding 1s) -> final count per key.
 *
 * WHY IT SCALES (the point of the exercise):
 *   Map and Reduce tasks are EMBARRASSINGLY parallel - each key reduces
 *   independently, each input slice maps independently - so work spreads
 *   across machines just by shuffling pairs between them.
 *
 * COMPLEXITY:
 *   O(n) map over n input characters, O(n + k) shuffle for k distinct keys,
 *   O(n) reduce = linear overall - same as a counter, but structured for
 *   distribution.
 *
 * NOTES / INFO:
 *   - Non-alphabetic characters are ignored (digits, spaces, punctuation).
 *   - Keys are printed in sorted order, matching the "sort" in the shuffle
 *     phase; a real Hadoop streaming job produces the same grouped output.
 */

#include <cctype>
#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

// The fixed sample dataset used by the exercise (same text as the lab).
const string SAMPLE_DATA =
    "Hello World!\n"
    "This is an Information Retrieval assignment.\n"
    "MapReduce counts alphabetic characters.\n"
    "Hello Python!\n";

// ---------------- MAP PHASE ----------------
// Every alphabetic character becomes a (letter, 1) pair.
vector<pair<char, int>> mapPhase(const string& data) {
    vector<pair<char, int>> mapped;
    for (char c : data) {
        if (isalpha(static_cast<unsigned char>(c)))
            mapped.emplace_back(
                static_cast<char>(tolower(static_cast<unsigned char>(c))), 1);
    }
    return mapped;
}

// ---------- SHUFFLE & SORT PHASE ----------
// Group all the 1s by key. std::map keeps the keys sorted automatically,
// which is exactly the "sort" half of this phase in a real framework.
map<char, vector<int>> shuffleAndSort(const vector<pair<char, int>>& mapped) {
    map<char, vector<int>> grouped;
    for (const auto& [letter, count] : mapped) grouped[letter].push_back(count);
    return grouped;
}

// ---------------- REDUCE PHASE ----------------
// Sum the list of values for each key; the pair list is the final output.
map<char, int> reducePhase(const map<char, vector<int>>& grouped) {
    map<char, int> result;
    for (const auto& [letter, counts] : grouped) {
        int total = 0;
        for (int count : counts) total += count;
        result[letter] = total;
    }
    return result;
}

// Print the final per-character counts.
void printResult(const map<char, int>& result) {
    cout << "Character Occurrence Count\n";
    cout << "---------------------------\n";
    for (const auto& [letter, count] : result)
        cout << letter << " : " << count << "\n";
}

// Drives the whole practical; main() only calls this.
void run() {
    vector<pair<char, int>> mapped = mapPhase(SAMPLE_DATA);          // map
    map<char, vector<int>> grouped = shuffleAndSort(mapped);         // shuffle
    map<char, int> result = reducePhase(grouped);                    // reduce
    printResult(result);                                             // output
}

int main() {
    run();
    return 0;
}
