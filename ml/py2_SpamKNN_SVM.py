"""
QUESTION 2 (ML):
Classify the email using the binary classification method (Normal = not
spam / Abnormal = spam). Use K-Nearest Neighbors and Support Vector
Machine for classification and analyze their performance.
Dataset: https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv

DATASET STRUCTURE (IMPORTANT): the REAL emails.csv is NOT raw text. It is
already a word-count matrix with 3002 columns:
    - "Email Text"  : the email id/name (numbers, not addresses)
    - 3000 columns  : the 3000 most common words; each cell is how many
                      times that word occurs in that email
    - "Label"       : 1 = spam, 0 = not spam
So the code trains KNN + SVM directly on the count features - no TF-IDF.

NOTE ON STEP 2: the hardcoded demo CSV mirrors that schema EXACTLY
(an id column + a small set of word-count columns + Label), and the code
treats every column except "Email Text"/"Label" as a feature, so dropping
the real Kaggle CSV in this folder works with no code change - just
better numbers (the real one simply has 3000 word columns instead of 14).

COMMANDS (run from the repository root):
    install dependencies : pip install pandas scikit-learn
    run the program      : python3 ml/py2_SpamKNN_SVM.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import os

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

DATASET_FILE = "emails.csv"


def ensure_dataset():
    """Use the real CSV if present; otherwise create the demo CSV."""
    if os.path.exists(DATASET_FILE):
        print(f"Using existing {DATASET_FILE}")
    else:
        with open(DATASET_FILE, "w") as file:
            file.write(DEMO_EMAILS_CSV)
        print(f"Created demo {DATASET_FILE} from hardcoded sample data")


# ============================================================
# STEP 3 : USE THE FILE - load, clean, and split X (word counts)
#          from y (Label). Every column except the id column and
#          the label IS a feature - exactly like the real file.
# ============================================================
def load_and_clean():
    """Read emails.csv, drop duplicates/blanks, show the class balance."""
    data = pd.read_csv(DATASET_FILE)

    print("Dataset Shape:", data.shape)
    print(data.head())

    # Tolerate older copies that name the columns differently.
    data = data.rename(columns={"Email name": "Email Text", "spam": "Label",
                                "text": "Email Text", "label": "Label"})

    before = data.shape[0]
    data = data.drop_duplicates().dropna().copy()
    print("\nCleaned Dataset Shape:", data.shape,
          f"({before - data.shape[0]} rows removed)")
    print("\nClass Distribution (1 = spam):")
    print(data["Label"].value_counts())

    y = data["Label"].astype(int)
    X = data.drop(columns=["Email Text", "Label"], errors="ignore")
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
    ensure_dataset()                                  # STEP 2
    X, y = load_and_clean()                           # STEP 3
    X_train, X_test, y_train, y_test = split_dataset(X, y)

    evaluate_model("KNN", KNeighborsClassifier(n_neighbors=5),      # STEP 4
                   X_train, X_test, y_train, y_test)
    evaluate_model("SVM", SVC(kernel="linear"),
                   X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    run()
