# LP-3 Practical Solutions (Python / C++)

Solutions to the LP-3 laboratory questions. **DAA and IR questions have
both Python and C++ versions**; ML and CSDF are Python only (ML needs
scikit-learn / TensorFlow; CSDF's forensic scripts need Linux tools —
everything else runs on the bare standard library).

## Naming scheme (sorts .py before .cpp in every file explorer)

- `py<n>_<Topic>.py` — Python solution
- `q<n>_<Topic>.cpp` — C++ solution

File explorers sort case-insensitively, and `p` < `q`, so every Python
file appears first, followed by the C++ twins with the same question
number. Example: `py3_FractionalKnapsack.py`, then `q3_FractionalKnapsack.cpp`.

Style used in every file:

- The main entry point is one call to a `run()` driver function.
- Header comment block contains: the **QUESTION** (exact statement),
  **HOW IT WORKS** (algorithm explanation), **COMPLEXITY** (with
  reasoning) and **NOTES / INFO** (practical discussion points).
- Programs that need input prompt for it in the terminal.
- Every Python file is organised into numbered `STEP` sections:
  **STEP 1** imports, **STEP 2** creates the needed file/dataset from
  hardcoded data when one is required (ML scripts auto-create a small
  demo CSV if the real Kaggle dataset is absent — the demo CSVs have
  **exactly the same columns as the real datasets**, so dropping the
  real CSV in the folder works with no code change), later steps use
  and process it. C++ programs need no files, so their data is embedded.

## Folder structure

```
daa/   Design & Analysis of Algorithms   (.py + .cpp)
ir/    Information Retrieval             (.py + .cpp)
csdf/  Cyber Security & Digital Forensics (Python only)
ml/    Machine Learning                   (Python only)
```

## DAA — `daa/`

| Question | Python file | C++ file | Technique |
| --- | --- | --- | --- |
| Q1 Fibonacci (recursive + non-recursive, complexity analysis) | `py1_Fibonacci.py` | `q1_Fibonacci.cpp` | recursion vs iteration, O(2^n) vs O(n) |
| Q2 Huffman encoding (greedy) | `py2_HuffmanEncoding.py` | `q2_HuffmanEncoding.cpp` | min-heap merge tree, prefix codes |
| Q3 Fractional Knapsack (greedy) | `py3_FractionalKnapsack.py` | `q3_FractionalKnapsack.cpp` | sort by value/weight ratio |
| Q4 0/1 Knapsack (dynamic programming) | `py4_Knapsack01_DP.py` | `q4_Knapsack01_DP.cpp` | DP table + trace-back of items |
| Q5 N-Queens (first queen placed) | `py5_NQueens.py` | `q5_NQueens.cpp` | backtracking |
| Q6 Tower of Hanoi | `py6_TowerOfHanoi.py` | `q6_TowerOfHanoi.cpp` | recursion, 2^n - 1 moves |

Run any of them: `python3 "daa/py2_HuffmanEncoding.py"`
or build the C++ twin:
`g++ -std=c++17 -Wall -o bin/q2 "daa/q2_HuffmanEncoding.cpp" && ./bin/q2`

## IR — `ir/`

| Question | Python file | C++ file | Technique |
| --- | --- | --- | --- |
| Q1 Cosine similarity of two documents | `py1_CosineSimilarity.py` | `q1_CosineSimilarity.cpp` | word-frequency vectors, cosine |
| Q2 Stop-word removal | `py2_StopWordRemoval.py` | `q2_StopWordRemoval.cpp` | tokenizing + hash-set filter |
| Q3 MapReduce character counting | `py3_MapReduce.py` | `q3_MapReduce.cpp` | map, shuffle & sort, reduce |
| Q4 PageRank | `py4_PageRank.py` | `q4_PageRank.cpp` | power iteration, damping 0.85 |
| Q5 Topic-sensitive PageRank | `py5_TopicSensitivePageRank.py` | `q5_TopicSensitivePageRank.cpp` | XML graph, personalization vector, dangling-mass handling |

Run any of them: `python3 "ir/py1_CosineSimilarity.py"`
or build the C++ twin:
`g++ -std=c++17 -Wall -o bin/q1 "ir/q1_CosineSimilarity.cpp" && ./bin/q1`

## CSDF — `csdf/`

| Question | Python file | Requirements |
| --- | --- | --- |
| Q1 CAPTCHA generation + verification | `py1_Captcha.py` | none (pure stdlib — builds the PNG by hand) |
| Q2 Email header analysis | `py2_EmailHeaderAnalysis.py` | standard library only |
| Q3 Log capture & event correlation | `py3_LogCapture_EventCorrelation.py` | standard library only (writes `system.log`) |
| Q4 File recovery (dd → fls → istat → icat) | `py4_FileRecovery.py` | Sleuth Kit (`sudo apt install sleuthkit`) |
| Q5 Partition recovery (fdisk → TestDisk) | `py5_PartitionRecovery.py` | TestDisk (`sudo apt install testdisk`) |

Run any of them: `python3 "csdf/py2_EmailHeaderAnalysis.py"`

## ML — `ml/`

| Question | Python file | Dataset needed (in this directory) |
| --- | --- | --- |
| Q1 Uber fare prediction (preprocess, outliers, correlation, Linear + Random Forest, R2/RMSE) | `py1_UberRegression.py` | `uber.csv` |
| Q2 Email spam classification (KNN + SVM on the Kaggle word-count features) | `py2_SpamKNN_SVM.py` | `emails.csv` |
| Q3 Customer churn neural network (dropout + early stopping) | `py3_ChurnNN.py` | `Churn_Modelling.csv`, TensorFlow |
| Q4 Gradient descent on y = (x+3)^2 | `py4_GradientDescent.py` | none |
| Q5 Diabetes KNN (confusion matrix, accuracy, error rate, precision, recall) | `py5_DiabetesKNN.py` | `diabetes.csv` |

Python packages:

```bash
python3 -m pip install numpy pandas scikit-learn   # Q1, Q2, Q5
python3 -m pip install tensorflow                  # Q3 only
```

No other third-party packages are used anywhere — charts are rendered as
ASCII art in the terminal and the CAPTCHA PNG is written by hand.

Run any of them: `python3 "ml/py5_DiabetesKNN.py"`

## Safety note (forensics)

`py4_FileRecovery.py` and `py5_PartitionRecovery.py` touch real block
devices under `sudo`. Run only on media you own or are authorised to
examine, double-check device paths, and never run write/repair operations
inside TestDisk without a verified backup.
