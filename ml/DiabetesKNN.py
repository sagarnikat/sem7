"""
PROBLEM STATEMENT : Diabetes prediction with K-Nearest Neighbours (ML)

Predict whether a patient has diabetes (Outcome = 1) or not (Outcome = 0)
from standard medical measurements (glucose, BMI, age, ...), using the
pima-style diabetes.csv dataset. The algorithm used is K-Nearest Neighbours
with k = 5, and the exercise evaluates the classifier properly:
confusion matrix, accuracy, error rate, precision, recall.

HOW IT WORKS:
1. LOAD - diabetes.csv must be in the working directory (search Kaggle
   "Pima Indians Diabetes Database"); it needs the Outcome column.
2. SPLIT - rows are divided 80/20 into train and test. stratify=y keeps the
   same positive/negative ratio in both halves (vital for medical data),
   random_state=42 makes the split reproducible for grading.
3. SCALE - StandardScaler standardises every feature to mean 0 std 1.
   MANDATORY for KNN: distance-based algorithms are dominated by
   large-range columns otherwise (glucose ~ 0-200 would drown BMI ~ 15-70).
   fit on train only, transform both (test scaling must not leak train info).
4. CLASSIFY (what KNN does at prediction time):
   - compute the distance from the test point to EVERY training point
     (Euclidean on the scaled features),
   - keep the k = 5 nearest training rows,
   - output the majority label among those 5 ("tell me who your neighbours
     are and I'll tell you who you are").
5. EVALUATE on the untouched test half:
   - Confusion matrix [[TN, FP], [FN, TP]],
   - Accuracy = (TN+TP)/total, Error rate = 1 - accuracy,
   - Precision = TP/(TP+FP): of predicted diabetic, how many really are,
   - Recall    = TP/(TP+FN): of really diabetic, how many we caught.
   For a medical test, RECALL matters most: a missed diabetic (FN) is the
   dangerous error, and also why precision-only reading is misleading.

RESULT: printed confusion matrix plus the five metrics above (accuracy,
error rate, precision, recall, percentages), same output as the notebook.

NEEDS:  pip install pandas numpy scikit-learn
RUN:    python3 "ml/DiabetesKNN.py"   (diabetes.csv in the same directory)
"""

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


def load_dataset():
    """Read the CSV and split into feature matrix X and target vector y."""
    data = pd.read_csv("diabetes.csv")

    print("Dataset:")
    print(data.head(), "\n")

    X = data.drop("Outcome", axis=1)  # every measurement column
    y = data["Outcome"]               # the label to predict
    return X, y


def split_and_scale(X, y):
    """80/20 stratified split, then scale (fit train, transform both)."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,     # 20% held out for honest evaluation
        random_state=42,    # reproducible split
        stratify=y,         # keep class ratio in both halves
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)  # learn mean/std FROM TRAIN
    X_test = scaler.transform(X_test)        # apply the SAME scaling to test
    return X_train, X_test, y_train, y_test


def train_knn(X_train, y_train, neighbours=5):
    """Fit the KNN model; k=5 = the vote size used by the lab notebook."""
    knn = KNeighborsClassifier(n_neighbors=neighbours)
    knn.fit(X_train, y_train)
    return knn


def evaluate(y_test, y_pred):
    """Confusion matrix + the standard binary classification metrics."""
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


def run():
    """Load -> split/scale -> train -> predict -> evaluate; main calls this."""
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = split_and_scale(X, y)

    knn = train_knn(X_train, y_train)
    y_pred = knn.predict(X_test)  # majority vote of the 5 nearest rows

    evaluate(y_test, y_pred)


if __name__ == "__main__":
    run()
