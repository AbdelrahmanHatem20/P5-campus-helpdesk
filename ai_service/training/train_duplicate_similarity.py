import os

import joblib
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_PATH = "data/processed/duplicate_data.csv"


# ============================================
# 1. Load Dataset
# ============================================

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# ============================================
# 2. Split Original and Duplicate Tickets
# ============================================

positive = df[df["is_duplicate"] == 1].copy()

print("\nPositive duplicate pairs:", len(positive))


# ============================================
# 3. Build Ticket Lookup
# ============================================

ticket_lookup = df.set_index("ticket_id")


# ============================================
# 4. Build Positive Pairs
# ============================================

positive_pairs = []

for _, row in positive.iterrows():

    duplicate_id = row["ticket_id"]
    original_id = row["duplicate_of"]

    if original_id not in ticket_lookup.index:
        continue

    original = ticket_lookup.loc[original_id]

    positive_pairs.append({
        "title_1": str(original["title"]),
        "description_1": str(original["description"]),
        "title_2": str(row["title"]),
        "description_2": str(row["description"]),
        "label": 1
    })


positive_pairs = pd.DataFrame(positive_pairs)

print("Valid positive pairs:", len(positive_pairs))


# ============================================
# 5. Build Negative Pairs
# ============================================

# Randomly pair duplicate tickets with unrelated tickets.
# We make the number of negatives equal to positives.

rng = np.random.default_rng(42)

non_duplicates = df[df["is_duplicate"] == 0].copy()

negative_pairs = []

for _, row in positive.iterrows():

    random_row = non_duplicates.iloc[
        rng.integers(0, len(non_duplicates))
    ]

    negative_pairs.append({
        "title_1": str(row["title"]),
        "description_1": str(row["description"]),
        "title_2": str(random_row["title"]),
        "description_2": str(random_row["description"]),
        "label": 0
    })


negative_pairs = pd.DataFrame(negative_pairs)


# ============================================
# 6. Combine Pairs
# ============================================

pairs = pd.concat(
    [positive_pairs, negative_pairs],
    ignore_index=True
)

pairs = pairs.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


print("\nPair dataset:")
print(pairs["label"].value_counts())


# ============================================
# 7. Create Text Fields
# ============================================

pairs["title_1"] = pairs["title_1"].fillna("")
pairs["title_2"] = pairs["title_2"].fillna("")

pairs["description_1"] = pairs["description_1"].fillna("")
pairs["description_2"] = pairs["description_2"].fillna("")


# ============================================
# 8. Title Similarity
# ============================================

all_titles = pd.concat([
    pairs["title_1"],
    pairs["title_2"]
])

title_vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

title_vectorizer.fit(all_titles)


title_1 = title_vectorizer.transform(
    pairs["title_1"]
)

title_2 = title_vectorizer.transform(
    pairs["title_2"]
)


title_similarity = []

for i in range(len(pairs)):

    score = cosine_similarity(
        title_1[i],
        title_2[i]
    )[0][0]

    title_similarity.append(score)


pairs["title_similarity"] = title_similarity


# ============================================
# 9. Description Similarity
# ============================================

all_descriptions = pd.concat([
    pairs["description_1"],
    pairs["description_2"]
])

description_vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

description_vectorizer.fit(all_descriptions)


description_1 = description_vectorizer.transform(
    pairs["description_1"]
)

description_2 = description_vectorizer.transform(
    pairs["description_2"]
)


description_similarity = []

for i in range(len(pairs)):

    score = cosine_similarity(
        description_1[i],
        description_2[i]
    )[0][0]

    description_similarity.append(score)


pairs["description_similarity"] = description_similarity


# ============================================
# 10. Combined Similarity
# ============================================

pairs["combined_similarity"] = (
    0.7 * pairs["title_similarity"]
    +
    0.3 * pairs["description_similarity"]
)


# ============================================
# 11. Analyze Results
# ============================================

print("\n================================")
print("SIMILARITY RESULTS")
print("================================")

print("\nPositive pairs:")
print(
    pairs[pairs["label"] == 1][
        [
            "title_similarity",
            "description_similarity",
            "combined_similarity"
        ]
    ].describe()
)

print("\nNegative pairs:")
print(
    pairs[pairs["label"] == 0][
        [
            "title_similarity",
            "description_similarity",
            "combined_similarity"
        ]
    ].describe()
)


# ============================================
# 12. Save Pair Dataset
# ============================================

os.makedirs(
    "data/processed",
    exist_ok=True
)

output_path = (
    "data/processed/duplicate_pairs.csv"
)

pairs.to_csv(
    output_path,
    index=False
)

print("\nPair dataset saved:")
print(output_path)