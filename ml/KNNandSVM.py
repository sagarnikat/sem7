"""
PROBLEM STATEMENT : Email spam classification with KNN and SVM (ML)

Classify e-mails as spam (spam = 1) or normal (spam = 0) from their raw
text, following the notebook "KNN&SVM.ipynb": TF-IDF vectorisation, then
K-Nearest Neighbours (k = 5) and a linear SVM, compared on accuracy /
precision / recall / F1 and a full classification report.

HOW IT WORKS:
1. DATA - emails.csv with two columns (text, spam) must be in the working
   directory. Cleaning drops duplicate rows and rows with a missing text
   or label (a repeated identical e-mail or a blank label would otherwise
   skew both training and evaluation).
2. SPLIT - 80/20 train/test, stratified on the label, random_state fixed
   -> anyone can reproduce the exact numbers.
3. FEATURES - TfidfVectorizer(stop_words="english", max_features=5000):
   - tokenizes each e-mail and drops generic English stop words
     (see the IR StopWordRemoval practical for why),
   - counts word occurrences (TF) but DOWNWEIGHTS words that occur across
     almost all mails (IDF) - "money" separates mails, "subject" doesn't,
   - normalises each document vector to unit length, so long mails don't
     tilt distances/kernels, and caps the vocabulary at 5000 terms.
   fit_transform on train (learns the vocabulary + IDF), transform on test
   (test mails are encoded with the TRAINING vocabulary only - never leak).
   Output: sparse matrices, one row per mail, one column per term.
4. CLASSIFIERS, then compare:
   - KNN(5): votes on the 5 nearest mails in TF-IDF space; simple, but a
     full distance computation per test mail is slow at scale.
   - Linear SVC: finds the hyper-plane that separates the two classes with
     maximal margin in that same space; sparse-friendly and fast, usually
     the stronger text classifier (exactly what comparison should show).
5. EVALUATE - accuracy, precision, recall, F1 per model, plus the sklearn
   classification_report (per-class precision/recall/F1/support).
   In spam filtering PRECISION is the sensitive metric: a normal mail
   wrongly flagged as spam (FP) means losing real mail, so a filter must
   stay precise even while catching most spam.

NEEDS:  pip install pandas scikit-learn
RUN:    python3 "ml/KNNandSVM.py"   (emails.csv in the same directory)
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


def load_and_clean():
    """Read e-mails.csv, drop duplicates/blank rows, and show class balance."""
    data = pd.read_csv("emails.csv")

    print("Dataset Shape:", data.shape)
    print(data.head())
    print("\nColumns:", list(data.columns))

    before = data.shape[0]
    data = data.drop_duplicates().dropna(subset=["text", "spam"]).copy()
    print("\nCleaned Dataset Shape:", data.shape, f"({before - data.shape[0]} rows removed)")

    print("\nClass Distribution:")
    print(data["spam"].value_counts(), "\n")

    X, y = data["text"], data["spam"]
    return X, y


def split_and_vectorize(X, y):
    """80/20 stratified split; TF-IDF fitted on train only."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print("Training samples:", len(X_train))
    print("Testing samples:", len(X_test))

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(X_train)  # learn vocab + IDF here
    X_test_tfidf = vectorizer.transform(X_test)        # reuse for test mails
    print("Training TF-IDF shape:", X_train_tfidf.shape)
    print("Testing TF-IDF shape:", X_test_tfidf.shape, "\n")
    return X_train_tfidf, X_test_tfidf, y_train, y_test


def evaluate_model(name, model, X_train_tfidf, X_test_tfidf, y_train, y_test):
    """Fit one classifier, predict, and print its metric block."""
    model.fit(X_train_tfidf, y_train)
    y_pred = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print(f"----- {name} PERFORMANCE -----")
    print("Accuracy :", round(float(accuracy), 4))
    print("Precision:", round(float(precision), 4))
    print("Recall   :", round(float(recall), 4))
    print("F1 Score :", round(float(f1), 4))
    print(f"\nClassification Report - {name}")
    print(classification_report(y_test, y_pred, zero_division=0))


def run():
    """Load -> vectorize -> evaluate both classifiers; main calls this."""
    X, y = load_and_clean()
    X_train_tfidf, X_test_tfidf, y_train, y_test = split_and_vectorize(X, y)

    # KNN in TF-IDF space: nearest 5 training mails vote on the label.
    evaluate_model("KNN", KNeighborsClassifier(n_neighbors=5),
                   X_train_tfidf, X_test_tfidf, y_train, y_test)

    # Linear SVM: maximal-margin separating hyper-plane in TF-IDF space.
    evaluate_model("SVM", SVC(kernel="linear"),
                   X_train_tfidf, X_test_tfidf, y_train, y_test)


if __name__ == "__main__":
    run()
