"""
QUESTION 2 (DAA):
Write a program to implement Huffman Encoding using a greedy strategy.

HOW IT WORKS (GREEDY TREE CONSTRUCTION):
1. Count the frequency of every character in the text.
2. Put every character into a min-priority-queue keyed by frequency.
3. GREEDY STEP: repeatedly remove the TWO least frequent nodes, merge them
   under a parent whose frequency is their sum, and push it back. Merging
   the rarest nodes first pushes them DEEPEST into the tree, which
   minimises the total encoded length -> greedy is provably optimal here.
4. Label the finished tree: left edge adds a '0', right edge a '1'. The
   code of a character = path from root to its leaf.
5. ENCODING = concatenating each character's code; DECODING = walking the
   tree from the root bit by bit until a leaf is hit. The prefix property
   (no code is a prefix of another) makes decoding unambiguous.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 daa/py2_HuffmanEncoding.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import heapq
from collections import Counter


# ============================================================
# STEP 2 : HUFFMAN TREE NODE + GREedy CONSTRUCTION FUNCTIONS
# ============================================================
class Node:
    """Huffman tree node: a leaf (character) or a merged internal node."""

    def __init__(self, frequency, symbol=None, left=None, right=None):
        self.frequency = frequency  # total frequency of this subtree
        self.symbol = symbol        # only set for leaves
        self.left = left            # branch taken with bit '0'
        self.right = right          # branch taken with bit '1'

    def is_leaf(self):
        return self.left is None and self.right is None

    def __lt__(self, other):        # lets heapq order nodes by frequency
        return self.frequency < other.frequency


def build_tree(text):
    """Greedy part: merge the two least frequent nodes until one root remains."""
    frequencies = Counter(text)                       # count every character
    heap = [Node(freq, symbol=ch) for ch, freq in frequencies.items()]
    heapq.heapify(heap)                               # min-heap by frequency

    # Special case: only one unique character in the whole text.
    if len(heap) == 1:
        only = heapq.heappop(heap)
        return Node(only.frequency, left=only)

    while len(heap) > 1:                              # greedy merge loop
        left = heapq.heappop(heap)                    # rarest node
        right = heapq.heappop(heap)                   # second rarest node
        parent = Node(left.frequency + right.frequency, left=left, right=right)
        heapq.heappush(heap, parent)
    return heap[0]


def generate_codes(node, code="", table=None):
    """Walk the tree: left = '0', right = '1'; leaves collect their codes."""
    if table is None:
        table = {}
    if node.is_leaf():
        table[node.symbol] = code or "0"   # single-character edge case
        return table
    generate_codes(node.left, code + "0", table)
    generate_codes(node.right, code + "1", table)
    return table


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
            node = root                    # restart for the next character
    return "".join(decoded)


# ============================================================
# STEP 3 : DRIVER - build tree, show codes, encode + decode
# ============================================================
def run():
    text = input("Enter text: ").strip()
    if not text:
        print("Text cannot be empty.")
        return

    root = build_tree(text)
    codes = generate_codes(root)

    print("\nHuffman Codes:")
    for char, code in sorted(codes.items()):
        display = "[space]" if char == " " else char
        print(f"  {display} : {code}")

    encoded = encode(text, codes)
    decoded = decode(encoded, root)

    print(f"\nOriginal text : {text}")
    print(f"Encoded text  : {encoded}")
    print(f"Decoded text  : {decoded}")
    print(f"Bits: {len(text) * 8} (ASCII) -> {len(encoded)} (Huffman)")


if __name__ == "__main__":
    run()
