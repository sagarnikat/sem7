/*
 * QUESTION 4 (IR) : Calculate the PageRank of a small directed web graph.
 *
 * Compute PageRank on the small directed web graph from the lab:
 *
 *        Page 1 -> links to 2, 3
 *        Page 2 -> links to 3
 *        Page 3 -> links to 1, 4
 *        Page 4 -> links to 1
 *
 * A page's importance is NOT how many links point TO it, but how IMPORTANT
 * those pointing pages are: every page divides its own rank equally among the
 * pages it links to.
 *
 * THE ALGORITHM (power iteration):
 *   Start with rank[i] = 1/n for all n pages. Each iteration computes:
 *
 *        newRank[j] = (1 - d)/n  +  d * sum over every i linking j of
 *                                   rank[i] / outDegree(i)
 *
 *   d = damping factor (0.85 here): with probability d the random surfer
 *   follows a link, otherwise she jumps to a random page - that jumpy part
 *   (1-d)/n keeps the method converging and handles loops nicely.
 *   Repeat for a fixed number of iterations (or until changes drop below a
 *   tolerance) and the values converge to the principal eigenvector of the
 *   normalised link matrix.
 *
 * COMPLEXITY:
 *   O(iterations * E) for E links in adjacency-matrix form:
 *   O(iterations * n^2) here since every cell is inspected.
 *
 * NOTES / INFO:
 *   - The (1-d)/n term is what saves pages with NO inbound links from
 *     dropping to rank 0.
 *   - Real PageRank adds extra refinements (e.g. dangling-node handling -
 *     see TopicPageRank.cpp for a version that models them); the lab graph
 *     above has no dangling nodes, so the plain recurrence converges cleanly.
  *
 * COMMANDS (run from inside this folder):
 *   install dependencies : sudo apt install g++
 *   compile and run      : g++ -std=c++17 -Wall q4_PageRank.cpp -o q4_PageRank && ./q4_PageRank
*/

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <vector>

using namespace std;

const double DAMPING = 0.85;   // probability of following a link
const int    ITERATIONS = 100;

// The lab graph: graph[i][j] = 1 if page i links to page j (fixed dataset).
const vector<vector<int>> GRAPH = {
    {0, 1, 1, 0},   // page 1 -> 2, 3
    {0, 0, 1, 0},   // page 2 -> 3
    {1, 0, 0, 1},   // page 3 -> 1, 4
    {1, 0, 0, 0},   // page 4 -> 1
};

// One power-iteration step: distribute every page's rank along its links.
vector<double> step(const vector<double>& rank, int n) {
    // Teleport base: every page starts here (random-jump part).
    vector<double> newRank(n, (1.0 - DAMPING) / n);

    for (int i = 0; i < n; ++i) {
        // Count page i's outgoing links.
        int outgoing = accumulate(GRAPH[i].begin(), GRAPH[i].end(), 0);
        if (outgoing == 0) continue;   // no links -> nothing to give away

        for (int j = 0; j < n; ++j) {
            if (GRAPH[i][j] == 1) {
                // Share i's rank equally over all of i's targets.
                newRank[j] += DAMPING * rank[i] / outgoing;
            }
        }
    }
    return newRank;
}

// Run the fixed number of power iterations and return the final ranks.
vector<double> pageRank(int n) {
    vector<double> rank(n, 1.0 / n);   // everyone starts equally important
    for (int it = 0; it < ITERATIONS; ++it) rank = step(rank, n);
    return rank;
}

// Print ranks and then the pages sorted from most to least important.
void printResults(const vector<double>& ranks, int n) {
    cout << "PageRank Values:\n";
    cout << fixed << setprecision(6);
    for (int i = 0; i < n; ++i) cout << "Page " << i + 1 << " : " << ranks[i] << "\n";

    // Ranking order: indices sorted by descending rank value.
    vector<int> order(n);
    iota(order.begin(), order.end(), 0);
    sort(order.begin(), order.end(),
         [&ranks](int a, int b) { return ranks[a] > ranks[b]; });

    cout << "\nPage Ranking:\n";
    for (int position = 0; position < n; ++position)
        cout << position + 1 << " -> Page " << order[position] + 1 << "\n";
}

// Drives the whole practical; main() only calls this.
void run() {
    int n = static_cast<int>(GRAPH.size());
    vector<double> ranks = pageRank(n);
    printResults(ranks, n);
}

int main() {
    run();
    return 0;
}
