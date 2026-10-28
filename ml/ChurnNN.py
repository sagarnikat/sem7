"""
PROBLEM STATEMENT : Customer Churn prediction with a Neural Network (Keras)

Predict whether a bank customer will EXIT (Exited = 1) or stay (Exited = 0)
from the Churn_Modelling.csv dataset, using a feed-forward neural network.
The notebook trains a BASE model, then an IMPROVED model with dropout
layers and early stopping, showing the two classic anti-overfitting tools.

HOW IT WORKS:
1. DATA - Churn_Modelling.csv in the working directory (Kaggle "Churn
   Modelling"). Drop the pure identifier columns RowNumber / CustomerId /
   Surname: they carry NO pattern, letting the model memorise row identity
   would be pure overfitting fuel.
2. ENCODE - one-hot encode the two categorical strings with get_dummies
   (drop_first=True avoids a redundant duplicate column): Geography and
   Gender become 0/1 indicator columns a network can consume. Everything
   else is already numeric.
3. SPLIT + SCALE - 80/20 stratified split, then StandardScaler. Neural
   networks train by gradient descent: when a feature like Balance
   (~0-250k) drowns a 0/1 indicator, the shared learning rate is wrong for
   every layer gradient - scaling makes convergence fast and stable.
   Train-only scaling (fit) as always.
4. BASE NETWORK - Sequential stack:
        64 relu -> 32 relu -> 1 sigmoid
   relu solves the vanishing-gradient problem of sigmoid hidden layers;
   the single sigmoid output gives P(churn) for binary cross-entropy loss;
   Adam = adaptive learning-rate SGD (the standard default optimiser).
5. IMPROVED NETWORK - dropout (0.3 / 0.2) + early stopping:
   - Dropout randomly zeroes a fraction of the activations per training
     batch, so no single path/neuron can carry memorised patterns - the
     network must learn redundant robust features. At inference dropout
     is off automatically.
   - EarlyStopping monitors validation loss (20% of train is held out by
     validation_split) and RESTORES THE BEST WEIGHTS when it stops
     improving, preventing the model from overfitting in later epochs.
6. EVALUATE - threshold P > 0.5 -> class 1, then accuracy_score and the
   confusion matrix. Note the class-imbalance lesson: churn is ~20% of
   rows, so a "predict nobody churns" dummy scores 80% accuracy with zero
   business value - read the confusion matrix (recall on churned
   customers), not just the accuracy number.

NEEDS:  pip install pandas numpy scikit-learn tensorflow
RUN:    python3 "ml/ChurnNN.py"   (Churn_Modelling.csv in the same directory)
"""

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.models import Sequential


def load_dataset():
    """Read Churn_Modelling.csv and drop the three identifier columns."""
    data = pd.read_csv("Churn_Modelling.csv")

    print("Dataset Shape:", data.shape)
    print(data.head(), "\n")

    data = data.drop(["RowNumber", "CustomerId", "Surname"], axis=1)
    return data


def make_features(data):
    """One-hot encode categoricals and split into X (features) / y (target)."""
    data = pd.get_dummies(data, columns=["Geography", "Gender"], drop_first=True)

    X = data.drop("Exited", axis=1)
    y = data["Exited"]

    print("Feature shape:", X.shape)
    print("Target shape:", y.shape, "\n")
    return X, y


def split_and_scale(X, y):
    """80/20 stratified split, StandardScaler fitted on train only."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)  # apply train scaling, never refit
    return X_train, X_test, y_train, y_test


def build_base_model(input_dim):
    """The plain baseline: two Dense(relu) hidden layers + sigmoid output."""
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(64, activation="relu"),
        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid"),  # P(churn) in [0, 1]
    ])
    model.compile(optimizer="adam",
                  loss="binary_crossentropy",
                  metrics=["accuracy"])
    model.summary()
    return model


def build_improved_model(input_dim):
    """Baseline + dropout regularisation between/inside hidden layers."""
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(64, activation="relu"),
        Dropout(0.3),                    # 30% of activations zeroed per batch
        Dense(32, activation="relu"),
        Dropout(0.2),
        Dense(16, activation="relu"),
        Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer="adam",
                  loss="binary_crossentropy",
                  metrics=["accuracy"])
    model.summary()
    return model


def evaluate(y_test, y_pred, label):
    """Accuracy + confusion matrix for one model's hard predictions."""
    print(f"\n----- {label} -----")
    print("Accuracy Score:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix (TN, FP / FN, TP):")
    print(confusion_matrix(y_test, y_pred))


def run():
    """Compare base vs improved network; main() only calls this."""
    data = load_dataset()
    X, y = make_features(data)
    X_train, X_test, y_train, y_test = split_and_scale(X, y)

    # Step 1: the unregularised baseline (watch its validation-loss climb).
    input_dim = X_train.shape[1]
    initial_model = build_base_model(input_dim)
    initial_model.fit(X_train, y_train, epochs=50,
                      batch_size=32, validation_split=0.2, verbose=1)
    y_base = (initial_model.predict(X_test) > 0.5).astype(int).ravel()
    evaluate(y_test, y_base, "BASE MODEL")

    # Step 2: dropout + early stopping on validation loss.
    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=5,           # epochs of no improvement before stopping
        restore_best_weights=True,
    )
    model = build_improved_model(input_dim)
    model.fit(X_train, y_train, epochs=50, batch_size=32,
              validation_split=0.2, callbacks=[early_stop], verbose=1)

    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int).ravel()  # threshold at 0.5
    evaluate(y_test, y_pred, "IMPROVED MODEL (dropout + early stopping)")


if __name__ == "__main__":
    run()
