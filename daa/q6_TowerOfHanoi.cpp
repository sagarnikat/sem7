/*
 * QUESTION 6 (DAA) : Solve the Tower of Hanoi problem using recursion.
 *
 * Three pegs are named A (source), B (auxiliary) and C (destination). Peg A
 * starts with n disks, largest at the bottom; they must all reach C while:
 *   - only ONE disk moves at a time (the top disk of some peg), and
 *   - a larger disk is never placed on top of a smaller one.
 *
 * HOW IT WORKS (DIVIDE AND CONQUER / RECURSION):
 *   To move n disks from SOURCE to DESTINATION using AUXILIARY:
 *   Step 1. move the top n-1 disks SOURCE -> AUXILIARY (using DESTINATION),
 *           which uncovers the largest disk;
 *   Step 2. move the largest disk SOURCE -> DESTINATION;
 *   Step 3. move those n-1 disks AUXILIARY -> DESTINATION (using SOURCE).
 *   Base case: n == 1 -> one direct move.
 *
 * TOTAL NUMBER OF MOVES:
 *   T(n) = 2 * T(n-1) + 1  =>  T(n) = 2^n - 1.
 *   It grows extremely fast: n = 10 -> 1,023 moves, n = 30 -> 1,073,741,823.
 *
 * COMPLEXITY:
 *   - Time  : O(2^n) - the printed output itself has that many lines.
 *   - Space : O(n)   - recursion stack, one frame per disk.
 *
 * NOTES / INFO:
 *   - The roles of the three pegs ROTATE in every recursive call; this is why
 *     the function takes source, auxiliary and destination as arguments
 *     instead of hard-coding A, B and C.
 *   - Run with n = 1, 2, 3 to see the sequence 1, 3, 7 moves; the trace after
 *     each move shows that no larger disk ever lands on a smaller one.
 *
 * COMMANDS (run from inside this folder):
 *   install dependencies : sudo apt install g++
 *   compile and run      : g++ -std=c++17 -Wall q6_TowerOfHanoi.cpp -o q6_TowerOfHanoi && ./q6_TowerOfHanoi
*/

#include <iostream>
#include <vector>

using namespace std;

// Move `n` disks from source to destination using the auxiliary peg.
void towerOfHanoi(int n, char source, char auxiliary, char destination) {
    if (n == 1) {                                   // base case
        cout << "Move disk 1 from " << source << " to " << destination << "\n";
        return;
    }

    towerOfHanoi(n - 1, source, destination, auxiliary);  // Step 1
    cout << "Move disk " << n << " from " << source
         << " to " << destination << "\n";                // Step 2
    towerOfHanoi(n - 1, auxiliary, source, destination);  // Step 3
}

// Number of moves for n disks, without running the recursion.
long long moveCount(int n) {
    return (1LL << n) - 1;              // 2^n - 1 (unsigned shifts are safe here)
}

// Read n, print every move, then compare with 2^n - 1.
void run() {
    int n;
    cout << "Enter the number of disks: ";
    cin >> n;

    if (n < 1) {
        cout << "Number of disks must be at least 1.\n";
        return;
    }
    if (n > 25) {
        cout << "That would print more than " << moveCount(25)
             << " lines; use 25 or fewer.\n";
        return;
    }

    cout << "\nSequence of moves:\n";
    towerOfHanoi(n, 'A', 'B', 'C');

    cout << "\nTotal moves = " << moveCount(n)
         << "  (= 2^" << n << " - 1)\n";
}

int main() {
    run();
    return 0;
}
