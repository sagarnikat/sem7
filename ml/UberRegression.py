"""
PROBLEM STATEMENT : Uber fare prediction - Linear & Random Forest Regression (ML)

Predict the numeric fare (fare_amount) of an Uber ride from pickup/dropoff
coordinates and passenger count, first with a plain LinearRegression and
then with a RandomForestRegressor, and compare them with R2, MAE and RMSE.
This practical shows the full REGRESSION pipeline: an end-to-end data
preparation phase (cleaning, feature engineering, outliers) before any
model is fitted, because a regression is only as good as its data.

HOW IT WORKS:
1. DATA - uber.csv in the working directory (Kaggle "Uber Fares Dataset";
   fix any PDF-copy column-name corruption like "dropoƯ_longitude").
2. CLEAN - drop an unnamed index column, duplicate rows and NAs; force the
   numeric columns to numbers (bad strings become NaN, dropped after).
3. RULE OUT IMPOSSIBLE RIDES - positive fares only, 1-6 passengers, and
   latitudes/longitudes inside the legal globe range. Data science is
   mostly data sanity checks, and this cell is the point of the lesson.
4. FEATURE ENGINEERING - the Haversine formula computes the great-circle
   distance in km from the two coordinate pairs on the sphere:
        a = sin^2(dlat/2) + cos(lat1) cos(lat2) sin^2(dlon/2)
        d = 2 R arcsin(sqrt(a))        (R = 6371 km, Earth's radius)
   Raw coordinates correlate with fare in a twisted non-linear way; a
   distance column is the feature an actual fare ~ distance relation uses.
   Zero-distance rides are dropped (GPS errors / staged pickups).
5. OUTLIERS (IQR method) - keep only rows inside
        [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
   for fare_amount AND distance_km. One 10,000 km fare would wreck least
   squares: squared errors punish outliers quadratically.
6. CORRELATION HEATMAP - check which feature actually relates to the fare
   before modelling (distance_km should dominate).
7. SPLIT - 80/20 train/test, then:
   - LinearRegression: fits coefficients minimising least squares; a
     straight line/hyper-plane through feature space.
   - RandomForestRegressor(100 trees): averages many decision trees, each
     trained on a random row subset with random feature splits (bagging).
     Captures non-linear fare rules (minima, surcharges) linears cannot.
8. EVALUATE & COMPARE -
   R2  = 1 - SS_res/SS_tot (1 = perfect, 0 = predicting the mean),
   MAE = mean absolute rupee error (robust, interpretable),
   RMSE = root mean squared error (punishes big misses; comparable to the
   target scale). Then a scatter of actual vs predicted fare for the
   forest: a good model hugs the diagonal y = x.

NOTE - plot windows only open with a display:
run from a desktop session (the heatmap/scatter call plt.show());
over SSH headless, comment the two plt.show() lines or use Agg backend.

NEEDS:  pip install pandas numpy matplotlib seaborn scikit-learn
RUN:    python3 "ml/UberRegression.py"   (uber.csv in the same directory)
"""

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

# Only force a non-GUI backend when there is no display (headless SSH).
if not os.environ.get("DISPLAY"):
    matplotlib.use("Agg")


def load_dataset():
    """Read uber.csv and fix the known PDF-copy column name corruption."""
    df = pd.read_csv("uber.csv")
    df.rename(
        columns={
            "dropoƯ_longitude": "dropoff_longitude",
            "dropoƯ_latitude": "dropoff_latitude",
        },
        inplace=True,
    )

    print("First 5 rows:")
    print(df.head())
    print("\nDataset Shape:", df.shape)
    print("\nMissing Values:")
    print(df.isnull().sum(), "\n")
    return df


def clean_data(df):
    """Drop index column, duplicates, NAs; enforce numeric fare/passengers."""
    if "Unnamed: 0" in df.columns:
        df = df.drop("Unnamed: 0", axis=1)

    df = df.drop_duplicates().dropna()

    numeric_columns = [
        "fare_amount", "pickup_longitude", "pickup_latitude",
        "dropoff_longitude", "dropoff_latitude", "passenger_count",
    ]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")  # bad text -> NaN
    df = df.dropna()
    return df


