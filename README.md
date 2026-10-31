# LP-3 Practical Solutions (Python / C++)

Solutions to the LP-3 laboratory questions. **DAA questions have both
Python and C++ versions**; ML is Python only (it needs
scikit-learn / TensorFlow); BT contains Solidity contracts deployed with
Remix + MetaMask on a free testnet. Everything else runs on the bare
standard library.

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
bt/    Blockchain Technology              (.sol + instructions)
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

## BT — `bt/`

| Practical | File | Type |
| --- | --- | --- |
| 1. Install MetaMask | `01_MetaMaskInstallation.md` | instructions |
| 2. Create a wallet with MetaMask | `02_CreateWallet.md` | instructions |
| 3. Smart contract for a bank account | `03_BankAccount.sol` | Solidity |
| 4. Smart contract with fallback + receive | `04_BankWithFallback.sol` | Solidity |
| 5. Survey report / real-time use cases | `05_SurveyReport.md` | report |

Deploy the contracts on the free **Sepolia testnet** with
[Remix IDE](https://remix.ethereum.org) and MetaMask — no toolchain needed.
Full steps, test cases and viva questions: [`bt/README.md`](bt/README.md).
Optional local compile: `npm install -g solc && solcjs --bin bt/03_BankAccount.sol`.

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
ASCII art in the terminal.

Run any of them: `python3 "ml/py5_DiabetesKNN.py"`
