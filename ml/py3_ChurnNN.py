"""
QUESTION 3 (ML):
Given a bank customer, build a neural-network-based classifier that can
determine whether they will leave (churn) or not in the next 6 months.
Steps: read the dataset; distinguish features/target and split; normalize;
initialize and build the model, identify points of improvement and
implement them; print the accuracy score and confusion matrix.
Dataset: https://www.kaggle.com/barelydedicated/bank-customer-churn-modeling

NOTE ON STEP 2: if the real Churn_Modelling.csv is not present, a small
HARDCODED demo dataset (16 customers, same column structure) is written
so the pipeline runs end-to-end. Drop the real Kaggle CSV in this folder
for real-world numbers.

COMMANDS (run from the repository root):
    install dependencies : pip install pandas numpy scikit-learn tensorflow
    run the program      : python3 ml/py3_ChurnNN.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import os

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.models import Sequential


# ============================================================
# STEP 2 : CREATE THE DATASET FILE - if Churn_Modelling.csv is
#          missing, write a small HARDCODED demo dataset with the
#          same columns as the real one (16 customers)
# ============================================================
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

DATASET_FILE = "Churn_Modelling.csv"


def ensure_dataset():
    """Use the real CSV if present; otherwise create the demo CSV."""
    if os.path.exists(DATASET_FILE):
        print(f"Using existing {DATASET_FILE}")
    else:
        with open(DATASET_FILE, "w") as file:
            file.write(DEMO_CHURN_CSV)
        print(f"Created demo {DATASET_FILE} from hardcoded sample data")


# ============================================================
# STEP 3 : USE THE FILE - read it, distinguish features/target,
#          one-hot encode, split into train and test sets
# ============================================================
def load_dataset():
    """Read the CSV and drop the three pure identifier columns."""
    data = pd.read_csv(DATASET_FILE)

    print("Dataset Shape:", data.shape)
    print(data.head())

    data = data.drop(["RowNumber", "CustomerId", "Surname"], axis=1)
    return data


def split_dataset(data):
    """One-hot encode categoricals, split X/y, 80/20 stratified split."""
    data = pd.get_dummies(data, columns=["Geography", "Gender"],
                          drop_first=True)
    X, y = data.drop("Exited", axis=1), data["Exited"]

    print("Feature shape:", X.shape)
    print("Target shape:", y.shape)
    return train_test_split(X, y, test_size=0.20, random_state=42,
                            stratify=y)


# ============================================================
# STEP 4 : NORMALIZE THE DATA (fit the scaler on train only)
# ============================================================
def scale_data(X_train, X_test):
    """StandardScaler: fit on train, apply the same scaling to test."""
    scaler = StandardScaler()
    return scaler.fit_transform(X_train), scaler.transform(X_test)


# ============================================================
# STEP 5 : INITIALIZE AND BUILD THE MODELS (base + improvement)
# ============================================================
def build_base_model(input_dim):
    """Baseline: two relu layers + sigmoid output (no regularisation)."""
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(64, activation="relu"),
        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy",
                  metrics=["accuracy"])
    model.summary()
    return model


def build_improved_model(input_dim):
    """Improvement: dropout layers (0.3/0.2) - the point of improvement."""
    model = Sequential([
        Input(shape=(input_dim,)),
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
    return model


# ============================================================
# STEP 6 : TRAIN BOTH MODELS (improved one adds early stopping)
# ============================================================
def train_models(X_train, X_test, y_train):
    """Fit base, then dropout+early-stopping model; return both models."""
    input_dim = X_train.shape[1]

    initial_model = build_base_model(input_dim)
    initial_model.fit(X_train, y_train, epochs=50, batch_size=32,
                      validation_split=0.2, verbose=1)

    early_stop = EarlyStopping(monitor="val_loss", patience=5,
                               restore_best_weights=True)
    model = build_improved_model(input_dim)
    model.fit(X_train, y_train, epochs=50, batch_size=32,
              validation_split=0.2, callbacks=[early_stop], verbose=1)
    return initial_model, model


# ============================================================
# STEP 7 : EVALUATE - accuracy score + confusion matrix
# ============================================================
def evaluate(y_test, y_pred, label):
    """Print accuracy + confusion matrix for one model's predictions."""
    print(f"\n----- {label} -----")
    print("Accuracy Score:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix (TN, FP / FN, TP):")
    print(confusion_matrix(y_test, y_pred))


# ============================================================
# STEP 8 : DRIVER - chain steps 2-7 together
# ============================================================
def run():
    ensure_dataset()                                  # STEP 2
    data = load_dataset()                             # STEP 3
    X_train, X_test, y_train, y_test = split_dataset(data)
    X_train, X_test = scale_data(X_train, X_test)     # STEP 4

    initial_model, model = train_models(X_train, X_test, y_train)   # STEP 5-6

    y_base = (initial_model.predict(X_test) > 0.5).astype(int).ravel()
    evaluate(y_test, y_base, "BASE MODEL")            # STEP 7

    y_pred = (model.predict(X_test) > 0.5).astype(int).ravel()
    evaluate(y_test, y_pred, "IMPROVED MODEL (dropout + early stopping)")


if __name__ == "__main__":
    run()