import pandas as pd


DATA_PATH = "data/processed/duplicate_pairs.csv"

df = pd.read_csv(DATA_PATH)

# Sort tickets by similarity score
df = df.sort_values(
    "combined_similarity",
    ascending=False
).reset_index(drop=True)

total_duplicates = df["label"].sum()

print("Total duplicate pairs:", total_duplicates)

print("\n==============================")
print("DUPLICATE PRECISION@K")
print("==============================")

for k in [1, 5, 10, 20, 50]:

    top_k = df.head(k)

    precision_at_k = top_k["label"].sum() / k

    print(
        f"Precision@{k}: "
        f"{precision_at_k:.4f}"
    )

print("\nEvaluation completed.")