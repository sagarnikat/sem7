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

NOTE ON STEP 2: the REAL uber.csv has 9 columns -
    Unnamed: 0, key, fare_amount, pickup_datetime, pickup_longitude,
    pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count
The hardcoded demo CSV mirrors that schema EXACTLY, and the code uses
only column names from the real file, so dropping the real Kaggle CSV
in this folder works with no code change - just better numbers.

NOTE ON LIBRARIES: only numpy, pandas and scikit-learn are used. The
correlation heatmap and the actual-vs-predicted plot are rendered as
ASCII art in the terminal, so no plotting library is required.

COMMANDS (run from the repository root):
    install dependencies : pip install numpy pandas scikit-learn
    run the program      : python3 ml/py1_UberRegression.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
import os

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# ============================================================
# STEP 2 : CREATE THE DATASET FILE - if uber.csv is missing,
#          write a small HARDCODED demo dataset with the SAME
#          9 COLUMNS as the real Kaggle file (a few impossible
#          rows are included so preprocessing has work to do)
# ============================================================
DEMO_UBER_CSV = """Unnamed: 0,key,fare_amount,pickup_datetime,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count
0,2015-01-27 19:47:14.0000001,8.5,2015-01-27 19:47:14,-73.98,40.75,-73.95,40.78,1
1,2015-02-14 08:15:00.0000002,12.0,2015-02-14 08:15:00,-73.99,40.73,-73.92,40.76,2
2,2015-03-08 22:30:45.0000003,6.5,2015-03-08 22:30:45,-73.97,40.79,-73.96,40.77,1
3,2015-04-21 07:05:12.0000004,25.0,2015-04-21 07:05:12,-73.95,40.65,-73.85,40.75,3
4,2015-05-30 13:40:59.0000005,40.0,2015-05-30 13:40:59,-74.00,40.70,-73.70,40.85,4
5,2015-06-12 18:20:33.0000006,4.5,2015-06-12 18:20:33,-73.98,40.76,-73.99,40.75,1
6,2015-01-05 11:11:11.0000007,15.5,2015-01-05 11:11:11,-73.90,40.80,-73.80,40.84,2
7,2015-02-19 05:55:05.0000008,30.0,2015-02-19 05:55:05,-73.85,40.60,-73.70,40.75,2
8,2015-03-27 16:00:00.0000009,9.0,2015-03-27 16:00:00,-73.96,40.71,-73.93,40.73,5
9,2015-04-02 09:45:20.0000010,22.0,2015-04-02 09:45:20,-74.01,40.72,-73.90,40.79,3
10,2015-05-16 20:10:10.0000011,7.0,2015-05-16 20:10:10,-73.99,40.74,-73.97,40.75,1
11,2015-06-28 14:35:42.0000012,18.0,2015-06-28 14:35:42,-73.92,40.77,-73.82,40.82,2
12,2015-01-17 03:25:55.0000013,5.5,2015-01-17 03:25:55,-73.98,40.75,-74.00,40.76,6
13,2015-02-08 12:12:12.0000014,28.0,2015-02-08 12:12:12,-73.80,40.85,-73.60,40.95,4
14,2015-03-15 21:05:37.0000015,3.5,2015-03-15 21:05:37,-73.97,40.76,-73.98,40.76,1
15,2015-04-29 10:50:23.0000016,45.0,2015-04-29 10:50:23,-73.70,40.60,-73.40,40.90,2
16,2015-05-23 17:18:46.0000017,11.0,2015-05-23 17:18:46,-73.95,40.72,-73.90,40.75,3
17,2015-06-03 06:30:30.0000018,60.0,2015-06-03 06:30:30,-73.00,40.00,-72.00,41.00,1
18,2015-06-20 23:59:59.0000019,100.0,2015-06-20 23:59:59,-73.90,40.70,-73.90,40.70,2
19,2015-06-25 02:02:02.0000020,-5.0,2015-06-25 02:02:02,-73.98,40.75,-73.95,40.78,0
"""

