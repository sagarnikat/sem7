"""
QUESTION 2 (ML):
Classify the email using the binary classification method (Normal = not
spam / Abnormal = spam). Use K-Nearest Neighbors and Support Vector
Machine for classification and analyze their performance.
Dataset: https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv

NOTE ON STEP 2: if the real emails.csv is not present, a small HARDCODED
demo dataset (a handful of obvious spam + normal mails) is written to
emails.csv so the pipeline runs end-to-end. Drop the real Kaggle CSV in
this folder for real-world numbers.

COMMANDS (run from the repository root):
    install dependencies : pip install pandas scikit-learn
    run the program      : python3 ml/py2_SpamKNN_SVM.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (accuracy_score, classification_report,
                             f1_score, precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


# ============================================================
# STEP 2 : CREATE THE DATASET FILE - if emails.csv is missing,
#          write a small HARDCODED demo dataset (spam mails with
#          prize/offer wording, normal mails without)
# ============================================================
DEMO_EMAILS_CSV = """text,spam
"Congratulations! You have WON a free prize. Claim your cash reward now by clicking this link",1
"URGENT: your account is locked. Verify your billing details immediately to avoid suspension",1
"You are our lucky winner! Exclusive offer: free vacation, claim today, limited time only",1
"Get rich quick! Make cash from home with this amazing investment opportunity, act now",1
"Free entry in a weekly competition to win a prize. Text WIN to participate now",1
"Discount offer: buy one get one free on all products. Limited stock, order now",1
"Hi team, the project meeting is moved to 3 PM tomorrow. Please review the agenda before we meet",0
"Reminder: your dentist appointment is scheduled for Friday at 10 AM. Reply to reschedule",0
"The quarterly report is attached. Let me know if you need any changes before the review",0
"Thanks for your order. Your package has been shipped and will arrive on Tuesday",0
"Can we reschedule our call to next week? I am traveling for a conference until Thursday",0
"Your monthly statement is ready. You can view it anytime from the account portal",0
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
# STEP 3 : USE THE FILE - load, clean, split, vectorize (TF-IDF)
# ============================================================
def load_and_clean():
    """Read emails.csv, drop duplicates/blanks, show the class balance."""
    data = pd.read_csv(DATASET_FILE)

    print("Dataset Shape:", data.shape)
    print(data.head())

    before = data.shape[0]
    data = data.drop_duplicates().dropna(subset=["text", "spam"]).copy()
    print("\nCleaned Dataset Shape:", data.shape,
          f"({before - data.shape[0]} rows removed)")
    print("\nClass Distribution:")
    print(data["spam"].value_counts())
    return data["text"], data["spam"]


def split_and_vectorize(X, y):
    """80/20 stratified split; TF-IDF fitted on the training fold only."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    print("Training TF-IDF shape:", X_train_tfidf.shape)
    print("Testing TF-IDF shape:", X_test_tfidf.shape)
    return X_train_tfidf, X_test_tfidf, y_train, y_test


# ============================================================
# STEP 4 : TRAIN + EVALUATE THE TWO CLASSIFIERS (KNN vs SVM)
# ============================================================
def evaluate_model(name, model, X_train_tfidf, X_test_tfidf, y_train, y_test):
    """Fit one classifier and print its full metric block."""
    model.fit(X_train_tfidf, y_train)
    y_pred = model.predict(X_test_tfidf)

    print(f"\n----- {name} PERFORMANCE -----")
    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred, zero_division=0))
    print("Recall   :", recall_score(y_test, y_pred, zero_division=0))
    print("F1 Score :", f1_score(y_test, y_pred, zero_division=0))
    print(f"\nClassification Report - {name}")
    print(classification_report(y_test, y_pred, zero_division=0))


# ============================================================
# STEP 5 : DRIVER - create dataset -> vectorize -> KNN vs SVM
# ============================================================
def run():
    ensure_dataset()                                        # STEP 2
    X, y = load_and_clean()                                 # STEP 3
    X_train_tfidf, X_test_tfidf, y_train, y_test = split_and_vectorize(X, y)

    evaluate_model("KNN", KNeighborsClassifier(n_neighbors=5),    # STEP 4
                   X_train_tfidf, X_test_tfidf, y_train, y_test)
    evaluate_model("SVM", SVC(kernel="linear"),
                   X_train_tfidf, X_test_tfidf, y_train, y_test)


if __name__ == "__main__":
    run()