/*
 * QUESTION 2 (IR) : Remove stop words from a given text document.
 *
 * Stop words are the extremely common, content-free words of a language -
 * "the", "is", "at", "and", ... - that appear in almost every document and so
 * are nearly useless for telling documents apart. Removing them is standard
 * preprocessing BEFORE indexing or ranking, because it:
 *   - shrinks the index (stop words can be a large share of all tokens),
 *   - speeds up later steps (fewer terms to score),
 *   - removes noise which could otherwise dominate frequency comparisons.
 *
 * HOW IT WORKS:
 *   1. Lowercase the whole text (so "The" and "the" match the same entry).
 *   2. Tokenize by splitting on whitespace.
 *   3. Drop every token present in the fixed stop-word set;
 *      3a. keep the remainder in original order.
 *
 * COMPLEXITY:
 *   O(t) for t tokens: each token needs one O(1) hash-set lookup, plus a
 *   single output pass; O(|S|) extra space for the stop-word set.
 *
 * NOTES / INFO:
 *   - The stop-word list here is a small fixed teaching set (the 25 most
 *     common ones used as convention in many IR texts); real systems use
 *     longer curated lists per language.
 *   - Punctuation is left untouched on purpose (lab scope); production
 *     systems normalize tokens first, which stops "the." from escaping
 *     the filter - try entering "The cat, and the dog." to see the effect.
  *
 * COMMANDS (run from inside this folder):
 *   install dependencies : sudo apt install g++
 *   compile and run      : g++ -std=c++17 -Wall q2_StopWordRemoval.cpp -o q2_StopWordRemoval && ./q2_StopWordRemoval
*/

#include <iostream>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;

// The built-in stop word list (same words as the Python lab version).
const unordered_set<string> STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "in", "on", "at", "to", "of", "and", "or",
    "for", "with", "as", "by", "this", "that",
    "it", "from", "be", "has", "have", "had"
};

// Lowercase everything so tokens match the list reliably.
string toLower(const string& text) {
    string lowered;
    for (char c : text)
        lowered += static_cast<char>(tolower(static_cast<unsigned char>(c)));
    return lowered;
}

// Split the lowercase text into whitespace-separated tokens.
vector<string> tokenize(const string& text) {
    vector<string> words;
    istringstream stream(text);
    string word;
    while (stream >> word) words.push_back(word);
    return words;
}

// Keep only the tokens that are NOT stop words (order preserved).
vector<string> removeStopWords(const vector<string>& words) {
    vector<string> kept;
    for (const string& word : words) {
        if (STOP_WORDS.find(word) == STOP_WORDS.end())  // not a stop word
            kept.push_back(word);
    }
    return kept;
}

// Join the surviving tokens with single spaces for printing.
string join(const vector<string>& words) {
    string joined;
    for (size_t i = 0; i < words.size(); ++i) {
        if (i > 0) joined += ' ';
        joined += words[i];
    }
    return joined;
}

// Drives the whole practical; main() only calls this.
void run() {
    cout << "Enter the text document: ";
    string text;
    getline(cin, text);

    vector<string> words = tokenize(toLower(text));
    vector<string> filtered = removeStopWords(words);

    cout << "\nOriginal Text:\n" << toLower(text) << "\n";
    cout << "\nText after Stop Word Removal:\n" << join(filtered) << "\n";
}

int main() {
    run();
    return 0;
}
