"""
QUESTION 4 (IR):
Write a program to calculate the PageRank of a small directed web graph.

HOW IT WORKS (POWER ITERATION):
A page's importance depends on the importance of the pages LINKING to it:
every page splits its own rank equally among its outgoing links.
1. Start with rank[i] = 1/n for all n pages.
2. Every iteration:
       newRank[j] = (1 - d)/n + d * sum(rank[i] / outDegree(i))
                    for every i that links to j
   d = damping factor 0.85: with probability d a random surfer follows a
   link, otherwise jumps to ANY page - that (1-d)/n base keeps the method
   converging and gives pages with no inbound links a non-zero floor.
3. Repeat for a fixed number of iterations; values converge to the
   principal eigenvector of the normalised link matrix.

COMMANDS (run from the repository root):
    install dependencies : none (Python standard library only)
    run the program      : python3 ir/py4_PageRank.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
# none - this program needs only the standard built-ins


# ============================================================
# STEP 2 : HARDCODED DATA - the web graph (the "dataset" here)
# GRAPH[i][j] = 1 if page i links to page j.
#   page 1 -> 2, 3 ; page 2 -> 3 ; page 3 -> 1, 4 ; page 4 -> 1
# ============================================================
DAMPING = 0.85
ITERATIONS = 100

GRAPH = [
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 0],
]


# ============================================================
# STEP 3 : USE THE DATA - the power-iteration algorithm
# ============================================================
def page_rank(graph, damping=DAMPING, iterations=ITERATIONS):
    """Power iteration: distribute each page's rank along its links."""
    n = len(graph)
    rank = [1 / n] * n                            # uniform start

    for _ in range(iterations):
        new_rank = [(1 - damping) / n] * n        # teleport base value

        for i in range(n):
            outgoing = sum(graph[i])              # links leaving page i
            if outgoing == 0:
                continue
            for j in range(n):
                if graph[i][j] == 1:
                    new_rank[j] += damping * rank[i] / outgoing
        rank = new_rank
    return rank


# ============================================================
# STEP 4 : DRIVER - run PageRank and print values + final ranking
# ============================================================
def run():
    ranks = page_rank(GRAPH)

    print("PageRank Values:")
    for i, value in enumerate(ranks):
        print("Page", i + 1, ":", round(value, 6))

    ranking = sorted(range(len(ranks)), key=lambda i: ranks[i], reverse=True)
    print("\nPage Ranking:")
    for position, page in enumerate(ranking, start=1):
        print(position, "-> Page", page + 1)


if __name__ == "__main__":
    run()
