import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

# === load dataset ===
raw_data_path = os.path.join('data','raw','fashion_boutique_dataset.csv')
df = pd.read_csv(raw_data_path)

# === process data ===

# fill the NaN entries of ratings with median
rating_median = df['customer_rating'].median()
df['customer_rating'] = df['customer_rating'].fillna(rating_median)

# acessories have null size. make it N/A
df.loc[df['category'] == 'Accessories', 'size'] = 'N/A'

# any other null sizes with unknown
df['size'] = df['size'].fillna('Unknown')

# === extract seasonal features ===

# convert string dates into datetime objects
df['purchase_date'] = pd.to_datetime(df['purchase_date'])

df['purchase_month'] = df['purchase_date'].dt.month
df['purchase_quarter'] = df['purchase_date'].dt.quarter

# === stocking priority ===

# logical conditions for inventory tiers
conditions = [
    (df['customer_rating'] > 4.0) & (df['is_returned'] == False),   # high priority
    (df['customer_rating'] < 2.0) | (df['is_returned'] == True)     # low priority
]

choices = ['High Stock', 'Low Stock']
df['stocking_priority'] = np.select(conditions, choices, default='Maintain')

# === final data preparation ===

# remove product_id, return_reason
# return_reason is removed because it happens after a return
# so it cannot be used to predict stocking priority
df_cleaned = df.drop(columns=['product_id', 'return_reason'])

# === scale price columns ===
# apply StandardScaler to price columns so distance-based models aren't biased
price_cols = [c for c in ['original_price', 'current_price'] if c in df_cleaned.columns]
if price_cols:
    scaler = StandardScaler()
    df_cleaned[price_cols] = scaler.fit_transform(df_cleaned[price_cols])
    print(f"Scaled columns: {price_cols}")

# === export processed data ===
processed_path = os.path.join('data', 'processed', 'cleaned_fashion_boutique.csv')
df_cleaned.to_csv(processed_path, index=False)
print(f"Final data saved to {processed_path}")