/*
 * PROBLEM STATEMENT : Huffman Coding (Greedy Algorithm)
 *
 * Compress a piece of text by assigning each character a variable-length binary
 * code. Frequently used characters get SHORT codes and rare characters get
 * LONG codes, so the total number of bits is smaller than using fixed-length
 * codes (e.g. ASCII's 8 bits per character).
 *
 * HOW IT WORKS (GREEDY TREE CONSTRUCTION):
 *   1. Count the frequency of every character in the text.
 *   2. Put every character in a min-priority-queue keyed by frequency.
 *   3. Repeatedly remove the two nodes with the SMALLEST frequency, create a
 *      parent node whose frequency is their sum, and push it back. Each such
 *      merge is one internal node of the tree. Repeat until one node is left:
 *      this is the root of the Huffman tree.
 *   4. The tree assigns codes naturally:
 *        - every left branch contributes a '0',
 *        - every right branch contributes a '1',
 *        - the code of a leaf is the path from the root to it.
 *   5. ENCODING  : concatenating the code of each character of the text.
 *      DECODING  : walk the tree from the root, one bit at a time; a leaf
 *                  ends one character, then restart from the root. Decoding is
 *                  unambiguous because no code is a prefix of another.
 *
 * WHY GREEDY IS OPTIMAL:
 *   Merging the two least frequent nodes puts them deepest in the tree (longest
 *   codes), which is exactly what minimises the total encoded length.
 *
 * COMPLEXITY:
 *   - Frequency count       : O(n) over the text
 *   - Tree building         : O(k log k) for k distinct characters
 *   - Encode / decode       : O(n) per message
 *
 * NOTES / INFO:
 *   - Interactive menu: build tree, encode, decode (same flow as the lab).
 *   - A text with a single distinct character gets the special code "0".
 *   - The code table depends on the text frequencies; decoding requires the
 *     same tree that encoding produced.
 */

#include <iostream>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

// A node of the Huffman tree: a leaf holds a character; an internal node
// holds two children. Leaves and internal nodes are kept in one structure.
struct Node {
    char ch;        // valid only for leaves
    int freq;       // total frequency of the subtree rooted here
    Node* left;     // child reached with bit '0'
    Node* right;    // child reached with bit '1'

    // Leaf constructor
    Node(char symbol, int frequency) : ch(symbol), freq(frequency),
                                       left(nullptr), right(nullptr) {}

    // Internal (merged) constructor
    Node(int frequency, Node* leftChild, Node* rightChild)
        : ch('\0'), freq(frequency), left(leftChild), right(rightChild) {}

    bool isLeaf() const { return left == nullptr && right == nullptr; }
};

// Min-heap ordering: the node with the smallest frequency comes out first.
struct CompareFreq {
    bool operator()(const Node* a, const Node* b) const {
        return a->freq > b->freq;
    }
};

Node* g_root = nullptr;                          // root of the Huffman tree
unordered_map<char, string> g_codes;             // character -> its code

// Count how many times every character occurs in the text.
unordered_map<char, int> countFrequencies(const string& text) {
    unordered_map<char, int> freq;
    for (char c : text) freq[c]++;
    return freq;
}

// Recursively label the tree: going left appends '0', going right appends '1'.
void generateCodes(Node* node, string code) {
    if (node == nullptr) return;

    if (node->isLeaf()) {
        // Edge case: a tree with a single character gives it the code "0".
        g_codes[node->ch] = code.empty() ? "0" : code;
        return;
    }
    generateCodes(node->left, code + "0");
    generateCodes(node->right, code + "1");
}

// The greedy part: repeatedly merge the two least frequent nodes.
void buildTree(const string& text) {
    unordered_map<char, int> freq = countFrequencies(text);

    priority_queue<Node*, vector<Node*>, CompareFreq> pq;
    for (const auto& [ch, count] : freq) pq.push(new Node(ch, count));

    // Special case: only one unique character in the whole text.
    if (pq.size() == 1) {
        Node* only = pq.top();
        g_root = new Node(only->freq, only, nullptr);
    } else {
        while (pq.size() > 1) {
            Node* left = pq.top(); pq.pop();
            Node* right = pq.top(); pq.pop();
            // Parent frequency = sum of the children (just an internal count).
            pq.push(new Node(left->freq + right->freq, left, right));
        }
        g_root = pq.top();
    }
    g_codes.clear();
    generateCodes(g_root, "");
}

// Replace every character of the text by its Huffman code.
string encode(const string& text) {
    string encoded;
    for (char c : text) encoded += g_codes[c];
    return encoded;
}

// Walk the tree bit by bit; reaching a leaf outputs one character.
string decode(const string& encoded, Node* root) {
    string decoded;
    Node* current = root;
    for (char bit : encoded) {
        current = (bit == '0') ? current->left : current->right;
        if (current->isLeaf()) {
            decoded += current->ch;
            current = root;  // restart for the next character
        }
    }
    return decoded;
}

// Pretty-print the code table ("[space]" is easier to read than ' ').
void displayCodes() {
    cout << "\nHuffman Codes:\n";
    for (const auto& [ch, code] : g_codes) {
        if (ch == ' ') cout << "[space] : " << code << "\n";
        else if (ch == '\t') cout << "[tab] : " << code << "\n";
        else cout << ch << " : " << code << "\n";
    }
}

// Drives the whole practical; main() only calls this.
void run() {
    cout << "Enter text: ";
    string text;
    getline(cin, text);

    if (text.empty()) {
        cout << "Text cannot be empty.\n";
        return;
    }

    buildTree(text);

    int choice;
    do {
        cout << "\n----- HUFFMAN ENCODING -----\n";
        cout << "1. Build Huffman Tree\n";
        cout << "2. Encode the Text\n";
        cout << "3. Decode the Text\n";
        cout << "4. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;
        cin.ignore();  // drop the newline so later getline calls behave

        if (choice == 1) {
            buildTree(text);
            cout << "\nHuffman Tree built successfully.\n";
            displayCodes();
        } else if (choice == 2) {
            string encoded = encode(text);
            cout << "\nOriginal Text : " << text << "\n";
            cout << "Encoded Text  : " << encoded << "\n";
            displayCodes();
        } else if (choice == 3) {
            string encoded = encode(text);
            string decoded = decode(encoded, g_root);
            cout << "\nEncoded Text : " << encoded << "\n";
            cout << "Decoded Text : " << decoded << "\n";
        } else if (choice == 4) {
            cout << "Program terminated.\n";
        } else {
            cout << "Invalid choice.\n";
        }
    } while (choice != 4);
}

int main() {
    run();
    return 0;
}
