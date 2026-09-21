import pandas as pd

DATA_PATH = "data/processed/duplicate_data.csv"

df = pd.read_csv(DATA_PATH)

duplicates = df[df["is_duplicate"] == 1].copy()

print("Number of duplicates:", len(duplicates))

print("\nDuplicate columns:")
print(
    duplicates[
        [
            "ticket_id",
            "title",
            "description",
            "duplicate_of",
            "is_duplicate"
        ]
    ].head(20).to_string(index=False)
)


print("\n================================")
print("DUPLICATE EXAMPLES")
print("================================")

for _, row in duplicates.head(10).iterrows():

    original_id = row["duplicate_of"]

    original = df[
        df["ticket_id"] == original_id
    ]

    print("\n--------------------------------")
    print("DUPLICATE TICKET")
    print("--------------------------------")

    print("ID:", row["ticket_id"])
    print("Title:", row["title"])
    print("Description:", row["description"])

    print("\nDuplicate of:", original_id)

    if len(original) > 0:

        original = original.iloc[0]

        print("\nORIGINAL TICKET")
        print("Title:", original["title"])
        print("Description:", original["description"])