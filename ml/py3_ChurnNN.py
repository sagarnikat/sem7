"""
QUESTION 3 (ML):
Given a bank customer, build a neural-network-based classifier that can
determine whether they will leave (churn) or not in the next 6 months.

Dataset: https://www.kaggle.com/barelydedicated/bank-customer-churn-modeling

HOW IT WORKS
    Churn_Modelling.csv sits in the same folder as this file. If it is
    missing, Step 2 writes a small hardcoded demo file with the same columns.

    The model is a small feed-forward network:
        input -> Dense(64, relu) -> Dense(32, relu) -> Dense(1, sigmoid)
    The improved version adds an extra layer, dropout and early stopping.

STEPS
    1. Imports
    2. Create the dataset file if it is missing
    3. Load the dataset
    4. Separate features and target, then split
    5. Normalise the data
    6. Build the baseline model
    7. Train the baseline model
    8. Build the improved model
    9. Train the improved model
    10. Accuracy and confusion matrix for both models
    11. Observation
    12. Plots with matplotlib

RUN
    python3 ml/py3_ChurnNN.py

    In Jupyter, open py3_ChurnNN.ipynb or split this file at the "# %%"
    markers.
"""

# %% Step 1: Imports
import os

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.models import Sequential

if "__file__" in globals():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
else:
    SCRIPT_DIR = os.getcwd()

DATASET_FILE = os.path.join(SCRIPT_DIR, "Churn_Modelling.csv")

# %% Step 2: Create the dataset file if it is missing
# Skip this step when Churn_Modelling.csv is already in the folder.
DEMO_CHURN_CSV = """RowNumber,CustomerId,Surname,CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Exited
1,15634702,Hargrave,619,France,Male,42,2,0.00,1,1,1,101348.88,1
2,15634773,Hill,702,Spain,Female,45,8,122608.29,1,1,0,112542.58,0
3,15668891,Bergstrom,667,France,Male,39,1,0.00,2,1,0,113931.57,1
4,15647382,Booth,502,France,Female,32,9,0.00,2,0,0,146955.64,0
5,15631944,Chin,587,Spain,Male,35,5,115046.74,2,1,0,146955.64,0
6,15639287,Cherry,699,France,Female,30,7,102716.55,1,0,1,85020.83,0
7,15668824,Duke,545,Germany,Male,54,2,112635.79,1,1,0,148412.23,1
8,15634368,Onoro,641,France,Male,50,5,0.00,2,1,1,74266.32,0
9,15631840,Marshall,608,Spain,Female,28,8,112542.58,2,1,1,134611.93,0
10,15630786,McBride,677,Germany,Male,38,3,0.00,2,1,0,96709.07,0
11,15638075,Bearce,623,France,Male,26,3,0.00,2,1,1,51419.18,0
12,15654327,Giannopoulos,635,Spain,Female,49,7,0.00,1,1,0,101348.88,1
13,15622196,Nejad,549,Germany,Female,57,4,95243.11,1,0,0,112542.58,1
14,15628762,Chien,556,France,Male,33,4,0.00,2,1,1,123456.78,0
15,15632244,Bonelli,723,France,Female,44,2,130142.89,2,1,1,98765.43,1
16,15691973,Chu,501,Spain,Male,41,6,0.00,1,1,0,51419.18,0
"""

if os.path.exists(DATASET_FILE):
    print(f"Using dataset: {DATASET_FILE}")
else:
    with open(DATASET_FILE, "w", encoding="utf-8") as file:
        file.write(DEMO_CHURN_CSV)
    print(f"Created demo dataset: {DATASET_FILE}")

# %% Step 3: Load the dataset
data = pd.read_csv(DATASET_FILE)
data = data.drop(columns=["RowNumber", "CustomerId", "Surname"])

print("\nShape:", data.shape)
print(data.head())

# %% Step 4: Separate features and target, then split
data = pd.get_dummies(data, columns=["Geography", "Gender"], drop_first=True)

X = data.drop(columns=["Exited"])
y = data["Exited"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y)

print("\nFeature shape:", X.shape)
print("Training rows:", len(X_train))
print("Test rows    :", len(X_test))

# %% Step 5: Normalise the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# %% Step 6: Build the baseline model
initial_model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(64, activation="relu"),
    Dense(32, activation="relu"),
    Dense(1, activation="sigmoid"),
])
initial_model.compile(optimizer="adam", loss="binary_crossentropy",
                      metrics=["accuracy"])
initial_model.summary()

# %% Step 7: Train the baseline model
initial_history = initial_model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=1,
)

# %% Step 8: Build the improved model
model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(64, activation="relu"),
    Dropout(0.3),
    Dense(32, activation="relu"),
    Dropout(0.2),
    Dense(16, activation="relu"),
    Dense(1, activation="sigmoid"),
])
model.compile(optimizer="adam", loss="binary_crossentropy",
              metrics=["accuracy"])
model.summary()

# %% Step 9: Train the improved model
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True,
)

history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stop],
    verbose=1,
)

# %% Step 10: Accuracy and confusion matrix for both models
def evaluate(name, prediction):
    """Print accuracy and confusion matrix for one model."""
    print(f"\n----- {name} -----")
    print("Accuracy Score:", accuracy_score(y_test, prediction))
    print("Confusion Matrix (TN, FP / FN, TP):")
    print(confusion_matrix(y_test, prediction))


y_base = (initial_model.predict(X_test) > 0.5).astype(int).ravel()
evaluate("BASE MODEL", y_base)

y_pred = (model.predict(X_test) > 0.5).astype(int).ravel()
evaluate("IMPROVED MODEL (dropout + early stopping)", y_pred)

# %% Step 11: Observation
print("\nObservation")
print("  Compare the accuracy and confusion matrices. Dropout and early")
print("  stopping usually reduce overfitting, so the improved model should")
print("  generalise better than the baseline on the test set.")

# %% Step 12: Plots with matplotlib
import matplotlib.pyplot as plt

# Plots 1 and 2: training history metrics, each in its own figure.
for metric in ["accuracy", "loss"]:
    fig, axis = plt.subplots(figsize=(7, 5))
    axis.plot(initial_history.history[metric], label="baseline train")
    axis.plot(initial_history.history[f"val_{metric}"],
              "--", label="baseline validation")
    axis.plot(history.history[metric], label="improved train")
    axis.plot(history.history[f"val_{metric}"],
              "--", label="improved validation")
    axis.set_title(f"Model {metric}")
    axis.set_xlabel("Epoch")
    axis.set_ylabel(metric.capitalize())
    axis.grid(alpha=0.3)
    axis.legend(fontsize=8)
    fig.tight_layout()
    plt.show()

# Plots 3 and 4: one separate confusion matrix for each model.
for name, prediction in [("Baseline", y_base), ("Improved", y_pred)]:
    matrix = confusion_matrix(y_test, prediction)
    fig, axis = plt.subplots(figsize=(6, 5))
    image = axis.imshow(matrix, cmap="Blues")
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            axis.text(column, row, matrix[row, column], ha="center",
                      va="center",
                      color="white" if matrix[row, column] > matrix.max() / 2
                      else "black")
    axis.set_title(f"{name} model confusion matrix")
    axis.set_xlabel("Predicted (0 = stays, 1 = churns)")
    axis.set_ylabel("Actual (0 = stays, 1 = churns)")
    axis.set_xticks([0, 1])
    axis.set_yticks([0, 1])
    fig.colorbar(image, ax=axis, shrink=0.8)
    fig.tight_layout()
    plt.show()
