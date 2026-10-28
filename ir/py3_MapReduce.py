"""
QUESTION 3 (IR):
Write a program to demonstrate the MapReduce framework (map, shuffle/sort
and reduce phases) by counting alphabetic characters in a sample string.

HOW IT WORKS - THE THREE PHASES:
1. MAP       - every alphabetic character emits a (letter, 1) pair.
               Mappers are independent, so in a real cluster they run in
               parallel on different machines.
2. SHUFFLE & SORT - all pairs with the same key are routed to one place
               and grouped: 'a' -> [1, 1, 1], 'b' -> [1], ...
3. REDUCE    - each key is reduced once: sum its list of values -> the
               final per-key count.

WHY IT MATTERS: map and reduce tasks are embarrassingly parallel, so the
same code scales from one machine to thousands just by shuffling pairs.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 ir/py3_MapReduce.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
from collections import defaultdict


# ============================================================
# STEP 2 : HARDCODED DATA - the sample string (the "dataset" here)
# ============================================================
SAMPLE_DATA = """
Hello World!
This is an Information Retrieval assignment.
MapReduce counts alphabetic characters.
Hello Python!
"""


# ============================================================
# STEP 3 : THE THREE MAPREDUCE PHASES (use the data above)
# ============================================================
def map_phase(data):
    """MAP: every alphabetic character becomes a (lowercased letter, 1)."""
    mapped = []
    for character in data:
        if character.isalpha():
            mapped.append((character.lower(), 1))
    return mapped


def shuffle_and_sort_phase(mapped):
    """SHUFFLE & SORT: group all the 1s by key; sorted keys keep order."""
    grouped = defaultdict(list)
    for letter, count in mapped:
        grouped[letter].append(count)
    return dict(sorted(grouped.items()))


def reduce_phase(grouped):
    """REDUCE: sum the list of values for every key -> final counts."""
    return {letter: sum(counts) for letter, counts in grouped.items()}


# ============================================================
# STEP 4 : DRIVER - run map -> shuffle&sort -> reduce -> print
# ============================================================
def run():
    mapped = map_phase(SAMPLE_DATA)                    # phase 1
    grouped = shuffle_and_sort_phase(mapped)           # phase 2
    result = reduce_phase(grouped)                     # phase 3

    print("Character Occurrence Count")
    print("---------------------------")
    for letter, count in result.items():
        print(letter, ":", count)


if __name__ == "__main__":
    run()
