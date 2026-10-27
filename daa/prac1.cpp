#include <iostream>

using namespace std;

long long fibonacciRecursive(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
}

long long fibonacciIterative(int n) {
    if (n <= 1) {
        return n;
    }

    long long previous = 0;
    long long current = 1;
    for (int i = 2; i <= n; ++i) {
        long long next = previous + current;
        previous = current;
        current = next;
    }
    return current;
}

int main() {
    int n;
    cout << "Enter n (0 to 40; recursive version is exponential): ";
    if (!(cin >> n) || n < 0 || n > 40) {
        cerr << "n must be between 0 and 40.\n";
        return 1;
    }

    cout << "Iterative Fibonacci: " << fibonacciIterative(n) << '\n';
    cout << "Recursive Fibonacci: " << fibonacciRecursive(n) << '\n';
    cout << "Iterative complexity: O(n) time, O(1) space\n";
    cout << "Recursive complexity: O(2^n) time, O(n) call-stack space\n";
}
