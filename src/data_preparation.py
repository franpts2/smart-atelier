import pandas as pd
import numpy as np
import os

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

# === calculate Net_Margin ===

# Assuming theoretical cost is 40% of original price
if 'original_price' in df.columns:
    theoretical_cost = df['original_price'] * 0.40
else:
    theoretical_cost = df['current_price'] * 0.50 

df['Net_Margin'] = df['current_price'] - theoretical_cost

# === Encode Brands & Categories (no sklearn required) ===

# Use pandas factorize to create integer codes without sklearn
if 'brand' in df.columns:
    df['brand_encoded'] = pd.factorize(df['brand'].astype(str))[0]

if 'category' in df.columns:
    df['category_encoded'] = pd.factorize(df['category'].astype(str))[0]

# === final data preparation ===

# remove product_id, return_reason
# return_reason is removed because it happens after a return
# so it cannot be used to predict stocking priority
df_cleaned = df.drop(columns=['product_id', 'return_reason'])

# === export processed data ===
processed_path = os.path.join('data', 'processed', 'cleaned_fashion_boutique.csv')
df_cleaned.to_csv(processed_path, index=False)
print(f"Final data saved to {processed_path}")