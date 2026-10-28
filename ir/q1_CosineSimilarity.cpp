/*
 * QUESTION 1 (IR) : Compare two text documents using cosine similarity.
 *
 * Measure how similar two documents are. Convert each document to a
 * word-frequency vector, treating every distinct word as one dimension; then
 * measure the cosine of the angle between the two vectors:
 *
 *        cos(theta) = (D1 . D2) / (|D1| * |D2|)
 *
 *   - 1.0   -> identical direction (same words in the same proportions)
 *   - 0.0   -> no word shared at all
 *   The value ignores document LENGTH, which is what makes it useful in IR:
 *   a long article and its abstract can still score high.
 *
 * HOW IT WORKS:
 *   1. Preprocess each document: lowercase it, strip every character that is
 *      not a letter/digit, and split on whitespace ("Hello, World!" and
 *      "hello world" become the same tokens).
 *   2. Count word frequencies (the vector, one entry per term).
 *   3. Dot product  = sum over the union vocabulary of f1[w]*f2[w]
 *      (f1[w]=0 for words missing from a document, so absent words add 0).
 *   4. Magnitude  = sqrt(sum of squares of the frequencies).
 *   5. Similarity = dot / (|v1| * |v2|), with a 0 guard against /0.
 *
 * COMPLEXITY:
 *   O(n1 + n2) time for the token counting plus O(v) for the vocabulary pass
 *   (n = text lengths, v = vocabulary size); O(v) extra space.
 *
 * NOTES / INFO:
 *   - This is exactly the scoring formula behind TF vector-space retrieval;
 *     weigh with IDF next and you get TF-IDF (see the ML spam practical).
 *   - Frequencies are raw counts, not normalized TFs - fine for the lab.
  *
 * COMMANDS (run from inside this folder):
 *   install dependencies : sudo apt install g++
 *   compile and run      : g++ -std=c++17 -Wall q1_CosineSimilarity.cpp -o q1_CosineSimilarity && ./q1_CosineSimilarity
*/

#include <cmath>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>

using namespace std;

// Lowercase the text and keep only [a-z0-9]; other chars become spaces.
string preprocess(const string& text) {
    string cleaned;
    for (char c : text) {
        if (isalnum(static_cast<unsigned char>(c)))
            cleaned += static_cast<char>(tolower(static_cast<unsigned char>(c)));
        else
            cleaned += ' ';  // punctuation/symbols act as token separators
    }
    return cleaned;
}

// Count how many times each word occurs -> the document's frequency vector.
unordered_map<string, int> wordFrequencies(const string& text) {
    unordered_map<string, int> freq;
    istringstream stream(preprocess(text));
    string word;
    while (stream >> word) freq[word]++;  // split on whitespace automatically
    return freq;
}

// Core similarity computation between two frequency vectors.
double cosineSimilarity(const unordered_map<string, int>& freq1,
                        const unordered_map<string, int>& freq2) {
    // Union vocabulary: every word seen in either document.
    unordered_set<string> vocabulary;
    for (const auto& [word, _] : freq1) vocabulary.insert(word);
    for (const auto& [word, _] : freq2) vocabulary.insert(word);

    // Dot product: only words present in BOTH vectors contribute.
    double dotProduct = 0.0;
    double sumSquares1 = 0.0, sumSquares2 = 0.0;
    for (const string& word : vocabulary) {
        int f1 = freq1.count(word) ? freq1.at(word) : 0;
        int f2 = freq2.count(word) ? freq2.at(word) : 0;
        dotProduct += static_cast<double>(f1) * f2;
        sumSquares1 += static_cast<double>(f1) * f1;
        sumSquares2 += static_cast<double>(f2) * f2;
    }

    double magnitude1 = sqrt(sumSquares1);
    double magnitude2 = sqrt(sumSquares2);

    // Empty document(s): undefined angle -> call it "no similarity".
    if (magnitude1 == 0.0 || magnitude2 == 0.0) return 0.0;

    return dotProduct / (magnitude1 * magnitude2);
}

// Drives the whole practical; main() only calls this.
void run() {
    cout << "Enter first document: ";
    string doc1;
    getline(cin, doc1);

    cout << "Enter second document: ";
    string doc2;
    getline(cin, doc2);

    double similarity = cosineSimilarity(wordFrequencies(doc1),
                                         wordFrequencies(doc2));

    cout << fixed << setprecision(4);
    cout << "\nCosine Similarity = " << similarity << "\n";
    cout << "Similarity Percentage = " << similarity * 100 << " %\n";
}

int main() {
    run();
    return 0;
}
