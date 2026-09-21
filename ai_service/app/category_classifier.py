import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class CategoryClassifier:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=20000
        )

        self.model = LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )

        self.is_trained = False

    def train(self, texts, labels):

        X = self.vectorizer.fit_transform(texts)

        self.model.fit(X, labels)

        self.is_trained = True

    def predict(self, text):

        if not self.is_trained:
            raise RuntimeError(
                "Category classifier is not trained."
            )

        X = self.vectorizer.transform([text])

        prediction = self.model.predict(X)[0]

        probabilities = self.model.predict_proba(X)[0]

        confidence = float(probabilities.max())

        return {
            "category": prediction,
            "confidence": round(confidence, 4)
        }

    def save(self, model_dir="models"):

        category_dir = os.path.join(
            model_dir,
            "category"
        )

        os.makedirs(
            category_dir,
            exist_ok=True
        )

        joblib.dump(
            self.model,
            os.path.join(
                category_dir,
                "category_model.joblib"
            )
        )

        joblib.dump(
            self.vectorizer,
            os.path.join(
                category_dir,
                "category_vectorizer.joblib"
            )
        )

    def load(self, model_dir="models"):

        category_dir = os.path.join(
            model_dir,
            "category"
        )

        self.model = joblib.load(
            os.path.join(
                category_dir,
                "category_model.joblib"
            )
        )

        self.vectorizer = joblib.load(
            os.path.join(
                category_dir,
                "category_vectorizer.joblib"
            )
        )

        self.is_trained = True