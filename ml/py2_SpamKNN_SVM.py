"""
QUESTION 2 (ML):
Classify the email using the binary classification method (Normal = not
spam / Abnormal = spam). Use K-Nearest Neighbors and Support Vector
Machine for classification and analyze their performance.
Dataset: https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv

DATASET STRUCTURE (IMPORTANT): the REAL emails.csv is NOT raw text. It is
already a word-count matrix with 3002 columns:
    - "Email No."   : the email id/name (numbers, not addresses)
    - 3000 columns  : the 3000 most common words; each cell is how many
                      times that word occurs in that email
    - "Prediction"  : 1 = spam, 0 = not spam
Some copies rename these to "Email Text" and "Label"; both spellings are
accepted. The code trains KNN + SVM directly on the count features - no
TF-IDF.

NOTE ON STEP 2: the hardcoded demo CSV mirrors that schema EXACTLY
(an id column + a small set of word-count columns + label), and the code
treats every column except the id and label as a feature, so the real
Kaggle CSV in ml/ works with no code change - just better numbers (it has
3000 word columns instead of 14).

COMMANDS (run from the repository root):
    install dependencies : pip install pandas scikit-learn
    run the program      : python3 ml/py2_SpamKNN_SVM.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import os
import sys

import pandas as pd
from sklearn.metrics import (accuracy_score, classification_report,
                             f1_score, precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


# ============================================================
# STEP 2 : CREATE THE DATASET FILE - if emails.csv is missing,
#          write a small HARDCODED demo dataset with the SAME
#          structure as the real Kaggle file (id column +
#          word-count columns + 1/0 Label). The real file has
#          3000 word columns; the demo uses 14 frequent ones.
# ============================================================
DEMO_EMAILS_CSV = """Email Text,free,winner,offer,cash,prize,claim,urgent,click,meeting,report,schedule,attached,order,account,Label
1,2,1,1,2,1,1,1,2,0,0,0,0,0,1,1
2,1,0,2,1,0,1,2,1,0,0,0,0,0,2,1
3,3,2,1,2,1,1,0,1,0,0,0,0,0,0,1
4,0,1,1,2,0,1,1,0,0,0,0,0,1,1,1
5,1,1,0,1,2,1,0,1,0,0,0,0,0,0,1
6,2,0,2,0,1,0,1,1,0,0,0,0,1,0,1
7,0,0,0,0,0,0,0,0,2,2,1,1,0,0,0
8,0,0,0,0,0,0,0,0,1,1,2,1,0,0,0
9,0,0,0,0,0,0,0,0,2,3,0,2,0,0,0
10,0,0,0,0,0,0,0,1,0,0,0,0,2,1,0
11,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0
12,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0
13,1,0,0,0,0,0,0,0,2,0,1,1,0,0,0
14,0,0,1,0,0,0,0,0,1,2,0,1,0,0,0
"""

DATASET_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "emails.csv")


def find_dataset():
    """Return the CSV to use: ml/emails.csv first, then ./emails.csv."""
    if os.path.exists(DATASET_FILE):
        return DATASET_FILE
    local = os.path.abspath("emails.csv")
    if os.path.exists(local):
        return local
    return DATASET_FILE


def ensure_dataset():
    """Return the CSV to use; create the demo only when no file exists."""
    path = find_dataset()
    if os.path.exists(path):
        print(f"Using dataset: {path}")
        return path
    with open(DATASET_FILE, "w", encoding="utf-8") as file:
        file.write(DEMO_EMAILS_CSV)
    print(f"No emails.csv found - created demo dataset: {DATASET_FILE}")
    return DATASET_FILE


# ============================================================
# STEP 3 : USE THE FILE - load, clean, and split X (word counts)
#          from y (Label). Every column except the id column and
#          the label IS a feature - exactly like the real file.
# ============================================================
def load_and_clean(path=None):
    """Read emails.csv, normalise columns, show the class balance."""
    path = path or find_dataset()
    data = pd.read_csv(path)
    data.columns = [str(c).replace("\ufeff", "").strip()
                    for c in data.columns]

    # The Kaggle file uses "Email No." + "Prediction"; other copies use
    # "Email Text"/"Email name" + "Label"/"spam". Match exact names only:
    # the 3000 word-count columns are lower-case, so a word called "label"
    # or "spam" must NOT be mistaken for the target column.
    id_column = next((name for name in
                      ["Email No.", "Email Text", "Email name", "text", "id",
                       "Unnamed: 0"] if name in data.columns), None)
    label_column = next((name for name in ["Prediction", "Label", "spam"]
                         if name in data.columns), None)
    if label_column is None and str(data.columns[-1]).lower() in {
            "label", "prediction", "spam"}:
        label_column = data.columns[-1]

    rename = {}
    if id_column is not None:
        rename[id_column] = "Email Text"
    if label_column is not None:
        rename[label_column] = "Label"
    data = data.rename(columns=rename)

    if "Label" not in data.columns:
        print("\nERROR: no label column found (expected 'Prediction', "
              "'Label' or 'spam').", file=sys.stderr)
        print(f"Columns found (first 10): {list(data.columns)[:10]}",
              file=sys.stderr)
        raise SystemExit(1)

    print(f"\nFile: {path}")
    print("Dataset Shape:", data.shape)
    print("\nFirst 5 rows (first 6 columns only):")
    print(data.iloc[:5, :6])

    before = data.shape[0]
    data = data.drop_duplicates().dropna().copy()
    print("\nCleaned Dataset Shape:", data.shape,
          f"({before - data.shape[0]} rows removed)")
    print("\nClass Distribution (1 = spam):")
    print(data["Label"].value_counts())

    y = pd.to_numeric(data["Label"], errors="coerce").astype("Int64")
    X = data.drop(columns=["Email Text", "Label"], errors="ignore")
    X = X.apply(pd.to_numeric, errors="coerce")
    valid = y.notna() & X.notna().all(axis=1)
    X, y = X[valid].astype(float), y[valid].astype(int)

    print("\nNumber of word-count features:", X.shape[1])
    return X, y


def split_dataset(X, y):
    """80/20 stratified split of the word-count features."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))
    print("Features per sample:", X_train.shape[1])
    return X_train, X_test, y_train, y_test


# ============================================================
# STEP 4 : TRAIN + EVALUATE THE TWO CLASSIFIERS (KNN vs SVM)
# ============================================================
def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    """Fit one classifier and print its full metric block."""
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(f"\n----- {name} PERFORMANCE -----")
    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred, zero_division=0))
    print("Recall   :", recall_score(y_test, y_pred, zero_division=0))
    print("F1 Score :", f1_score(y_test, y_pred, zero_division=0))
    print(f"\nClassification Report - {name}")
    print(classification_report(y_test, y_pred, zero_division=0))


# ============================================================
# STEP 5 : DRIVER - create dataset -> split -> KNN vs SVM
# ============================================================
def run():
    path = ensure_dataset()                           # STEP 2
    X, y = load_and_clean(path)                       # STEP 3
    X_train, X_test, y_train, y_test = split_dataset(X, y)

    evaluate_model("KNN", KNeighborsClassifier(n_neighbors=5),      # STEP 4
                   X_train, X_test, y_train, y_test)
    evaluate_model("SVM", SVC(kernel="linear"),
                   X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    run()
