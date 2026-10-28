# LP-3 Practical Codes (C++ / Python rewrite)

My own implementations of the LP-3 (DAA, IR, CSDF, ML) practical problem
statements, rewritten in **C++** where possible and **Python** elsewhere.
Every problem statement was sourced from
[Aryan-123-app/lp3-practical-codes](https://github.com/Aryan-123-app/lp3-practical-codes)
and re-implemented from scratch.

## Conventions used in every file

| Rule | Detail |
| --- | --- |
| `main()` is one function call | All logic lives in a `run()`-style driver function. |
| Header comment block | Every file opens with `PROBLEM STATEMENT`, `HOW IT WORKS` (algorithm explanation), `COMPLEXITY` (with why) and `NOTES / INFO`. |
| Interactive input | Programs prompt in the terminal, exactly like the original exercises. |

## Contents

### `daa/` — Design & Analysis of Algorithms (C++)

| File | Problem | Ideas / Tags |
| --- | --- | --- |
| `FractionalKnapsack.cpp` | Greedy fractional knapsack | sort by value/weight ratio, O(n log n) |
| `KnapsackDP.cpp` | 0/1 knapsack (dynamic programming) | bottom-up DP table + trace-back of chosen items, O(n·W) |
| `HuffmanCoding.cpp` | Huffman encoding | min-priority-queue merge tree, encode/decode menu |
| `NQueens.cpp` | N-Queens | backtracking; first queen permanently fixed at (0,0) (lab constraint) |
| `TowerOfHanoi.cpp` | Tower of Hanoi | divide & conquer recursion, 2ⁿ−1 moves |
| `FibonacciComparison.cpp` | Fibonacci | iterative O(n) vs recursive O(2ⁿ) timing lesson |

Build and run (no external libraries needed):

```bash
g++ -std=c++17 -Wall -o bin/FractionalKnapsack "daa/FractionalKnapsack.cpp" && ./bin/FractionalKnapsack
```

### `ir/` — Information Retrieval (C++)

| File | Problem | Ideas / Tags |
| --- | --- | --- |
| `CosineSimilarity.cpp` | Document similarity | word-frequency vectors, cosine of the vector angle |
| `MapReduce.cpp` | MapReduce word/char count | map → shuffle & sort → reduce phases |
| `PageRankAlgo.cpp` | PageRank | power iteration, damping factor 0.85 |
| `StopWordRemoval.cpp` | Stop-word removal | hash-set token filter (preprocessing step) |
| `TopicPageRank.cpp` | Topic-sensitive PageRank | hand-rolled XML parse, personalized vector + dangling-mass handling |

Build and run exactly like the DAA programs:

```bash
g++ -std=c++17 -Wall -o bin/CosineSimilarity "ir/CosineSimilarity.cpp" && ./bin/CosineSimilarity
```

### `csdf/` — Cyber Security & Digital Forensics

| File | Problem | Language | Why not C++ |
| --- | --- | --- | --- |
| `EmailHeaderAnalysis.cpp` | Email-header / Received-chain analysis, IPv4 extraction | C++ | — |
| `LogCaptureEventCorrelation.cpp` | Log capture + event correlation, flag IP with ≥ 3 failed logins | C++ | — |
| `Captcha.py` | CAPTCHA generation & verification | Python | image rendering needs Pillow |
| `FileRecovery.py` | Deleted-file recovery (dd → fls → istat → icat) | Python | orchestrates Sleuth Kit utilities |
| `PartitionRecovery.py` | Partition recovery inspection (lsblk → fdisk → testdisk) | Python | orchestrates Linux forensic tools |

C++ programs build as above. Python prerequisites:

```bash
sudo apt install python3-pil sleuthkit testdisk   # Pillow + forensic tools
```

### `ml/` — Machine Learning (Python)

Each script mirrors one notebook from the reference repository. Datasets
are **not** included — download them yourself and place them in the working
directory:

| Script | Experiment | Dataset needed |
| --- | --- | --- |
| `GradientDescent.py` | Gradient descent on f(x) = (x + 3)² | none (pure Python) |
| `DiabetesKNN.py` | Diabetes classification with KNN (k = 5), scaling, all metrics | `diabetes.csv` |
| `KNNandSVM.py` | Spam classification with TF-IDF + KNN vs linear SVM | `emails.csv` (`text`, `spam`) |
| `UberRegression.py` | Uber fare prediction: cleaning, Haversine distance, IQR outliers, Linear vs Random Forest | `uber.csv` |
| `ChurnNN.py` | Customer churn with a Keras network: base model vs dropout + early stopping | `Churn_Modelling.csv` (TensorFlow needed) |

Python prerequisites:

```bash
python3 -m pip install pandas numpy matplotlib seaborn scikit-learn
python3 -m pip install tensorflow        # only for ChurnNN.py
python3 "ml/DiabetesKNN.py"
```

## Verified

- All `daa/`, `ir/`, `csdf/` C++ files compile clean with
  `g++ -std=c++17 -Wall` and were smoke-tested with valid input
  (knapsack answers, Huffman round-trip, N=8 solution, PageRank ranks).
- All Python scripts pass `python3 -m py_compile`.
- The `prac1.cpp` … `prac6.cpp` files in `daa/` are an earlier, separate
  set of attempts (Fibonacci, quicksort, …) kept for reference.

## Safety note (forensics)

`FileRecovery.py` and `PartitionRecovery.py` touch real block devices with
`sudo`. Work only on media you own or are authorised to examine, double-check
device paths, and never run write/repair operations inside TestDisk without a
verified backup.
