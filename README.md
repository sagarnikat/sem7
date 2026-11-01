# LP-3 Practical Solutions (DAA / ML / BT)

Solutions for the LP-3 laboratory assignments. The repository follows the
syllabus directly:

- **Group A — DAA:** assignments 1–6.
- **Group B — ML:** assignments 1–6.
- **Group C — BT:** practicals 1–6, including the Hyperledger business
  network.

DAA programs have Python and C++ versions. ML and BT use Python, Solidity,
JavaScript and Markdown instructions.

Every Python practical is written in **step blocks** using `# %%` markers:

```python
# %% Step 1: Imports
...
# %% Step 2: Create the demo dataset file
...
# %% Step 3: Load the dataset
...
```

This format works in both places:

- **Run the `.py` file normally** — Python ignores the `# %%` lines and the
  steps run from top to bottom.
- **Run it as notebook cells** — open the matching `.ipynb`, or use an
  editor that understands `# %%` cells (VS Code, JupyterLab with Jupytext,
  Spyder). Each block becomes one cell.

The `.ipynb` files are generated from these exact blocks, so the script and
the notebook always contain the same code.

## Naming scheme

| Prefix | Meaning |
| --- | --- |
| `py<n>_<Topic>.py` / `.ipynb` | Python assignment (step script + notebook) |
| `q<n>_<Topic>.cpp` | C++ twin of the same DAA assignment |
| `<nn>_<Topic>.sol` / `.md` | Blockchain contract or instruction document |

Python files sort before their C++ twins (`p` < `q`), so each assignment
appears as a pair in the file explorer.

Every program has a header block with the **QUESTION**, **HOW IT WORKS**,
**COMPLEXITY** and **NOTES** sections. ML datasets are looked up in
`ml/dataset/` first, then next to the script, then in the current directory.
If a dataset is missing, a small demo file with the same required columns is
created so the program still runs end to end.

## Folder structure

```
daa/   Design & Analysis of Algorithms   (Python + C++)
ml/    Machine Learning                   (Python)
  dataset/  original Kaggle CSV files
bt/    Blockchain Technology              (Solidity + JS + docs)
```

## Running in Jupyter

Install Jupyter once:

```bash
python3 -m pip install notebook
# or: python3 -m pip install jupyterlab
```

Start it from a practical folder so the dataset paths resolve:

```bash
cd ml
jupyter notebook          # or: jupyter lab
```

Then open the `.ipynb` file and run the cells from top to bottom
(**Run → Run All Cells** also works). Notes:

- Each step is a separate cell, so the output of every stage is visible.
- DAA scripts use an editable input step (`n = 25`, `N = 4`, the item list,
  or the text string) instead of `input()`. Change the value, then re-run
  that cell and the cells below it.
- ML scripts use two separate steps: **Step 2** only *creates* a demo CSV if
  the real dataset is missing, and **Step 3** loads the dataset. When
  `ml/dataset/<file>` already exists, Step 2 prints `Step 2 skipped` and you
  can ignore it — Step 3 finds and loads the file by itself. Start Jupyter
  from `ml/` so the relative paths resolve.
- Outputs are not saved in the notebooks; run them to generate the results
  for your journal.
- The `.py` files remain available for the command line and for the C++
  twins.

### Selecting the right kernel

Jupyter may start with a Python environment that does not have TensorFlow
or scikit-learn. Register the project environment once:

```bash
cd /home/sagar/code/collage
.venv/bin/python -m pip install ipykernel
.venv/bin/python -m ipykernel install --user \
  --name collage-venv --display-name "Python (collage .venv)"
```

Then in the notebook choose **Kernel → Change kernel → Python (collage
.venv)**. That kernel has all the packages used by this repository
(TensorFlow included). If you instead see
`ModuleNotFoundError: No module named 'tensorflow'`, the notebook is still
using the old kernel — switch it and restart.

## Group A — DAA (`daa/`)

| # | Assignment | Python | Notebook | C++ | Technique |
| --- | --- | --- | --- | --- | --- |
| 1 | Fibonacci (recursive + non-recursive) and complexity | `py1_Fibonacci.py` | `py1_Fibonacci.ipynb` | `q1_Fibonacci.cpp` | recursion vs iteration, O(2^n) vs O(n) |
| 2 | Huffman encoding | `py2_HuffmanEncoding.py` | `py2_HuffmanEncoding.ipynb` | `q2_HuffmanEncoding.cpp` | greedy, min-heap merge tree |
| 3 | Fractional knapsack | `py3_FractionalKnapsack.py` | `py3_FractionalKnapsack.ipynb` | `q3_FractionalKnapsack.cpp` | greedy by value/weight ratio |
| 4 | 0/1 knapsack | `py4_Knapsack01_DP.py` | `py4_Knapsack01_DP.ipynb` | `q4_Knapsack01_DP.cpp` | dynamic programming + trace-back |
| 5 | n-Queens with the first queen placed | `py5_NQueens.py` | `py5_NQueens.ipynb` | `q5_NQueens.cpp` | backtracking |
| 6 | Tower of Hanoi (recursive) and move-count analysis | `py6_TowerOfHanoi.py` | `py6_TowerOfHanoi.ipynb` | `q6_TowerOfHanoi.cpp` | recursion, divide and conquer, 2^n - 1 moves |

Run Python:

```bash
python3 daa/py6_TowerOfHanoi.py
```

Build C++ (the `bin` folder is created first):

```bash
mkdir -p bin
g++ -std=c++17 -O2 -Wall -o bin/q6 "daa/q6_TowerOfHanoi.cpp" && ./bin/q6
```