DATASET_FILE = "uber.csv"

# Columns of the REAL Kaggle uber.csv - the demo file matches these.
REAL_COLUMNS = ["Unnamed: 0", "key", "fare_amount", "pickup_datetime",
                "pickup_longitude", "pickup_latitude", "dropoff_longitude",
                "dropoff_latitude", "passenger_count"]


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
    missing = set(REAL_COLUMNS) - set(df.columns)
    if missing:
        print("WARNING: columns missing vs the real uber.csv:", missing)
    return df


def preprocess(df):
    """Clean, extract time features, enforce numerics, remove bad rides."""
    df = df.drop(columns=["Unnamed: 0", "key"], errors="ignore")

    # Time features from pickup_datetime (works for real + demo data).
    pickup = pd.to_datetime(df["pickup_datetime"], errors="coerce")
    df["year"] = pickup.dt.year
    df["month"] = pickup.dt.month
    df["day_of_week"] = pickup.dt.dayofweek
    df["hour"] = pickup.dt.hour

    df = df.drop_duplicates().dropna()   # drop rows with unparseable data

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
# STEP 5 : CHECK THE CORRELATION (matrix + terminal ASCII heatmap)
# ============================================================
def show_correlation(df):
    """Which columns actually relate to fare_amount."""
    columns = ["fare_amount", "passenger_count", "hour", "day_of_week",
               "month", "distance_km", "pickup_longitude", "pickup_latitude",
               "dropoff_longitude", "dropoff_latitude"]
    correlation = df[columns].corr()

    print("\nCorrelation Matrix:")
    print(correlation.round(3).to_string())

    # ASCII heatmap: shade = |correlation|, sign shown in front of the cell.
    gradient = " .:-=+*#%@"          # index = |r| * 9  (0 -> blank, 1 -> '@')
    print("\nCorrelation Heatmap (ASCII; symbol shading = strength):")
    print("          " + " ".join(f"{c[:7]:>7}" for c in columns))
    for row_name in columns:
        cells = []
        for col_name in columns:
            value = correlation.loc[row_name, col_name]
            if pd.isna(value):            # constant column -> undefined r
                cells.append("  na    ")
                continue
            shade = gradient[min(int(abs(value) * 9.999), 9)]
            sign = "+" if value >= 0 else "-"
            cells.append(f"{sign}{shade}     ")
        print(f"{row_name[:8]:>8} " + " ".join(cells))


# ============================================================
# STEP 6 : TRAIN BOTH REGRESSION MODELS
# ============================================================
def train_models(df):
    """LinearRegression vs RandomForestRegressor on an 80/20 split."""
    X = df[["passenger_count", "hour", "day_of_week", "month",
            "pickup_longitude", "pickup_latitude",
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
# STEP 7 : EVALUATE + COMPARE + ASCII ACTUAL-VS-PREDICTED PLOT
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


def plot_actual_vs_predicted_ascii(actual, predicted, width=50, height=15):
    """Scatter plot in the terminal (no plotting library needed)."""
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    low = min(actual.min(), predicted.min())
    high = max(actual.max(), predicted.max())
    span = (high - low) or 1.0

    grid = [[" "] * width for _ in range(height)]
    for a, p in zip(actual, predicted):
        col = int((a - low) / span * (width - 1))
        row = int((1 - (p - low) / span) * (height - 1))
        grid[row][col] = "o"            # perfect model -> diagonal of 'o's

    print("\nActual vs Predicted - Random Forest (terminal scatter,")
    print("a perfect model draws the diagonal from bottom-left to top-right):")
    for row in grid:
        print("  " + "".join(row))
    print("  " + f"x-axis: actual ({low:.1f} .. {high:.1f}), "
          f"y-axis: predicted (same scale)")


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

    plot_actual_vs_predicted_ascii(y_test, rf_prediction)


if __name__ == "__main__":
    run()
