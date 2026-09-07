import pandas as pd
import numpy as np

df = pd.read_csv("UberCabFare.csv")
print(df.shape)
print(df.head())
print(df.tail())
print(df.info())
print(df.isnull().sum())
df["Driver_Name"] = df["Driver_Name"].fillna("Unknown")
print("Duplicate rows:", df.duplicated().sum())
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print(df.columns)
text_columns = [
    "driver_name",
    "city",
    "day_of_week",
    "traffic_level",
    "type_of_vehicle"
]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

print(df["city"].head())
print(df["day_of_week"].head())
print(df["traffic_level"].head())
print(df["type_of_vehicle"].head())
df["ride_date"] = pd.to_datetime(
    df["ride_date"],
    format="%d-%m-%Y",
    errors="coerce"
)
print(df["ride_date"].head())
numeric_columns = [
    "hour_of_day",
    "distance_km",
    "no_of_active_drivers",
    "ride_requests",
    "demand_supply_ratio",
    "trip_duration",
    "base_fare",
    "surge_multiplier",
    "final_fare"
]

print(df[numeric_columns].describe())
for col in numeric_columns:
    negative_count = (df[col] < 0).sum()
    print(f"{col}: {negative_count} negative values")

invalid_hours = df[
    (df["hour_of_day"] < 0) |
    (df["hour_of_day"] > 23)
]

print("Invalid hours:", len(invalid_hours))
invalid_distance = df[df["distance_km"] <= 0]

print("Invalid distance records:", len(invalid_distance))
invalid_drivers = df[df["no_of_active_drivers"] <= 0]

print("Invalid driver records:", len(invalid_drivers))
invalid_requests = df[df["ride_requests"] <= 0]

print("Invalid ride request records:", len(invalid_requests))
df["calculated_ratio"] = (
    df["ride_requests"] /
    df["no_of_active_drivers"]
)

df["ratio_difference"] = (
    df["demand_supply_ratio"] -
    df["calculated_ratio"]
).abs()

print(df["ratio_difference"].describe())
print(
    "Ratio mismatches:",
    (df["ratio_difference"] > 0.01).sum()
)
df["calculated_final_fare"] = (
    df["base_fare"] *
    df["surge_multiplier"]
)

df["fare_difference"] = (
    df["final_fare"] -
    df["calculated_final_fare"]
).abs()

print(df["fare_difference"].describe())
df["base_fare"] = df["base_fare"].round(2)
df["final_fare"] = df["final_fare"].round(2)
df["demand_supply_ratio"] = df["demand_supply_ratio"].round(2)
df["surge_multiplier"] = df["surge_multiplier"].round(2)
print(df.columns)
df = df.drop(
    columns=[
        "calculated_ratio",
        "ratio_difference",
        "calculated_final_fare",
        "fare_difference"
    ]
)
print(df.info())
print("========== DATA QUALITY REPORT ==========")

print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Duplicate rows:", df.duplicated().sum())
print("Missing values:", df.isnull().sum().sum())

print("\nColumn data types:")
print(df.dtypes)

print("\nDate range:")
print(df["ride_date"].min(), "to", df["ride_date"].max())
df.to_csv("UberCabFare_Cleaned.csv", index=False)

print("Clean CSV created successfully!")
print(df.columns)
print("Unique vehicle types:")
print(df["type_of_vehicle"].unique())
