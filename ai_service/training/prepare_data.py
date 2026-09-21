import pandas as pd
import os


INPUT_PATH = "data/campus_helpdesk_cleaned_v2.csv"
OUTPUT_DIR = "data/processed"


def load_data():

    print("Loading dataset...")

    df = pd.read_csv(
        INPUT_PATH,
        low_memory=False
    )

    print(f"Dataset shape: {df.shape}")

    return df


def clean_text(df):

    df["title"] = df["title"].fillna("").astype(str)

    df["description"] = (
        df["description"]
        .fillna("")
        .astype(str)
    )

    df["text"] = (
        df["title"] +
        " " +
        df["description"]
    )

    return df


# =========================================================
# CATEGORY DATA
# =========================================================

def prepare_category_data(df):

    category_df = df[
        [
            "ticket_id",
            "title",
            "description",
            "text",
            "category"
        ]
    ].copy()

    # Remove rows without target
    category_df = category_df.dropna(
        subset=["category"]
    )

    # Remove empty text
    category_df = category_df[
        category_df["text"].str.strip() != ""
    ]

    output_path = os.path.join(
        OUTPUT_DIR,
        "category_data.csv"
    )

    category_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Category dataset saved: "
        f"{category_df.shape}"
    )


# =========================================================
# DUPLICATE DATA
# =========================================================

def prepare_duplicate_data(df):

    duplicate_df = df[
        [
            "ticket_id",
            "title",
            "description",
            "text",
            "duplicate_of"
        ]
    ].copy()

    # Create binary duplicate label
    duplicate_df["is_duplicate"] = (
        duplicate_df["duplicate_of"]
        .notna()
        .astype(int)
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        "duplicate_data.csv"
    )

    duplicate_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Duplicate dataset saved: "
        f"{duplicate_df.shape}"
    )

    print(
        "Duplicate distribution:"
    )

    print(
        duplicate_df["is_duplicate"]
        .value_counts()
    )


# =========================================================
# SLA DATA
# =========================================================

def prepare_sla_data(df):

    sla_columns = [
        "ticket_id",
        "title",
        "description",
        "text",

        "category",
        "issue_type",
        "urgency",
        "impact",
        "priority",
        "location_type",
        "is_emergency",

        "sla_breached"
    ]

    sla_df = df[sla_columns].copy()

    # Remove rows without target
    sla_df = sla_df.dropna(
        subset=["sla_breached"]
    )

    # Convert boolean target to int
    sla_df["sla_breached"] = (
        sla_df["sla_breached"]
        .astype(int)
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        "sla_data.csv"
    )

    sla_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"SLA dataset saved: "
        f"{sla_df.shape}"
    )

    print(
        "SLA distribution:"
    )

    print(
        sla_df["sla_breached"]
        .value_counts()
    )


# =========================================================
# MAIN
# =========================================================

def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    df = load_data()

    df = clean_text(df)

    prepare_category_data(df)

    prepare_duplicate_data(df)

    prepare_sla_data(df)

    print("\nData preparation completed!")


if __name__ == "__main__":
    main()