## Group B — ML (`ml/`)

| # | Assignment | File | Notebook | Dataset |
| --- | --- | --- | --- | --- |
| 1 | Uber fare prediction: preprocess, outliers, correlation, linear + random forest, R²/RMSE | `py1_UberRegression.py` | `py1_UberRegression.ipynb` | `uber.csv` |
| 2 | Spam classification with KNN + SVM | `py2_SpamKNN_SVM.py` | `py2_SpamKNN_SVM.ipynb` | `emails.csv` |
| 3 | Bank churn neural network (dropout + early stopping) | `py3_ChurnNN.py` | `py3_ChurnNN.ipynb` | `Churn_Modelling.csv`, TensorFlow |
| 4 | Gradient descent on `y = (x + 3)^2` | `py4_GradientDescent.py` | `py4_GradientDescent.ipynb` | none |
| 5 | Diabetes KNN: confusion matrix, accuracy, error rate, precision, recall | `py5_DiabetesKNN.py` | `py5_DiabetesKNN.ipynb` | `diabetes.csv` |
| 6 | K-Means clustering + elbow method | `py6_KMeansClustering.py` | `py6_KMeansClustering.ipynb` | `sales_data_sample.csv` |

All original datasets are already downloaded into **`ml/dataset/`**:

| File | Rows × columns | Source |
| --- | --- | --- |
| `dataset/uber.csv` | 200,000 × 9 | [Kaggle: uber-fares-dataset](https://www.kaggle.com/datasets/yasserh/uber-fares-dataset) |
| `dataset/emails.csv` | 5,172 × 3,002 | [Kaggle: email-spam-classification](https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv) |
| `dataset/Churn_Modelling.csv` | 10,000 × 14 | [Kaggle: bank-customer-churn-modeling](https://www.kaggle.com/barelydedicated/bank-customer-churn-modeling) |
| `dataset/diabetes.csv` | 768 × 9 | [Kaggle: diabetes](https://www.kaggle.com/datasets/abdallamahgoub/diabetes) |
| `dataset/sales_data_sample.csv` | 2,823 × 25 | [Kaggle: sample-sales-data](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data) |

They are gitignored (`*.csv`) because they are large; the download links above
let you fetch them again. The scripts look in this order:

1. `ml/dataset/<file>` — the normal location,
2. `<file>` next to the script,
3. `<file>` in the current working directory.

How the two dataset steps behave:

| Step | What it does | When the dataset already exists |
| --- | --- | --- |
| Step 2 | Writes a small demo CSV if no dataset file is found | Prints `Step 2 skipped` and does nothing — **the whole step can be skipped** |
| Step 3 | Locates the dataset (same three places) and loads it | Loads the real file; never depends on Step 2 having run |

Missing required columns produce a clear error instead of a `KeyError`.

To re-download everything (no Kaggle login needed for these public files):

```bash
mkdir -p ml/dataset && cd ml/dataset
curl -L -o uber.zip "https://www.kaggle.com/api/v1/datasets/download/yasserh/uber-fares-dataset"
unzip -o uber.zip
```

Python packages:

```bash
python3 -m pip install numpy pandas scikit-learn matplotlib   # Q1, Q2, Q5, Q6
python3 -m pip install tensorflow                             # Q3 only
```

Run any script:

```bash
python3 ml/py5_DiabetesKNN.py
python3 ml/py6_KMeansClustering.py
```

Every ML practical ends with a **Step N: Plots with matplotlib** cell, so the
graphs for that practical appear as real images (inline in Jupyter, in a
window when run as a script):

| Practical | Plots |
| --- | --- |
| Q1 Uber | distance vs fare, fare histogram, correlation heatmap, actual vs predicted (linear + random forest) |
| Q2 Spam | KNN and SVM confusion matrices, metric comparison bars |
| Q3 Churn | accuracy/loss training curves, baseline + improved confusion matrices |
| Q4 Gradient descent | descent steps on the parabola, convergence for each learning rate |
| Q5 Diabetes | confusion matrix, metric bars, accuracy vs k |
| Q6 K-Means | elbow curve, cluster scatter with centres, orders per cluster |

## Group C — BT (`bt/`)

| # | Practical | File |
| --- | --- | --- |
| 1 | Install MetaMask + study Ether spent per transaction | `01_MetaMaskInstallation.md` |
| 2 | Create your own wallet with MetaMask | `02_CreateWallet.md` |
| 3 | Bank account contract: deposit, withdraw, show balance | `03_BankAccount.sol` |
| 4 | Student data with structs, arrays and fallback + gas observation | `04_StudentData.sol` |
| 5 | Survey: types of blockchains and real-time use cases | `05_SurveyReport.md` |
| 6 | Business network on Hyperledger Fabric | `06_HyperledgerBusinessNetwork/` |

Full deployment steps, test cases, expected outputs, gas tables and viva
questions: [`bt/README.md`](bt/README.md). Contracts are deployed with
[Remix](https://remix.ethereum.org) and MetaMask on the free **Sepolia**
testnet. Optional local compile:

```bash
npm install -g solc
solcjs --bin bt/03_BankAccount.sol bt/04_StudentData.sol
```

The Hyperledger practical includes JavaScript chaincode plus exact Fabric
`test-network` commands.

## Safety

- Use a dedicated test wallet with Sepolia ETH only; never reuse a wallet
  that holds real funds.
- Never share the Secret Recovery Phrase or private key, including in
  screenshots or reports.
- Test ETH has no real value.
- Confirm the network in MetaMask before signing a transaction.
