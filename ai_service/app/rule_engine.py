from .rules import (
    CATEGORY_RULES,
    EMERGENCY_KEYWORDS,
    PRIORITY_MATRIX
)


def normalize_text(text: str) -> str:
    return " ".join(
        text.lower().strip().split()
    )


def detect_category(text: str):
    category_scores = {}

    for category, keywords in CATEGORY_RULES.items():

        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 1

        category_scores[category] = score

    best_category = max(
        category_scores,
        key=category_scores.get
    )

    best_score = category_scores[best_category]

    if best_score == 0:
        return "Other", 0.30, []

    matched_keywords = []

    for keyword in CATEGORY_RULES[best_category]:

        if keyword in text:
            matched_keywords.append(keyword)

    confidence = min(
        0.50 + (best_score * 0.15),
        0.95
    )

    return (
        best_category,
        confidence,
        matched_keywords
    )


def detect_priority(
    text: str,
    urgency: str = "Medium",
    impact: str = "Medium"
):
    urgency = urgency.capitalize()
    impact = impact.capitalize()

    # Emergency always has highest priority
    for keyword in EMERGENCY_KEYWORDS:

        if keyword in text:

            return (
                "Critical",
                [f"Emergency keyword detected: {keyword}"]
            )

    # Safety defaults
    if urgency not in PRIORITY_MATRIX:
        urgency = "Medium"

    if impact not in PRIORITY_MATRIX:
        impact = "Medium"

    priority = PRIORITY_MATRIX[impact][urgency]

    reasons = [
        f"Priority determined by Impact={impact} × Urgency={urgency}"
    ]

    return priority, reasons


def calculate_sla_risk(priority: str) -> str:

    if priority == "Critical":
        return "High"

    if priority == "High":
        return "High"

    if priority == "Medium":
        return "Medium"

    return "Low"


def analyze_ticket(
    title: str,
    description: str,
    location: str = None,
    urgency: str = "Medium",
    impact: str = "Medium"
):
    text = f"{title} {description}"

    if location:
        text += f" {location}"

    text = normalize_text(text)

    category, confidence, category_keywords = detect_category(
        text
    )

    priority, priority_reasons = detect_priority(
        text=text,
        urgency=urgency,
        impact=impact
    )

    sla_risk = calculate_sla_risk(priority)

    explanation = []

    if category_keywords:

        explanation.append(
            "Category keywords detected: "
            + ", ".join(category_keywords)
        )

    else:

        explanation.append(
            "No category-specific keywords detected."
        )

    explanation.extend(priority_reasons)

    return {
        "category": category,
        "priority": priority,
        "sla_risk": sla_risk,
        "confidence": round(confidence, 2),
        "explanation": explanation,
        "method": "rule-based"
    }
class RuleEngine:

    def analyze(
        self,
        title,
        description,
        location=None,
        urgency="Medium",
        impact="Medium"
    ):
        return analyze_ticket(
            title=title,
            description=description,
            location=location,
            urgency=urgency,
            impact=impact
        )    