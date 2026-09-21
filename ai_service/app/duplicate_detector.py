from typing import List, Dict, Optional
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DuplicateDetector:
    """
    Detects whether a new ticket is similar to previously seen tickets.
    Uses TF-IDF + Cosine Similarity.
    """

    def __init__(self, threshold: float = 0.90):
        self.threshold = threshold

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=10000
        )

        self.ticket_ids = []
        self.ticket_texts = []
        self.ticket_vectors = None

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""

        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def fit(self, tickets: List[Dict]):
        """
        Build TF-IDF index from historical tickets.

        Expected format:
        [
            {
                "id": "T001",
                "text": "wifi is not working"
            }
        ]
        """

        self.ticket_ids = []
        self.ticket_texts = []

        for ticket in tickets:
            ticket_id = str(ticket["id"])
            text = self._clean_text(ticket["text"])

            if text:
                self.ticket_ids.append(ticket_id)
                self.ticket_texts.append(text)

        if not self.ticket_texts:
            self.ticket_vectors = None
            return

        self.ticket_vectors = self.vectorizer.fit_transform(
            self.ticket_texts
        )

    def detect(self, text: str) -> Dict:
        """
        Compare a new ticket against historical tickets.
        """

        if self.ticket_vectors is None:
            return {
                "is_duplicate": False,
                "similarity": 0.0,
                "matched_ticket_id": None,
                "status": "no_index"
            }

        cleaned_text = self._clean_text(text)

        if not cleaned_text:
            return {
                "is_duplicate": False,
                "similarity": 0.0,
                "matched_ticket_id": None,
                "status": "empty_text"
            }

        query_vector = self.vectorizer.transform([cleaned_text])

        similarities = cosine_similarity(
            query_vector,
            self.ticket_vectors
        )[0]

        best_index = similarities.argmax()
        best_similarity = float(similarities[best_index])

        matched_ticket_id = self.ticket_ids[best_index]

        return {
            "is_duplicate": best_similarity >= self.threshold,
            "similarity": round(best_similarity, 4),
            "matched_ticket_id": matched_ticket_id,
            "threshold": self.threshold,
            "status": "ok"
        }