#include <iostream>
#include <vector>

using namespace std;

bool isSafe(const vector<int>& queenColumnByRow, int row, int column) {
    for (int previousRow = 0; previousRow < row; ++previousRow) {
        int previousColumn = queenColumnByRow[previousRow];
        if (previousColumn == column ||
            previousRow - previousColumn == row - column ||
            previousRow + previousColumn == row + column) {
            return false;
        }
    }
    return true;
}

bool placeQueens(vector<int>& queenColumnByRow, int row, int n) {
    if (row == n) {
        return true;
    }
    for (int column = 0; column < n; ++column) {
        if (isSafe(queenColumnByRow, row, column)) {
            queenColumnByRow[row] = column;
            if (placeQueens(queenColumnByRow, row + 1, n)) {
                return true;
            }
            queenColumnByRow[row] = -1;
        }
    }
    return false;
}

int main() {
    int n;
    int firstQueenColumn;
    cout << "Enter board size n (1 to 15) and first queen column (1 to n): ";
    if (!(cin >> n >> firstQueenColumn) || n < 1 || n > 15 ||
        firstQueenColumn < 1 || firstQueenColumn > n) {
        cerr << "n must be between 1 and 15 and the column must be between 1 and n.\n";
        return 1;
    }

    vector<int> queenColumnByRow(n, -1);
    queenColumnByRow[0] = firstQueenColumn - 1;
    if (!isSafe(queenColumnByRow, 0, firstQueenColumn - 1) ||
        !placeQueens(queenColumnByRow, 1, n)) {
        cerr << "No solution exists with the first queen fixed at row 1, column "
             << firstQueenColumn << ".\n";
        return 1;
    }

    cout << "Solution with the first queen fixed at row 1, column "
         << firstQueenColumn << ":\n";
    for (int row = 0; row < n; ++row) {
        for (int column = 0; column < n; ++column) {
            cout << (queenColumnByRow[row] == column ? "Q " : ". ");
        }
        cout << '\n';
    }
    cout << "Complexity: O(n!) worst-case time and O(n) auxiliary space\n";
}
