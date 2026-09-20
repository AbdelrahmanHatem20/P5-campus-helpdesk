# app/rule_engine.py

from .rules import CATEGORY_RULES, PRIORITY_RULES


def normalize_text(text: str) -> str:
    """
    Convert text to lowercase and remove extra spaces.
    """

    return " ".join(text.lower().strip().split())


def detect_category(text: str):
    """
    Detect ticket category based on keyword matching.
    """

    category_scores = {}

    # Calculate score for every category
    for category, keywords in CATEGORY_RULES.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        category_scores[category] = score

    # Find category with highest score
    best_category = max(
        category_scores,
        key=category_scores.get
    )

    best_score = category_scores[best_category]

    # No category keyword was found
    if best_score == 0:

        return (
            "Other",
            0.30,
            []
        )

    # Get matched keywords
    matched_keywords = []

    for keyword in CATEGORY_RULES[best_category]:

        if keyword in text:
            matched_keywords.append(keyword)

    # Simple rule-based confidence
    confidence = min(
        0.50 + (best_score * 0.15),
        0.95
    )

    return (
        best_category,
        confidence,
        matched_keywords
    )


def detect_priority(text: str):
    """
    Detect ticket priority using a simple scoring system.
    """

    score = 0

    reasons = []

    # Critical keywords
    for keyword in PRIORITY_RULES["Critical"]:

        if keyword in text:

            score += 5

            reasons.append(
                f"Critical keyword detected: {keyword}"
            )

    # High priority keywords
    for keyword in PRIORITY_RULES["High"]:

        if keyword in text:

            score += 3

            reasons.append(
                f"High priority keyword detected: {keyword}"
            )

    # Medium priority keywords
    for keyword in PRIORITY_RULES["Medium"]:

        if keyword in text:

            score += 2

            reasons.append(
                f"Medium priority keyword detected: {keyword}"
            )

    # Low priority keywords
    for keyword in PRIORITY_RULES["Low"]:

        if keyword in text:

            score += 1

            reasons.append(
                f"Low priority keyword detected: {keyword}"
            )

    # Convert score to priority
    if score >= 9:

        priority = "Critical"

    elif score >= 6:

        priority = "High"

    elif score >= 3:

        priority = "Medium"

    else:

        priority = "Low"

    return priority, reasons


def calculate_sla_risk(priority: str) -> str:
    """
    Simple SLA risk rule based on priority.
    """

    if priority == "Critical":

        return "High"

    elif priority == "High":

        return "High"

    elif priority == "Medium":

        return "Medium"

    return "Low"


def analyze_ticket(
    title: str,
    description: str,
    location: str = None
):
    """
    Main Rule-Based AI function.

    It analyzes a ticket and returns:
    - Category
    - Priority
    - SLA risk
    - Confidence
    - Explanation
    """

    # Combine all ticket information
    text = f"{title} {description}"

    if location:
        text += f" {location}"

    # Normalize text
    text = normalize_text(text)

    # Detect category
    category, confidence, category_keywords = detect_category(
        text
    )

    # Detect priority
    priority, priority_reasons = detect_priority(
        text
    )

    # Detect SLA risk
    sla_risk = calculate_sla_risk(
        priority
    )

    # Build explanation
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

    explanation.extend(
        priority_reasons
    )

    # Final result
    return {
        "category": category,
        "priority": priority,
        "sla_risk": sla_risk,
        "confidence": round(confidence, 2),
        "explanation": explanation,
        "method": "rule-based"
    }