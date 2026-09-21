from datetime import datetime


URGENT_KEYWORDS = [
    "urgent",
    "critical",
    "down",
    "not working",
    "emergency",
    "immediately"
]


class SLARiskAnalyzer:

    def __init__(self):

        self.priority_weights = {
            "Low": 1,
            "Medium": 2,
            "High": 3,
            "Critical": 4
        }

    def calculate(
        self,
        text: str,
        priority: str,
        age_hours: float = 0
    ):

        text = text.lower()

        score = 0
        reasons = []

        # Priority
        priority_score = self.priority_weights.get(
            priority,
            1
        )

        score += priority_score

        if priority in ["High", "Critical"]:
            reasons.append(
                "High priority ticket"
            )

        # Urgent keywords
        keyword_matches = [
            keyword
            for keyword in URGENT_KEYWORDS
            if keyword in text
        ]

        if keyword_matches:
            score += 2

            reasons.append(
                f"Urgent keywords: {keyword_matches}"
            )

        # Age
        if age_hours >= 24:
            score += 3

            reasons.append(
                "Ticket age exceeds 24 hours"
            )

        elif age_hours >= 12:
            score += 2

            reasons.append(
                "Ticket age exceeds 12 hours"
            )

        # Risk level
        if score >= 7:
            risk = "High"

        elif score >= 4:
            risk = "Medium"

        else:
            risk = "Low"

        return {
            "risk": risk,
            "score": score,
            "reasons": reasons
        }