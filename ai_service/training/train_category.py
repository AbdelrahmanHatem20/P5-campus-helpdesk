import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import joblib


# ============================================
# 1. Load Dataset
# ============================================

DATA_PATH = "data/processed/category_data.csv"

print("Loading category dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")


# ============================================
# 2. Prepare Data
# ============================================

X = df["text"].fillna("")
y = df["category"]


print("\nNumber of categories:")
print(y.nunique())

print("\nCategory distribution:")
print(y.value_counts())


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
# 6. Prediction
# ============================================

print("\nEvaluating model...")

y_pred = model.predict(X_test_tfidf)


# ============================================
# 7. Evaluation
# ============================================

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("CATEGORY MODEL RESULTS")
print("==============================")

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ============================================
# 8. Save Model
# ============================================

MODEL_DIR = "models/category"

os.makedirs(MODEL_DIR, exist_ok=True)

model_path = os.path.join(
    MODEL_DIR,
    "category_model.joblib"
)

vectorizer_path = os.path.join(
    MODEL_DIR,
    "category_vectorizer.joblib"
)

joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print("\nModels saved successfully!")

print("Model:", model_path)
print("Vectorizer:", vectorizer_path)