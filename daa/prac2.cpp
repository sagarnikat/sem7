#include <iostream>
#include <queue>
#include <string>
#include <vector>

using namespace std;

struct Node {
    char symbol;
    long long frequency;
    Node* left;
    Node* right;

    Node(char symbol, long long frequency)
        : symbol(symbol), frequency(frequency), left(nullptr), right(nullptr) {}

    Node(Node* left, Node* right)
        : symbol('\0'),
          frequency(left->frequency + right->frequency),
          left(left),
          right(right) {}
};

struct CompareFrequency {
    bool operator()(const Node* first, const Node* second) const {
        return first->frequency > second->frequency;
    }
};

void printCodes(const Node* node, const string& code) {
    if (node == nullptr) {
        return;
    }
    if (node->left == nullptr && node->right == nullptr) {
        cout << node->symbol << ": " << (code.empty() ? "0" : code) << '\n';
        return;
    }
    printCodes(node->left, code + '0');
    printCodes(node->right, code + '1');
}

void deleteTree(Node* node) {
    if (node == nullptr) {
        return;
    }
    deleteTree(node->left);
    deleteTree(node->right);
    delete node;
}

int main() {
    int count;
    cout << "Enter number of symbols: ";
    if (!(cin >> count) || count <= 0) {
        cerr << "The number of symbols must be positive.\n";
        return 1;
    }

    priority_queue<Node*, vector<Node*>, CompareFrequency> queue;
    vector<Node*> leaves;
    for (int i = 0; i < count; ++i) {
        char symbol;
        long long frequency;
        cout << "Enter symbol and positive frequency: ";
        if (!(cin >> symbol >> frequency) || frequency <= 0) {
            for (Node* leaf : leaves) {
                delete leaf;
            }
            cerr << "Each frequency must be a positive integer.\n";
            return 1;
        }
        Node* leaf = new Node(symbol, frequency);
        leaves.push_back(leaf);
        queue.push(leaf);
    }

    while (queue.size() > 1) {
        Node* first = queue.top();
        queue.pop();
        Node* second = queue.top();
        queue.pop();
        queue.push(new Node(first, second));
    }

    Node* root = queue.top();
    cout << "Huffman codes:\n";
    printCodes(root, "");
    cout << "Complexity: O(k log k) time and O(k) space for k symbols\n";
    deleteTree(root);
}
