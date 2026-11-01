"""
QUESTION 4 (ML):
Implement the K-Nearest Neighbors algorithm on the diabetes.csv dataset.
Compute the confusion matrix, accuracy, error rate, precision and recall.

Dataset: https://www.kaggle.com/datasets/abdallamahgoub/diabetes

HOW IT WORKS
    diabetes.csv sits in the same folder as this file. If it is missing,
    Step 2 writes a small hardcoded demo file with the same columns.

    KNN classifies a patient by looking at the 5 nearest training patients.
    Zero values in Glucose, BloodPressure, SkinThickness, Insulin and BMI are
    missing measurements, so they are replaced by the training median.
    Features are standardised because KNN uses distances.

STEPS
    1. Imports
    2. Create the dataset file if it is missing
    3. Load the dataset
    4. Split, impute and scale
    5. Train KNN and predict
    6. Confusion matrix and metrics
    7. Observation
    8. Plots with matplotlib

RUN
    python3 ml/py4_DiabetesKNN.py

    In Jupyter, open py4_DiabetesKNN.ipynb or split this file at the
    "# %%" markers.
"""

# %% Step 1: Imports
import os

import pandas as pd
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

if "__file__" in globals():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
else:
    SCRIPT_DIR = os.getcwd()

DATASET_FILE = os.path.join(SCRIPT_DIR, "diabetes.csv")

# %% Step 2: Create the dataset file if it is missing
# Skip this step when diabetes.csv is already in the folder.
DEMO_DIABETES_CSV = """Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,Pedigree,Age,Outcome
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

if os.path.exists(DATASET_FILE):
    print(f"Using dataset: {DATASET_FILE}")
else:
    with open(DATASET_FILE, "w", encoding="utf-8") as file:
        file.write(DEMO_DIABETES_CSV)
    print(f"Created demo dataset: {DATASET_FILE}")

# %% Step 3: Load the dataset
data = pd.read_csv(DATASET_FILE)

print("\nShape:", data.shape)
print(data.head())

X = data.drop(columns=["Outcome"])
y = data["Outcome"]

# %% Step 4: Split, impute and scale
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y)

X_train = X_train.copy()
X_test = X_test.copy()
for column in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]:
    median = X_train.loc[X_train[column] > 0, column].median()
    X_train[column] = X_train[column].replace(0, median)
    X_test[column] = X_test[column].replace(0, median)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("\nTraining rows:", len(X_train))
print("Test rows    :", len(X_test))

# %% Step 5: Train KNN and predict
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

# %% Step 6: Confusion matrix and metrics
cm = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
error_rate = 1 - accuracy
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)

print("\nConfusion Matrix:")
print(cm)

print("\nAccuracy:", round(accuracy, 4))
print("Accuracy Percentage:", round(accuracy * 100, 2), "%")
print("Error Rate:", round(error_rate, 4))
print("Error Rate Percentage:", round(error_rate * 100, 2), "%")
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))

# %% Step 7: Observation
print("\nObservation")
print("  Accuracy is the fraction of correct predictions, and error rate is")
print("  1 - accuracy. Precision shows how many predicted diabetics really")
print("  are diabetic; recall shows how many real diabetics were found.")

# %% Step 8: Plots with matplotlib
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

image = axes[0].imshow(cm, cmap="Blues")
for row in range(cm.shape[0]):
    for column in range(cm.shape[1]):
        axes[0].text(column, row, cm[row, column], ha="center", va="center",
                     color="white" if cm[row, column] > cm.max() / 2
                     else "black")
axes[0].set_title("Confusion matrix")
axes[0].set_xlabel("Predicted (0 = healthy, 1 = diabetic)")
axes[0].set_ylabel("Actual (0 = healthy, 1 = diabetic)")
axes[0].set_xticks([0, 1])
axes[0].set_yticks([0, 1])
fig.colorbar(image, ax=axes[0], shrink=0.8)

names = ["Accuracy", "Error rate", "Precision", "Recall"]
values = [accuracy, error_rate, precision, recall]
bars = axes[1].bar(names, values, color=["tab:green", "tab:red",
                                        "tab:blue", "tab:orange"])
axes[1].bar_label(bars, fmt="%.3f", fontsize=8)
axes[1].set_ylim(0, 1.1)
axes[1].set_title("KNN evaluation metrics")
axes[1].set_ylabel("Score")
axes[1].grid(axis="y", alpha=0.3)

neighbours = list(range(1, 11))
scores = []
for k in neighbours:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    scores.append(accuracy_score(y_test, model.predict(X_test)))

axes[2].plot(neighbours, scores, "o-", color="tab:purple")
best_k = neighbours[scores.index(max(scores))]
axes[2].axvline(best_k, color="tab:red", linestyle="--",
                label=f"best k = {best_k}")
axes[2].set_title("Accuracy vs number of neighbours")
axes[2].set_xlabel("k")
axes[2].set_ylabel("Test accuracy")
axes[2].grid(alpha=0.3)
axes[2].legend(fontsize=8)
fig.suptitle("Diabetes prediction with K-Nearest Neighbors")
fig.tight_layout()
plt.show()
