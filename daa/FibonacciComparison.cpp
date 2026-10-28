/*
 * PROBLEM STATEMENT : Fibonacci number - iterative vs recursive
 *
 * The Fibonacci sequence starts 0, 1; every later term is the sum of the two
 * previous ones: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).
 *
 * HOW IT WORKS:
 *   ITERATIVE (bottom-up):
 *     Keep just two running values a = F(i-2) and b = F(i-1) and update them
 *     in a loop n-1 times. O(n) time, O(1) space, no repeated work.
 *   RECURSIVE (definition -> code):
 *     Directly apply the formula: F(n) = F(n-1) + F(n-2) with the two base
 *     cases above. Easy to read but HORRIBLY slow, because:
 *       - F(n-1) and F(n-2) overlap and recompute the same subproblems;
 *       - the call tree holds ~1.618^n nodes (golden-ratio growth).
 *     Running times: iterative O(n) vs recursive O(2^n) (roughly).
 *
 * WHY THIS COMPARISON MATTERS (lecture point):
 *   This exercise is the standard illustration of why naive recursion can be
 *   exponentially wasteful, and why memoisation / dynamic programming fixes
 *   it: storing each F(k) once turns 2^n calls into n additions.
 *
 * NOTES / INFO:
 *   - Both versions are in one file to make the comparison honest; main()
 *     still contains exactly one function call.
 *   - Results are kept in long long: F(92) is the largest value that fits;
 *     after that the numbers silently overflow, which is why input is capped.
 */

#include <iostream>

using namespace std;

const int LIMIT = 92;   // F(92) overflows for long long beyond this

// ---------- ITERATIVE version ----------
// O(n) time, O(1) space: carry the last two values forward.
long long fibonacciIterative(int n) {
    if (n <= 1) return n;

    long long a = 0, b = 1;         // F(i-2) and F(i-1)
    for (int i = 2; i <= n; ++i) {
        long long c = a + b;        // F(i) from the two previous terms
        a = b;                      // slide the window one step
        b = c;
    }
    return b;
}

// ---------- RECURSIVE version ----------
// Faithful translation of the formula, but exponential time.
long long fibonacciRecursive(int n) {
    if (n == 0) return 0;                                   // base case 1
    if (n == 1) return 1;                                   // base case 2
    return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
}

// Ask n once, compute both ways, show a practical timing contrast.
void run() {
    cout << "Enter n (0 to " << LIMIT
         << "; the recursive version is exponential): "; 
    int n;
    if (!(cin >> n) || n < 0 || n > LIMIT) {
        cout << "Invalid input.\n";
        return;
    }

    cout << "Iterative result : F(" << n << ") = " << fibonacciIterative(n)
         << "\n";
    cout << "Recursive result : F(" << n << ") = " << fibonacciRecursive(n)
         << "\n";
    cout << "\nNote: above n = 40 the recursive call count explodes; the "
         << "iterative version is instant.\n";
}

int main() {
    run();
    return 0;
}
