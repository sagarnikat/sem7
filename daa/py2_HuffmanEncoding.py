"""
QUESTION 2 (DAA):
Write a program to implement Huffman Encoding using a greedy strategy.

HOW IT WORKS
    1. Count the frequency of every character in the text.
    2. Put every character into a min-priority queue keyed by frequency.
    3. Greedy step: remove the two least frequent nodes, merge them under a
       parent whose frequency is their sum, and push the parent back.
    4. Label the finished tree: left edge = 0, right edge = 1. The code of a
       character is the path from the root to its leaf.
    5. Encoding joins the character codes; decoding walks the tree bit by bit.
       No code is a prefix of another, so decoding is unambiguous.

STEPS
    1. Imports
    2. Input text
    3. Tree node
    4. Build the Huffman tree
    5. Generate the codes
    6. Encode and decode
    7. Run the full pipeline
    8. Observation

RUN
    python3 daa/py2_HuffmanEncoding.py

    In Jupyter, open py2_HuffmanEncoding.ipynb or split this file at the
    "# %%" markers.
"""

# %% Step 1: Imports
import heapq
from collections import Counter

# %% Step 2: Input text
# Change the text and re-run this cell plus the steps below it.
text = "huffman coding is a greedy algorithm"

# %% Step 3: Tree node
class Node:
    """Huffman tree node: a leaf (character) or a merged internal node."""

    def __init__(self, frequency, symbol=None, left=None, right=None):
        self.frequency = frequency
        self.symbol = symbol
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

    def __lt__(self, other):
        return self.frequency < other.frequency

# %% Step 4: Build the Huffman tree
def build_tree(text):
    """Greedy part: merge the two least frequent nodes until one root remains."""
    frequencies = Counter(text)
    heap = [Node(freq, symbol=ch) for ch, freq in frequencies.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        only = heapq.heappop(heap)
        return Node(only.frequency, left=only)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = Node(left.frequency + right.frequency, left=left, right=right)
        heapq.heappush(heap, parent)
    return heap[0]

# %% Step 5: Generate the codes
def generate_codes(node, code="", table=None):
    """Walk the tree: left = 0, right = 1; leaves collect their codes."""
    if table is None:
        table = {}
    if node.is_leaf():
        table[node.symbol] = code or "0"
        return table
    generate_codes(node.left, code + "0", table)
    generate_codes(node.right, code + "1", table)
    return table

# %% Step 6: Encode and decode
def encode(text, codes):
    """Replace every character by its variable-length code."""
    return "".join(codes[ch] for ch in text)

def decode(encoded, root):
    """Walk the tree one bit at a time; a leaf emits one character."""
    decoded, node = [], root
    for bit in encoded:
        node = node.left if bit == "0" else node.right
        if node.is_leaf():
            decoded.append(node.symbol)
            node = root
    return "".join(decoded)

# %% Step 7: Run the full pipeline
root = build_tree(text)
codes = generate_codes(root)

print("Huffman Codes:")
for char, code_value in sorted(codes.items()):
    display = "[space]" if char == " " else char
    print(f"  {display} : {code_value}")

encoded = encode(text, codes)
decoded = decode(encoded, root)

print(f"\nOriginal text : {text}")
print(f"Encoded text  : {encoded}")
print(f"Decoded text  : {decoded}")
print(f"Bits: {len(text) * 8} (ASCII) -> {len(encoded)} (Huffman)")
print(f"Compression   : {len(encoded) / (len(text) * 8) * 100:.1f}% of ASCII")

# %% Step 8: Observation
print("\nObservation")
print("  The most frequent characters get the shortest codes. No code is a")
print("  prefix of another, so the decoder never has to guess where a code ends.")
