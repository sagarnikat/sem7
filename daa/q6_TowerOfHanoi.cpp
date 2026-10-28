/*
 * QUESTION 6 (DAA) : Solve the Tower of Hanoi problem using recursion.
 *
 * Three pegs are named A (source), B (auxiliary) and C (destination). Disk
 * stack A contains n disks, largest at the bottom; move them all to C
 * following the rules:
 *   - only ONE disk may be moved at a time (the top disk of any peg),
 *   - a larger disk can never rest on top of a smaller one.
 *
 * HOW IT WORKS (DIVIDE AND CONQUER / RECURSION):
 *   To move n disks (n, A, B, C):
 *   Step 1. move the top n-1 disks out of the way: A -> B (using C), which
 *           uncovers the largest disk;
 *   Step 2. move the largest disk directly A -> C;
 *   Step 3. move those n-1 disks from the auxiliary peg onto C: B -> C
 *           (using A).
 *   Base case: n == 1 -> a single direct move.
 *
 * TOTAL NUMBER OF MOVES = 2^n - 1 (geometric series), so even modest n grows
 * extremely fast (n = 30 -> 1,073,741,823 moves).
 *
 * COMPLEXITY:
 *   - Time  : O(2^n) - the output itself has that many lines.
 *   - Space : O(n)  - recursion stack depth (only n frames, one per disk).
 *
 * NOTES / INFO:
 *   - The roles of the three pegs ROTATE in every recursive call; this is why
 *     the function takes source, auxiliary and destination as arguments
 *     instead of hard-coding A/B/C.
 *   - Try n = 3 first: the printed sequence is the classic 7-move solution.
  *
 * COMMANDS (run from inside this folder):
 *   install dependencies : sudo apt install g++
 *   compile and run      : g++ -std=c++17 -Wall q6_TowerOfHanoi.cpp -o q6_TowerOfHanoi && ./q6_TowerOfHanoi
*/

#include <iostream>

using namespace std;

// Print a single move in everyday words.
void printMove(int disk, char source, char destination) {
    cout << "Move disk " << disk << " from " << source
         << " to " << destination << "\n";
}

// Move `n` disks from source (S) to destination (D) via auxiliary (AUX).
void towerOfHanoi(int n, char source, char auxiliary, char destination) {
    if (n == 1) {            // base case: one disk moves directly
        printMove(1, source, destination);
        return;
    }
    towerOfHanoi(n - 1, source, destination, auxiliary);  // Step 1
    printMove(n, source, destination);                   // Step 2
    towerOfHanoi(n - 1, auxiliary, source, destination); // Step 3
}

// Read the number of disks, run the algorithm, show the move count.
void run() {
    int n;
    cout << "Enter number of disks: ";
    cin >> n;

    if (n < 1) {
        cout << "Number of disks must be at least 1.\n";
        return;
    }

    towerOfHanoi(n, 'A', 'B', 'C');

    // 2^n - 1 = total moves (only meaningful for small n; use long long).
    long long totalMoves = (1LL << n) - 1;
    cout << "\nTotal moves = " << totalMoves << "\n";
}

int main() {
    run();
    return 0;
}
