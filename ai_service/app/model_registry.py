from datetime import datetime


class ModelRegistry:

    def __init__(self):

        self.models = {
            "category_classifier": {
                "name": "TF-IDF + Logistic Regression",
                "version": "1.0.0"
            },

            "duplicate_detector": {
                "name": "TF-IDF + Cosine Similarity",
                "version": "1.0.0"
            },

            "sla_risk": {
                "name": "Rule-based SLA Risk",
                "version": "1.0.0"
            },

            "rule_engine": {
                "name": "Keyword Rule Engine",
                "version": "1.0.0"
            }
        }

    def get_versions(self):

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "models": self.models
        }