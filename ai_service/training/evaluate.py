import pandas as pd
import sys
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.category_classifier import CategoryClassifier


DATA_PATH = "data/tickets.csv"


def main():

    df = pd.read_csv(DATA_PATH)

    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")

    df["text"] = (
        df["title"] + " " + df["description"]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["category"],
        test_size=0.2,
        random_state=42,
        stratify=df["category"]
    )

    classifier = CategoryClassifier()

    classifier.train(
        X_train,
        y_train
    )

    predictions = []

    for text in X_test:
        result = classifier.predict(text)
        predictions.append(result["category"])

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print("\n===== MODEL EVALUATION =====")

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    print("\n===== CLASSIFICATION REPORT =====")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    print("\n===== CONFUSION MATRIX =====")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )


if __name__ == "__main__":
    main()