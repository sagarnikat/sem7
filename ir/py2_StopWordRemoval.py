"""
QUESTION 2 (IR):
Write a program to remove stop words from a given text document.

HOW IT WORKS:
1. Lowercase the text (so "The" and "the" both match the stop list).
2. Tokenize by splitting on whitespace.
3. Drop every token found in the fixed stop-word set; keep the rest in
   their original order.

WHY THIS STEP EXISTS (the IR point):
Stop words ("the", "is", "at", ...) appear in almost every document, so
they cannot distinguish documents from each other. Removing them shrinks
the index, speeds up later scoring, and removes noise before ranking.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 ir/py2_StopWordRemoval.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
# none - this program needs only the standard built-ins


# ============================================================
# STEP 2 : HARDCODED DATA - the stop-word set (the "dataset" here)
# ============================================================
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "in", "on", "at", "to", "of", "and", "or",
    "for", "with", "as", "by", "this", "that",
    "it", "from", "be", "has", "have", "had",
}


# ============================================================
# STEP 3 : USE THE DATA - filter the tokens of the input text
# ============================================================
def remove_stop_words(text):
    """Tokenize lowercase text and keep only non-stop-word tokens."""
    words = text.lower().split()
    return [word for word in words if word not in STOP_WORDS]


# ============================================================
# STEP 4 : DRIVER - read a document, filter, show before/after
# ============================================================
def run():
    text = input("Enter the text document: ")

    filtered = remove_stop_words(text)

    print("\nOriginal Text:")
    print(text.lower())
    print("\nText after Stop Word Removal:")
    print(" ".join(filtered))


if __name__ == "__main__":
    run()
