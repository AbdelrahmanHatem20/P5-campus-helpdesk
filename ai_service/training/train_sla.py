import os

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, classification_report


DATA_PATH = "data/processed/sla_data.csv"

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

features = [
    "category",
    "issue_type",
    "urgency",
    "impact",
    "priority",
    "location_type",
    "is_emergency"
]

target = "sla_breached"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

categorical_features = [
    "category",
    "issue_type",
    "urgency",
    "impact",
    "priority",
    "location_type"
]

numeric_features = [
    "is_emergency"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ]
)

print("\nTraining SLA model...")

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

recall = recall_score(
    y_test,
    y_pred
)

print("\n================================")
print("SLA MODEL RESULTS")
print("================================")

print(f"Recall: {recall:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

os.makedirs("models/sla", exist_ok=True)

model_path = "models/sla/sla_model.joblib"

joblib.dump(
    model,
    model_path
)

print("\nModel saved:")
print(model_path)