import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

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

# === create reproducible train/test split ===
# use stratified split on `stocking_priority` if present to keep class balance
split_kwargs = dict(test_size=0.2, random_state=42, shuffle=True)
stratify_col = None
if 'stocking_priority' in df_cleaned.columns and df_cleaned['stocking_priority'].nunique() > 1:
    stratify_col = df_cleaned['stocking_priority']

train_df, test_df = train_test_split(df_cleaned, stratify=stratify_col, **split_kwargs)

train_df = train_df.copy()
test_df = test_df.copy()


# === calculate Net_Margin ===

# Assuming theoretical cost is 40% of original price
for data in [train_df, test_df]:
    theoretical_cost = data['original_price'] * 0.40 if 'original_price' in data.columns else data['current_price'] * 0.50
    data['Net_Margin'] = data['current_price'] - theoretical_cost



# === Encode Brands & Categories ===

# Create consistent mappings from the full cleaned dataset
brand_map = {brand: i for i, brand in enumerate(df_cleaned['brand'].astype(str).unique())}
category_map = {cat: i for i, cat in enumerate(df_cleaned['category'].astype(str).unique())}

for data in [train_df, test_df]:
    if 'brand' in data.columns:
        data['brand_encoded'] = data['brand'].astype(str).map(brand_map)
    if 'category' in data.columns:
        data['category_encoded'] = data['category'].astype(str).map(category_map)

# === scale price columns ===
# apply StandardScaler to price columns so distance-based models aren't biased
scale_cols = ['original_price', 'current_price', 'Net_Margin']
    
scaler = StandardScaler()

train_df[scale_cols] = scaler.fit_transform(train_df[scale_cols])
test_df[scale_cols] = scaler.transform(test_df[scale_cols])

# round the price columns to 3 decimal places
train_df[scale_cols] = train_df[scale_cols].round(3)
test_df[scale_cols] = test_df[scale_cols].round(3)
    


train_path = os.path.join('data', 'processed', 'train.csv')
test_path = os.path.join('data', 'processed', 'test.csv')

train_df.to_csv(train_path, index=False)
test_df.to_csv(test_path, index=False)

print(f"Saved train/test split to {train_path} and {test_path} (test_size=0.2, random_state=42)")
