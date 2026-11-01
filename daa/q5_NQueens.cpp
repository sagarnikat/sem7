/*
 * QUESTION 5 (DAA) : N-Queens matrix with the first queen placed, solved by backtracking.
 *
 * Place N chess queens on an N x N board so that NO two queens attack each
 * other. A queen attacks along its row, its column, and both diagonals - so a
 * valid solution has exactly one queen per row and no two queens sharing a
 * column, a "/" diagonal, or a "\" diagonal.
 *
 * HOW IT WORKS (BACKTRACKING):
 *   1. Place queens one ROW at a time (each row must hold exactly one queen,
 *      so we never try two rows at once).
 *   2. In the current row, try every column; keep the column only if it is
 *      "safe" against the queens already placed above.
 *   3. Recurse for the next row. If some later row becomes impossible, return
 *      here, REMOVE the queen (Backtrack) and try the next column.
 *   4. A solution is found when all N rows hold a queen successfully; if every
 *      option in this row fails, report failure upward.
 *   This program follows the lab constraint: the FIRST queen is permanently
 *   fixed at square (0, 0), so for some N (e.g. 6) the answer may legitimately
 *   be "no solution" even though one exists with the first queen elsewhere.
 *
 * COMPLEXITY:
 *   - Worst case: O(N!) states (exponential - the problem is NP-hard-ish),
 *     but pruning (isSafe) throws away huge parts of the search tree early,
 *     so small N (up to ~15) run comfortably fast.
 *   - Space: O(N) recursion depth + O(N^2) board for printing.
 *
 * NOTES / INFO:
 *   - The known solution counts: N=4 -> 2, N=8 -> 92 total solutions; this
 *     program prints only the FIRST one found.
 *   - No solution exists at all for N = 2 and N = 3.
  *
 * COMMANDS (run from inside this folder):
 *   install dependencies : sudo apt install g++
 *   compile and run      : g++ -std=c++17 -Wall q5_NQueens.cpp -o q5_NQueens && ./q5_NQueens
*/

#include <iostream>
#include <vector>

using namespace std;

int g_n = 0;
vector<vector<int>> g_board;

bool isSafe(int row, int col) {

    for (int r = 0; r < row; ++r)
        if (g_board[r][col]) return false;

    for (int r = row - 1, c = col - 1; r >= 0 && c >= 0; --r, --c)
        if (g_board[r][c]) return false;

    for (int r = row - 1, c = col + 1; r >= 0 && c < g_n; --r, ++c)
        if (g_board[r][c]) return false;

    return true;
}

bool solveNQueens(int row) {
    if (row == g_n) return true;

    if (row == 0) return solveNQueens(row + 1);

    for (int col = 0; col < g_n; ++col) {
        if (isSafe(row, col)) {
            g_board[row][col] = 1;
            if (solveNQueens(row + 1)) return true;
            g_board[row][col] = 0;
        }
    }
    return false;
}

void printBoard() {
    cout << "\nSolution Matrix:\n";
    for (int r = 0; r < g_n; ++r) {
        for (int c = 0; c < g_n; ++c) cout << g_board[r][c] << " ";
        cout << "\n";
    }
}

void run() {
    cout << "Enter the value of N: ";
    cin >> g_n;

    if (g_n < 1) {
        cout << "N must be at least 1.\n";
        return;
    }

    g_board.assign(g_n, vector<int>(g_n, 0));
    g_board[0][0] = 1;

    if (solveNQueens(0)) {
        printBoard();
    } else {
        cout << "No solution exists with the first queen at (0, 0).\n";
    }
}

int main() {
    run();
    return 0;
}
