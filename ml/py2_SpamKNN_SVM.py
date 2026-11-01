"""
QUESTION 2 (ML):
Classify the email using the binary classification method (Normal = not
spam / Abnormal = spam). Use K-Nearest Neighbors and Support Vector Machine
for classification and analyze their performance.

Dataset: https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv

HOW IT WORKS
    emails.csv sits in the same folder as this file. It is already a
    word-count matrix:
        Email No. : the email id
        3000 word columns : how many times that word occurs
        Prediction : 1 = spam, 0 = not spam
    If emails.csv is missing, Step 2 writes a small hardcoded demo file with
    the same columns.

STEPS
    1. Imports
    2. Create the dataset file if it is missing
    3. Load the dataset
    4. Split into training and test sets
    5. K-Nearest Neighbors
    6. Support Vector Machine
    7. Compare the two classifiers
    8. Observation
    9. Plots with matplotlib

RUN
    python3 ml/py2_SpamKNN_SVM.py

    In Jupyter, open py2_SpamKNN_SVM.ipynb or split this file at the
    "# %%" markers.
"""

# %% Step 1: Imports
import os

import pandas as pd
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

if "__file__" in globals():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
else:
    SCRIPT_DIR = os.getcwd()

DATASET_FILE = os.path.join(SCRIPT_DIR, "emails.csv")

# %% Step 2: Create the dataset file if it is missing
# Skip this step when emails.csv is already in the folder.
DEMO_EMAILS_CSV = """Email No.,free,winner,offer,cash,prize,claim,urgent,click,meeting,report,schedule,attached,order,account,Prediction
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

if os.path.exists(DATASET_FILE):
    print(f"Using dataset: {DATASET_FILE}")
else:
    with open(DATASET_FILE, "w", encoding="utf-8") as file:
        file.write(DEMO_EMAILS_CSV)
    print(f"Created demo dataset: {DATASET_FILE}")

# %% Step 3: Load the dataset
data = pd.read_csv(DATASET_FILE)

print("\nShape:", data.shape)
print(data.head())
print("\nClass Distribution (1 = spam):")
print(data["Prediction"].value_counts())

X = data.drop(columns=["Email No.", "Prediction"])
y = data["Prediction"]

# %% Step 4: Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y)

print("\nTraining samples:", len(X_train))
print("Testing samples :", len(X_test))
print("Features        :", X_train.shape[1])

# %% Step 5: K-Nearest Neighbors
def evaluate(name, model):
    """Fit one classifier, print its metrics, and return its predictions."""
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)

    print(f"\n----- {name} -----")
    print("Accuracy :", round(accuracy_score(y_test, prediction), 4))
    print("Precision:", round(precision_score(y_test, prediction,
                                             zero_division=0), 4))
    print("Recall   :", round(recall_score(y_test, prediction,
                                           zero_division=0), 4))
    print("F1 Score :", round(f1_score(y_test, prediction,
                                       zero_division=0), 4))
    return prediction


knn_prediction = evaluate("KNN", KNeighborsClassifier(n_neighbors=5))

# %% Step 6: Support Vector Machine
svm_prediction = evaluate("SVM", SVC(kernel="linear"))

# %% Step 7: Compare the two classifiers
comparison = pd.DataFrame({
    "Model": ["KNN", "SVM"],
    "Accuracy": [accuracy_score(y_test, knn_prediction),
                 accuracy_score(y_test, svm_prediction)],
    "Precision": [precision_score(y_test, knn_prediction, zero_division=0),
                  precision_score(y_test, svm_prediction, zero_division=0)],
    "Recall": [recall_score(y_test, knn_prediction, zero_division=0),
               recall_score(y_test, svm_prediction, zero_division=0)],
    "F1": [f1_score(y_test, knn_prediction, zero_division=0),
           f1_score(y_test, svm_prediction, zero_division=0)],
})

print("\nModel Comparison:")
print(comparison.round(4).to_string(index=False))

# %% Step 8: Observation
print("\nObservation")
print("  Both models work on the same word-count features. Compare accuracy,")
print("  precision, recall and F1 above. SVM usually handles the very wide")
print("  feature matrix better, while KNN is simpler but slower to predict.")

# %% Step 9: Plots with matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for axis, name, prediction in [(axes[0], "KNN", knn_prediction),
                               (axes[1], "SVM", svm_prediction)]:
    matrix = confusion_matrix(y_test, prediction)
    image = axis.imshow(matrix, cmap="Blues")
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            axis.text(column, row, matrix[row, column], ha="center",
                      va="center",
                      color="white" if matrix[row, column] > matrix.max() / 2
                      else "black")
    axis.set_title(f"{name} confusion matrix")
    axis.set_xlabel("Predicted (0 = normal, 1 = spam)")
    axis.set_ylabel("Actual (0 = normal, 1 = spam)")
    axis.set_xticks([0, 1])
    axis.set_yticks([0, 1])
    fig.colorbar(image, ax=axis, shrink=0.8)
fig.tight_layout()
plt.show()

metrics = ["Accuracy", "Precision", "Recall", "F1"]
width = 0.35

fig, axis = plt.subplots(figsize=(9, 4.5))
for offset, row in zip([-width / 2, width / 2], range(2)):
    values = [comparison.loc[row, metric] for metric in metrics]
    bars = axis.bar([p + offset for p in range(len(metrics))], values, width,
                    label=comparison.loc[row, "Model"])
    axis.bar_label(bars, fmt="%.3f", fontsize=8)

axis.set_xticks(range(len(metrics)))
axis.set_xticklabels(metrics)
axis.set_ylim(0, 1.1)
axis.set_ylabel("Score")
axis.set_title("KNN vs SVM on the spam dataset")
axis.grid(axis="y", alpha=0.3)
axis.legend()
fig.tight_layout()
plt.show()
