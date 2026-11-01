"""
QUESTION 1 (ML):
Predict the price of an Uber ride from a given pickup point to the agreed
drop-off location. Perform:
    1. Pre-process the dataset.
    2. Identify outliers.
    3. Check the correlation.
    4. Implement linear regression and random forest regression models.
    5. Evaluate the models and compare their scores (R2, RMSE, etc.).

Dataset: https://www.kaggle.com/datasets/yasserh/uber-fares-dataset

HOW IT WORKS
    uber.csv sits in the same folder as this file. If it is not there, Step 2
    writes a small hardcoded demo file (same columns) so the practical still
    runs. Step 3 loads whichever file is present.

STEPS
    1. Imports
    2. Create the dataset file if it is missing
    3. Load the dataset
    4. Preprocess
    5. Add distance and remove outliers
    6. Check the correlation
    7. Train linear regression and random forest
    8. Evaluate and compare the models
    9. Observation
    10. Plots with matplotlib

RUN
    python3 ml/py1_UberRegression.py

    In Jupyter, open py1_UberRegression.ipynb or split this file at the
    "# %%" markers.
"""

# %% Step 1: Imports
import os

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

if "__file__" in globals():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
else:
    SCRIPT_DIR = os.getcwd()

DATASET_FILE = os.path.join(SCRIPT_DIR, "uber.csv")

# %% Step 2: Create the dataset file if it is missing
# Skip this step when uber.csv is already in the folder.
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

if os.path.exists(DATASET_FILE):
    print(f"Using dataset: {DATASET_FILE}")
else:
    with open(DATASET_FILE, "w", encoding="utf-8") as file:
        file.write(DEMO_UBER_CSV)
    print(f"Created demo dataset: {DATASET_FILE}")

# %% Step 3: Load the dataset
df = pd.read_csv(DATASET_FILE)
print("\nShape:", df.shape)
print(df.head())

# %% Step 4: Preprocess
df = df.drop(columns=["Unnamed: 0", "key"], errors="ignore")
df = df.drop_duplicates()
df = df.dropna()

pickup = pd.to_datetime(df["pickup_datetime"])
df["hour"] = pickup.dt.hour
df["day_of_week"] = pickup.dt.day_of_week
df["month"] = pickup.dt.month

df = df[df["fare_amount"] > 0]
df = df[df["passenger_count"] > 0]

print("\nShape after preprocessing:", df.shape)

# %% Step 5: Add distance and remove outliers
def haversine(lat1, lon1, lat2, lon2):
    """Distance in km between two (lat, lon) points."""
    radius = 6371
    lat1, lat2 = np.radians(lat1), np.radians(lat2)
    dlat = lat2 - lat1
    dlon = np.radians(lon2) - np.radians(lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return radius * 2 * np.arcsin(np.sqrt(a))


df["distance_km"] = haversine(
    df["pickup_latitude"], df["pickup_longitude"],
    df["dropoff_latitude"], df["dropoff_longitude"])
df = df[df["distance_km"] > 0]

print("\nShape before removing outliers:", df.shape)
for column in ["fare_amount", "distance_km"]:
    q1, q3 = df[column].quantile([0.25, 0.75])
    iqr = q3 - q1
    df = df[df[column].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)]
print("Shape after removing outliers:", df.shape)

# %% Step 6: Check the correlation
columns = ["fare_amount", "passenger_count", "hour", "day_of_week", "month",
           "distance_km", "pickup_longitude", "pickup_latitude",
           "dropoff_longitude", "dropoff_latitude"]
correlation = df[columns].corr()

print("\nCorrelation Matrix:")
print(correlation.round(3).to_string())

# %% Step 7: Train linear regression and random forest
features = ["passenger_count", "hour", "day_of_week", "month",
            "pickup_longitude", "pickup_latitude",
            "dropoff_longitude", "dropoff_latitude", "distance_km"]

X = df[features]
y = df["fare_amount"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42)

linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_prediction = linear_model.predict(X_test)

forest = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
forest.fit(X_train, y_train)
rf_prediction = forest.predict(X_test)

# %% Step 8: Evaluate and compare the models
def evaluate(name, actual, predicted):
    """Print R2, MAE and RMSE for one model."""
    print(f"\n{name}")
    print("R2 Score :", round(r2_score(actual, predicted), 4))
    print("MAE      :", round(mean_absolute_error(actual, predicted), 4))
    print("RMSE     :", round(np.sqrt(mean_squared_error(actual, predicted)), 4))


evaluate("Linear Regression", y_test, linear_prediction)
evaluate("Random Forest Regression", y_test, rf_prediction)

# %% Step 9: Observation
print("\nObservation")
print("  The random forest usually gives the lower RMSE because it can learn")
print("  non-linear effects such as distance and time of day. Compare R2 and")
print("  RMSE for both models above.")

# %% Step 10: Plots with matplotlib
import matplotlib.pyplot as plt

sample = df.sample(min(5000, len(df)), random_state=42)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].scatter(sample["distance_km"], sample["fare_amount"],
                s=8, alpha=0.4, color="tab:blue")
axes[0].set_title("Trip distance vs fare")
axes[0].set_xlabel("Distance (km)")
axes[0].set_ylabel("Fare amount ($)")
axes[0].grid(alpha=0.3)

axes[1].hist(df["fare_amount"], bins=40, color="tab:green", edgecolor="white")
axes[1].set_title("Fare amount distribution")
axes[1].set_xlabel("Fare amount ($)")
axes[1].set_ylabel("Number of trips")
axes[1].grid(alpha=0.3)
fig.tight_layout()
plt.show()

fig, axis = plt.subplots(figsize=(8, 6.5))
image = axis.imshow(correlation, cmap="coolwarm", vmin=-1, vmax=1)
axis.set_xticks(range(len(columns)))
axis.set_yticks(range(len(columns)))
axis.set_xticklabels(columns, rotation=90)
axis.set_yticklabels(columns)
for row in range(len(columns)):
    for column in range(len(columns)):
        value = correlation.iat[row, column]
        axis.text(column, row, f"{value:.2f}", ha="center", va="center",
                  fontsize=7,
                  color="white" if abs(value) > 0.5 else "black")
axis.set_title("Correlation matrix (fare vs features)")
fig.colorbar(image, ax=axis, shrink=0.8)
fig.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharex=True, sharey=True)
for axis, name, prediction in [
        (axes[0], "Linear Regression", linear_prediction),
        (axes[1], "Random Forest", rf_prediction)]:
    axis.scatter(y_test, prediction, s=8, alpha=0.4, color="tab:blue")
    limit = [min(y_test.min(), prediction.min()),
             max(y_test.max(), prediction.max())]
    axis.plot(limit, limit, "r--", linewidth=1, label="perfect prediction")
    axis.set_title(name)
    axis.set_xlabel("Actual fare ($)")
    axis.set_ylabel("Predicted fare ($)")
    axis.grid(alpha=0.3)
    axis.legend()
fig.suptitle("Actual vs predicted fare")
fig.tight_layout()
plt.show()
