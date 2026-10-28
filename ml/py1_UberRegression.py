"""
QUESTION 1 (ML):
Predict the price of the Uber ride from a given pickup point to the agreed
drop-off location. Perform:
    1. Pre-process the dataset.
    2. Identify outliers.
    3. Check the correlation.
    4. Implement linear regression and random forest regression models.
    5. Evaluate the models and compare their scores (R2, RMSE, etc.).
Dataset: https://www.kaggle.com/datasets/yasserh/uber-fares-dataset

NOTE ON STEP 2: if the real uber.csv is not present, a small HARDCODED
demo dataset (a few valid rides + a few impossible ones) is written to
uber.csv so the whole pipeline runs end-to-end. Drop the real Kaggle CSV
in this folder to get real-world numbers instead of demo numbers.

COMMANDS (run from the repository root):
    install dependencies : pip install pandas numpy matplotlib seaborn scikit-learn
    run the program      : python3 ml/py1_UberRegression.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import os

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

if not os.environ.get("DISPLAY"):
    matplotlib.use("Agg")      # headless: save PNGs instead of opening windows


# ============================================================
# STEP 2 : CREATE THE DATASET FILE - if uber.csv is missing,
#          write a small HARDCODED demo dataset (valid rides +
#          a few impossible rows so preprocessing has work to do)
# ============================================================
DEMO_UBER_CSV = """fare_amount,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count
8.5,-73.98,40.75,-73.95,40.78,1
12.0,-73.99,40.73,-73.92,40.76,2
6.5,-73.97,40.79,-73.96,40.77,1
25.0,-73.95,40.65,-73.85,40.75,3
40.0,-74.00,40.70,-73.70,40.85,4
4.5,-73.98,40.76,-73.99,40.75,1
15.5,-73.90,40.80,-73.80,40.84,2
30.0,-73.85,40.60,-73.70,40.75,2
9.0,-73.96,40.71,-73.93,40.73,5
22.0,-74.01,40.72,-73.90,40.79,3
7.0,-73.99,40.74,-73.97,40.75,1
18.0,-73.92,40.77,-73.82,40.82,2
5.5,-73.98,40.75,-74.00,40.76,6
28.0,-73.80,40.85,-73.60,40.95,4
3.5,-73.97,40.76,-73.98,40.76,1
45.0,-73.70,40.60,-73.40,40.90,2
11.0,-73.95,40.72,-73.90,40.75,3
60.0,-73.00,40.00,-72.00,41.00,1
100.0,-73.90,40.70,-73.90,40.70,2
-5.0,-73.98,40.75,-73.95,40.78,1
"""

DATASET_FILE = "uber.csv"


def ensure_dataset():
    """Use the real CSV if present; otherwise create the demo CSV."""
    if os.path.exists(DATASET_FILE):
        print(f"Using existing {DATASET_FILE}")
    else:
        with open(DATASET_FILE, "w") as file:
            file.write(DEMO_UBER_CSV)
        print(f"Created demo {DATASET_FILE} from hardcoded sample data")


# ============================================================
# STEP 3 : USE THE FILE - load it, then pre-process the dataset
# ============================================================
def load_dataset():
    """Read uber.csv and fix the known PDF-copy column-name corruption."""
    df = pd.read_csv(DATASET_FILE)
    df.rename(columns={
        "dropo\u01ff_longitude": "dropoff_longitude",
        "dropo\u01ff_latitude": "dropoff_latitude",
    }, inplace=True)
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nDataset Shape:", df.shape)
    return df


def preprocess(df):
    """Clean, enforce numerics, remove impossible rides."""
    if "Unnamed: 0" in df.columns:
        df = df.drop("Unnamed: 0", axis=1)
    df = df.drop_duplicates().dropna()

    for col in ["fare_amount", "pickup_longitude", "pickup_latitude",
                "dropoff_longitude", "dropoff_latitude", "passenger_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")   # bad text -> NaN
    df = df.dropna()

    df = df[df["fare_amount"] > 0]
    df = df[(df["passenger_count"] >= 1) & (df["passenger_count"] <= 6)]
    df = df[
        df["pickup_latitude"].between(-90, 90)
        & df["dropoff_latitude"].between(-90, 90)
        & df["pickup_longitude"].between(-180, 180)
        & df["dropoff_longitude"].between(-180, 180)
    ].copy()
    print("Shape after preprocessing:", df.shape)
    return df


# ============================================================
# STEP 4 : FEATURE ENGINEERING (Haversine distance) + OUTLIERS
# ============================================================
def haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance (km) between two (lat, lon) points, vectorised."""
    R = 6371
    lat1, lat2 = np.radians(lat1), np.radians(lat2)
    dlat = lat2 - lat1
    dlon = np.radians(lon2) - np.radians(lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return R * 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def add_distance_and_trim_outliers(df):
    """Add distance_km, drop zero distances, IQR-trim the two key columns."""

    def remove_outliers_iqr(frame, column):
        Q1, Q3 = frame[column].quantile(0.25), frame[column].quantile(0.75)
        IQR = Q3 - Q1
        low, high = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        return frame[(frame[column] >= low) & (frame[column] <= high)]

    df["distance_km"] = haversine(
        df["pickup_latitude"], df["pickup_longitude"],
        df["dropoff_latitude"], df["dropoff_longitude"])
    df = df[df["distance_km"] > 0]

    print("Shape before removing outliers:", df.shape)
    df = remove_outliers_iqr(df, "fare_amount")
    df = remove_outliers_iqr(df, "distance_km")
    print("Shape after removing outliers:", df.shape)
    return df


# ============================================================
# STEP 5 : CHECK THE CORRELATION (matrix + heatmap)
# ============================================================
def show_correlation(df):
    """Which columns actually relate to fare_amount."""
    columns = ["fare_amount", "passenger_count", "pickup_longitude",
               "pickup_latitude", "dropoff_longitude", "dropoff_latitude",
               "distance_km"]
    correlation = df[columns].corr()
    print("\nCorrelation Matrix:")
    print(correlation)

    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.savefig("correlation_heatmap.png", dpi=120, bbox_inches="tight")
    plt.show()


# ============================================================
# STEP 6 : TRAIN BOTH REGRESSION MODELS
# ============================================================
def train_models(df):
    """LinearRegression vs RandomForestRegressor on an 80/20 split."""
    X = df[["passenger_count", "pickup_longitude", "pickup_latitude",
            "dropoff_longitude", "dropoff_latitude", "distance_km"]]
    y = df["fare_amount"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42)

    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    linear_prediction = linear_model.predict(X_test)

    random_forest = RandomForestRegressor(n_estimators=100, random_state=42,
                                          n_jobs=-1)
    random_forest.fit(X_train, y_train)
    rf_prediction = random_forest.predict(X_test)
    return y_test, linear_prediction, rf_prediction


# ============================================================
# STEP 7 : EVALUATE + COMPARE + PLOT
# ============================================================
def evaluate_model(name, actual, predicted):
    """R2 / MAE / RMSE for one model."""
    r2 = r2_score(actual, predicted)
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    print(f"\n{name}\n---------------------------")
    print("R2 Score :", round(float(r2), 4))
    print("MAE      :", round(float(mae), 4))
    print("RMSE     :", round(float(rmse), 4))
    return {"Model": name, "R2 Score": r2, "MAE": mae, "RMSE": rmse}


def run():
    """Steps 2-7 chained together; main() only calls this."""
    ensure_dataset()                                   # STEP 2
    df = preprocess(load_dataset())                    # STEP 3
    df = add_distance_and_trim_outliers(df)            # STEP 4
    show_correlation(df)                               # STEP 5
    y_test, linear_prediction, rf_prediction = train_models(df)   # STEP 6

    results = pd.DataFrame([                           # STEP 7
        evaluate_model("Linear Regression", y_test, linear_prediction),
        evaluate_model("Random Forest Regression", y_test, rf_prediction),
    ])
    print("\nModel Comparison:")
    print(results.to_string(index=False))

    plt.figure(figsize=(8, 5))
    plt.scatter(y_test, rf_prediction, alpha=0.5)
    plt.xlabel("Actual Fare")
    plt.ylabel("Predicted Fare")
    plt.title("Actual vs Predicted Fare - Random Forest")
    plt.savefig("actual_vs_predicted.png", dpi=120, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    run()