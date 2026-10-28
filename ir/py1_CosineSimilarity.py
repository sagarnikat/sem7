"""
QUESTION 1 (IR):
Write a program to compare two documents using cosine similarity.

HOW IT WORKS:
1. Preprocess both documents: lowercase, strip non-alphanumeric characters,
   split into words ("Hello, World!" and "hello world" become equal).
2. Build a word-frequency vector for each document (one dimension per
   distinct word in the union vocabulary).
3. Cosine similarity = angle between the two vectors:
        similarity = (D1 . D2) / (|D1| * |D2|)
   - dot product: sum over the vocabulary of f1[w] * f2[w] (words missing
     from a document contribute 0),
   - magnitudes: sqrt of the sum of squared frequencies.
4. Range: 1.0 = same word distribution, 0.0 = nothing shared. Document
   LENGTH cancels out - a long article and its abstract can still score
   high, which is what makes cosine the standard IR similarity.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 ir/py1_CosineSimilarity.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import math
import re
from collections import Counter


# ============================================================
# STEP 2 : PREPROCESSING + SIMILARITY FUNCTIONS (no files needed)
# ============================================================
def preprocess(text):
    """Lowercase, keep [a-z0-9] only (others become spaces), split into words."""
    cleaned = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    return cleaned.split()


def cosine_similarity(doc1, doc2):
    """Cosine of the angle between the two word-frequency vectors."""
    freq1, freq2 = Counter(preprocess(doc1)), Counter(preprocess(doc2))
    vocabulary = set(freq1) | set(freq2)          # union vocabulary

    dot_product = sum(freq1[w] * freq2[w] for w in vocabulary)
    magnitude1 = math.sqrt(sum(freq1[w] ** 2 for w in vocabulary))
    magnitude2 = math.sqrt(sum(freq2[w] ** 2 for w in vocabulary))

    if magnitude1 == 0 or magnitude2 == 0:        # empty document guard
        return 0.0
    return dot_product / (magnitude1 * magnitude2)


# ============================================================
# STEP 3 : DRIVER - read the two documents and print similarity
# ============================================================
def run():
    doc1 = input("Enter first document: ")
    doc2 = input("Enter second document: ")

    similarity = cosine_similarity(doc1, doc2)
    print(f"\nCosine Similarity = {round(similarity, 4)}")
    print(f"Similarity Percentage = {round(similarity * 100, 2)} %")


if __name__ == "__main__":
    run()
