import pandas as pd

# Load the unscaled data
df = pd.read_csv('./data/processed/cleaned_fashion_boutique.csv')

# View the mean, standard deviation (std), min, and max
print(df['original_price'].describe())