def filter_invalid_values(df):
    """Physical sanity: positive fare, 1-6 passengers, legal globe range."""
    df = df[df["fare_amount"] > 0]
    df = df[(df["passenger_count"] >= 1) & (df["passenger_count"] <= 6)]
    df = df[
        df["pickup_latitude"].between(-90, 90)
        & df["dropoff_latitude"].between(-90, 90)
        & df["pickup_longitude"].between(-180, 180)
        & df["dropoff_longitude"].between(-180, 180)
    ].copy()
    return df


def haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance in km between two (lat, lon) points, vectorised."""
    R = 6371  # Earth radius in km
    lat1, lat2 = np.radians(lat1), np.radians(lat2)
    dlat = lat2 - lat1
    dlon = np.radians(lon2) - np.radians(lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))  # clip: rounding guards arcsin
    return R * c


def add_distance_feature(df):
    """Step 4: engineer distance_km from the four coordinate columns."""
    df["distance_km"] = haversine(
        df["pickup_latitude"], df["pickup_longitude"],
        df["dropoff_latitude"], df["dropoff_longitude"],
    )
    return df[df["distance_km"] > 0].copy()


def remove_outliers_iqr(df, column):
    """IQR rule on one column; returns the trimmed frame."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)].copy()


def show_correlation_heatmap(df):
    """Step 6: which columns actually relate to fare_amount."""
    correlation = df[
        ["fare_amount", "passenger_count", "pickup_longitude", "pickup_latitude",
         "dropoff_longitude", "dropoff_latitude", "distance_km"]
    ].corr()
    print("Correlation Matrix:")
    print(correlation, "\n")

    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.savefig("correlation_heatmap.png", dpi=120, bbox_inches="tight")
    plt.show()  # comment out when running headless; PNG is always written


def split_data(df):
    """Step 7a: features vs target and the 80/20 train-test split."""
    X = df[
        ["passenger_count", "pickup_longitude", "pickup_latitude",
         "dropoff_longitude", "dropoff_latitude", "distance_km"]
    ]
    y = df["fare_amount"]
    return train_test_split(X, y, test_size=0.20, random_state=42)


def evaluate_model(name, actual, predicted):
    """R2 / MAE / RMSE for one model (passed y_test and the predictions)."""
    r2 = r2_score(actual, predicted)
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    print(f"\n{name}\n---------------------------")
    print("R2 Score :", round(float(r2), 4))
    print("MAE      :", round(float(mae), 4))
    print("RMSE     :", round(float(rmse), 4))
    return {"Model": name, "R2 Score": r2, "MAE": mae, "RMSE": rmse}


def plot_actual_vs_predicted(y_test, prediction, title):
    """Step 13 diagnostic: predictions hugging the y = x diagonal = good."""
    plt.figure(figsize=(8, 5))
    plt.scatter(y_test, prediction, alpha=0.5)
    plt.xlabel("Actual Fare")
    plt.ylabel("Predicted Fare")
    plt.title(title)
    plt.savefig("actual_vs_predicted.png", dpi=120, bbox_inches="tight")
    plt.show()


def run():
    """Full regression pipeline; main() only calls this."""
    df = load_dataset()
    df = clean_data(df)
    df = filter_invalid_values(df)
    print("Shape after cleaning:", df.shape, "\n")

    df = add_distance_feature(df)

    print("Shape before removing outliers:", df.shape)
    df = remove_outliers_iqr(df, "fare_amount")   # cheapest big wins first
    df = remove_outliers_iqr(df, "distance_km")
    print("Shape after removing outliers:", df.shape, "\n")

    X_train, X_test, y_train, y_test = split_data(df)

    # Model 1: ordinary least squares (assumes a linear fare relation).
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    linear_prediction = linear_model.predict(X_test)

    # Model 2: 100 randomised decision trees, averaged (handles non-linearity).
    random_forest = RandomForestRegressor(
        n_estimators=100, random_state=42, n_jobs=-1
    )
    random_forest.fit(X_train, y_train)
    rf_prediction = random_forest.predict(X_test)

    # Side-by-side comparison of the two models.
    linear_scores = evaluate_model("Linear Regression", y_test, linear_prediction)
    rf_scores = evaluate_model("Random Forest Regression", y_test, rf_prediction)

    comparison = pd.DataFrame([linear_scores, rf_scores])
    print("\nModel Comparison:")
    print(comparison.to_string(index=False), "\n")

    show_correlation_heatmap(df)
    plot_actual_vs_predicted(y_test, rf_prediction,
                             "Actual vs Predicted Fare - Random Forest")


if __name__ == "__main__":
    run()
