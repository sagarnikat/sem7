"""
QUESTION 5 (ML):
Implement the K-Nearest Neighbors algorithm on the diabetes.csv dataset.
Compute the confusion matrix, accuracy, error rate, precision and recall
on the given dataset.
Dataset: https://www.kaggle.com/datasets/abdallamahgoub/diabetes

NOTE ON STEP 2: if the real diabetes.csv is not present, a small
HARDCODED demo dataset (16 patients, standard Pima columns) is written
so the pipeline runs end-to-end. Drop the real Kaggle CSV in this folder
for real-world numbers.

COMMANDS (run from the repository root):
    install dependencies : pip install pandas scikit-learn
    run the program      : python3 ml/py5_DiabetesKNN.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import os

import pandas as pd
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


# ============================================================
# STEP 2 : CREATE THE DATASET FILE - if diabetes.csv is missing,
#          write a small HARDCODED demo dataset (16 patients with
#          the standard Pima columns and mixed outcomes)
# ============================================================
DEMO_DIABETES_CSV = """Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome
6,148,72,35,0,33.6,0.627,50,1
1,85,66,29,0,26.6,0.351,31,0
8,183,64,0,0,23.3,0.672,32,1
1,89,66,23,94,28.1,0.167,21,0
0,137,40,35,168,43.1,2.288,33,1
5,116,74,0,0,25.6,0.201,30,0
3,78,50,32,88,31.0,0.248,26,1
10,115,0,0,0,35.3,0.134,29,0
2,197,70,45,543,30.5,0.158,53,1
8,125,96,0,0,0.0,0.232,54,1
4,110,92,0,0,37.6,0.191,30,0
2,100,66,38,150,32.0,0.15,22,0
7,105,0,0,0,0.0,0.305,24,0
0,180,66,39,0,42.0,1.4,42,1
1,95,60,18,90,24.5,0.21,25,0
6,95,70,32,95,30.7,0.29,28,0
"""

DATASET_FILE = "diabetes.csv"


def ensure_dataset():
    """Use the real CSV if present; otherwise create the demo CSV."""
    if os.path.exists(DATASET_FILE):
        print(f"Using existing {DATASET_FILE}")
    else:
        with open(DATASET_FILE, "w") as file:
            file.write(DEMO_DIABETES_CSV)
        print(f"Created demo {DATASET_FILE} from hardcoded sample data")


# ============================================================
# STEP 3 : USE THE FILE - read it, split into features/target
# ============================================================
def load_dataset():
    """Read diabetes.csv; split into features X and target y (Outcome)."""
    data = pd.read_csv(DATASET_FILE)

    print("Dataset:")
    print(data.head())
    return data.drop("Outcome", axis=1), data["Outcome"]


# ============================================================
# STEP 4 : SPLIT + NORMALIZE (fit the scaler on train only)
# ============================================================
def split_and_scale(X, y):
    """80/20 stratified split + StandardScaler (fit train only)."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test


# ============================================================
# STEP 5 : TRAIN KNN AND PREDICT (k = 5 nearest neighbours vote)
# ============================================================
def train_and_predict(X_train, X_test, y_train):
    """Fit KNN(5) and predict the test rows."""
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    return knn.predict(X_test)


# ============================================================
# STEP 6 : EVALUATE - confusion matrix + the five metrics
# ============================================================
def evaluate(y_test, y_pred):
    """Confusion matrix + accuracy/error/precision/recall block."""
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    error_rate = 1 - accuracy
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)

    print("\nConfusion Matrix:")
    print(cm)

    print("\nAccuracy:", round(float(accuracy), 4))
    print("Accuracy Percentage:", round(float(accuracy) * 100, 2), "%")
    print("Error Rate:", round(float(error_rate), 4))
    print("Error Rate Percentage:", round(float(error_rate) * 100, 2), "%")
    print("Precision:", round(float(precision), 4))
    print("Recall:", round(float(recall), 4))


# ============================================================
# STEP 7 : DRIVER - create file -> load -> split/scale -> KNN
# ============================================================
def run():
    ensure_dataset()                                  # STEP 2
    X, y = load_dataset()                             # STEP 3
    X_train, X_test, y_train, y_test = split_and_scale(X, y)   # STEP 4
    y_pred = train_and_predict(X_train, X_test, y_train)       # STEP 5
    evaluate(y_test, y_pred)                          # STEP 6


if __name__ == "__main__":
    run()