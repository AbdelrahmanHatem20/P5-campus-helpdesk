import pandas as pd

DATA_PATH = "data/processed/sla_data.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nTarget distribution:")
print(df["sla_breached"].value_counts())

print("\nTarget percentage:")
print(df["sla_breached"].value_counts(normalize=True))