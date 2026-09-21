import os

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split


# ============================================
# 1. Load Dataset
# ============================================

DATA_PATH = "data/processed/duplicate_data.csv"

print("Loading duplicate dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")


# ============================================
# 2. Prepare Data
# ============================================

# IMPORTANT:
# We intentionally DO NOT use:
# - ticket_id
# - duplicate_of
#
# because duplicate_of directly reveals the target
# and would cause data leakage.

X = df["text"].fillna("")
y = df["is_duplicate"]


print("\nTarget distribution:")
print(y.value_counts())

print("\nDuplicate ratio:")
print(y.mean())


# ============================================
# 3. Train / Test Split
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTrain size:", len(X_train))
print("Test size:", len(X_test))

print("\nTrain target distribution:")
print(y_train.value_counts())

print("\nTest target distribution:")
print(y_test.value_counts())


# ============================================
# 4. TF-IDF
# ============================================

print("\nCreating TF-IDF...")

vectorizer = TfidfVectorizer(
    lowercase=True,
    max_features=20000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("TF-IDF train shape:", X_train_tfidf.shape)
print("TF-IDF test shape:", X_test_tfidf.shape)


# ============================================
# 5. Train Model
# ============================================

print("\nTraining Logistic Regression...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_tfidf, y_train)

print("Training completed!")


# ============================================
# 6. Predictions
# ============================================

print("\nGenerating predictions...")

# Probability of duplicate class
y_prob = model.predict_proba(X_test_tfidf)[:, 1]
print("\n================================")
print("THRESHOLD ANALYSIS")
print("================================")

thresholds = [
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90
]

for threshold in thresholds:

    y_threshold_pred = (
        y_prob >= threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        y_threshold_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_threshold_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_threshold_pred,
        zero_division=0
    )

    cm = confusion_matrix(
        y_test,
        y_threshold_pred
    )

    tn, fp, fn, tp = cm.ravel()

    print(
        f"\nThreshold: {threshold:.2f}"
    )

    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1:        {f1:.4f}")
    print(f"FP:        {fp}")
    print(f"FN:        {fn}")
    print(f"TP:        {tp}")

# Default threshold
threshold = 0.50

y_pred = (y_prob >= threshold).astype(int)


# ============================================
# 7. Evaluation
# ============================================

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

pr_auc = average_precision_score(
    y_test,
    y_prob
)


print("\n================================")
print("DUPLICATE MODEL RESULTS")
print("================================")

print(f"\nThreshold: {threshold:.2f}")

print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"PR-AUC:    {pr_auc:.4f}")


print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Not Duplicate", "Duplicate"],
        zero_division=0
    )
)


print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ============================================
# 8. Save Model
# ============================================

MODEL_DIR = "models/duplicate"

os.makedirs(MODEL_DIR, exist_ok=True)

model_path = os.path.join(
    MODEL_DIR,
    "duplicate_model.joblib"
)

vectorizer_path = os.path.join(
    MODEL_DIR,
    "duplicate_vectorizer.joblib"
)

joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print("\nModels saved successfully!")

print("Model:", model_path)
print("Vectorizer:", vectorizer_path)