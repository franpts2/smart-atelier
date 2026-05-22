import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# === load dataset ===
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_data_path = os.path.join(base_dir, "data", "raw", "fashion_boutique_dataset.csv")
df = pd.read_csv(raw_data_path)

# === process data ===

# fill the NaN entries of ratings with median
rating_median = df["customer_rating"].median()
df["customer_rating"] = df["customer_rating"].fillna(rating_median)

# acessories have null size. make it N/A
df.loc[df["category"] == "Accessories", "size"] = "N/A"

# any other null sizes with unknown
df["size"] = df["size"].fillna("Unknown")

# === extract seasonal features ===

# convert string dates into datetime objects
df["purchase_date"] = pd.to_datetime(df["purchase_date"])
df["purchase_month"] = df["purchase_date"].dt.month
df["purchase_quarter"] = df["purchase_date"].dt.quarter

# Assuming theoretical cost is 40% of original price
df["Net_Margin"] = df["current_price"] - (df["original_price"] * 0.40)

# Group by category and brand to count units sold (sales frequency)
units_sold_df = df.groupby(["category", "brand"]).size().reset_index(name="units_sold")
df = df.merge(units_sold_df, on=["category", "brand"], how="left")

# Save units_sold_map to artifacts
artifacts_dir = os.path.join(base_dir, "models", "artifacts")
os.makedirs(artifacts_dir, exist_ok=True)
units_sold_map = {
    (row["category"], row["brand"]): int(row["units_sold"])
    for _, row in units_sold_df.iterrows()
}
joblib.dump(units_sold_map, os.path.join(artifacts_dir, "units_sold_map.joblib"))

# === stocking priority ===
conditions_std = [
    (df["customer_rating"] > 4.0) & (df["is_returned"] == False),  # high priority
    (df["customer_rating"] < 2.0) | (df["is_returned"] == True),  # low priority
]
choices = ["High Stock", "Low Stock"]
df["stocking_priority"] = np.select(conditions_std, choices, default="Maintain")

# Advanced stocking priority rules
conditions_adv = [
    (df["units_sold"] >= 15) & (df["customer_rating"] >= 3.8) & (df["is_returned"] == False) & (df["Net_Margin"] > 0) & (df["stock_quantity"] < df["units_sold"] * 1.5),
    (df["is_returned"] == True) | (df["customer_rating"] < 2.5) | (df["units_sold"] < 5) | (df["Net_Margin"] <= 0) | (df["stock_quantity"] > df["units_sold"] * 3.0),
]
df["stocking_priority_advanced"] = np.select(conditions_adv, choices, default="Maintain")

# === final data preparation ===

# remove product_id, return_reason
df_cleaned = df.drop(columns=["product_id", "return_reason"])

# === create reproducible train/test split ===
split_kwargs = dict(test_size=0.2, random_state=42, shuffle=True)
stratify_col = None
if (
    "stocking_priority" in df_cleaned.columns
    and df_cleaned["stocking_priority"].nunique() > 1
):
    stratify_col = df_cleaned["stocking_priority"]

train_df, test_df = train_test_split(df_cleaned, stratify=stratify_col, **split_kwargs)

train_df = train_df.copy()
test_df = test_df.copy()


# === Encode Brands & Categories ===

# Create consistent mappings from the full cleaned dataset
brand_map = {
    brand: i for i, brand in enumerate(df_cleaned["brand"].astype(str).unique())
}
category_map = {
    cat: i for i, cat in enumerate(df_cleaned["category"].astype(str).unique())
}

# Save mappings for backend use
joblib.dump(brand_map, os.path.join(artifacts_dir, "brand_map.joblib"))
joblib.dump(category_map, os.path.join(artifacts_dir, "category_map.joblib"))

for data in [train_df, test_df]:
    if "brand" in data.columns:
        data["brand_encoded"] = data["brand"].astype(str).map(brand_map)
    if "category" in data.columns:
        data["category_encoded"] = data["category"].astype(str).map(category_map)

# === scale columns ===
scale_cols_std = ["original_price", "current_price", "Net_Margin"]
scale_cols_adv = ["original_price", "current_price", "Net_Margin", "units_sold"]

scaler_std = StandardScaler()
scaler_adv = StandardScaler()

# Fit on training data
scaler_std.fit(train_df[scale_cols_std])
scaler_adv.fit(train_df[scale_cols_adv])

# Apply scaling to datasets
train_df[scale_cols_std] = scaler_std.transform(train_df[scale_cols_std])
test_df[scale_cols_std] = scaler_std.transform(test_df[scale_cols_std])

train_df["units_sold"] = scaler_adv.transform(train_df[scale_cols_adv])[:, 3]
test_df["units_sold"] = scaler_adv.transform(test_df[scale_cols_adv])[:, 3]

# Save scalers for backend use
joblib.dump(scaler_std, os.path.join(artifacts_dir, "scaler.joblib"))
joblib.dump(scaler_adv, os.path.join(artifacts_dir, "scaler_advanced.joblib"))

# round the price columns to 3 decimal places
train_df[scale_cols_adv] = train_df[scale_cols_adv].round(3)
test_df[scale_cols_adv] = test_df[scale_cols_adv].round(3)


train_path = os.path.join(base_dir, "data", "processed", "train.csv")
test_path = os.path.join(base_dir, "data", "processed", "test.csv")

train_df.to_csv(train_path, index=False)
test_df.to_csv(test_path, index=False)

print(
    f"Saved train/test split to {train_path} and {test_path} (test_size=0.2, random_state=42)"
)
print(f"Saved artifacts to {artifacts_dir}")

