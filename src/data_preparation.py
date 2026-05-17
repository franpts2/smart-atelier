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

# === calculate Net_Margin ===

# Assuming theoretical cost is 40% of original price
if 'original_price' in df.columns:
    theoretical_cost = df['original_price'] * 0.40
else:
    theoretical_cost = df['current_price'] * 0.50 

df['Net_Margin'] = df['current_price'] - theoretical_cost


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

# === Encode Brands & Categories (no sklearn required) ===

# Use pandas factorize to create integer codes without sklearn
for data in [train_df, test_df]:
    if 'brand' in data.columns:
        data['brand_encoded'] = pd.factorize(data['brand'].astype(str))[0]
    if 'category' in data.columns:
        data['category_encoded'] = pd.factorize(data['category'].astype(str))[0]

# === scale price columns ===
# apply StandardScaler to price columns so distance-based models aren't biased
price_cols = [c for c in ['original_price', 'current_price'] if c in train_df.columns]
if price_cols:
    scaler = StandardScaler()
    train_df[price_cols] = scaler.fit_transform(train_df[price_cols])
    test_df[price_cols] = scaler.transform(test_df[price_cols])

    # round the price columns to 3 decimal places
    train_df[price_cols] = train_df[price_cols].round(3)
    test_df[price_cols] = test_df[price_cols].round(3)
    
    #print(f"Scaled columns: {price_cols}")

# === export processed data ===
#processed_path = os.path.join('data', 'processed', 'cleaned_fashion_boutique.csv')
#df_cleaned.to_csv(processed_path, index=False)
#print(f"Final data saved to {processed_path}")


train_path = os.path.join('data', 'processed', 'train.csv')
test_path = os.path.join('data', 'processed', 'test.csv')

train_df.to_csv(train_path, index=False)
test_df.to_csv(test_path, index=False)

print(f"Saved train/test split to {train_path} and {test_path} (test_size=0.2, random_state=42)")