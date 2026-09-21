class DecisionEngine:

    def __init__(
        self,
        rule_engine,
        category_classifier=None,
        duplicate_detector=None,
        sla_analyzer=None
    ):

        self.rule_engine = rule_engine
        self.category_classifier = category_classifier
        self.duplicate_detector = duplicate_detector
        self.sla_analyzer = sla_analyzer

    def analyze(
        self,
        title,
        description,
        location=None,
        urgency="Medium"
    ):

        text = f"{title} {description}".strip()

        # --------------------------------
        # 1. RULE BASELINE
        # --------------------------------

        rule_result = self.rule_engine.analyze(
            title=title,
            description=description,
            location=location,
            urgency=urgency
        )

        final_category = rule_result.get(
            "category",
            "Other"
        )

        final_priority = rule_result.get(
            "priority",
            "Medium"
        )

        explanation = rule_result.get(
            "explanation",
            []
        )

        # --------------------------------
        # 2. ML CATEGORY
        # --------------------------------

        ml_result = None

        if self.category_classifier:

            try:

                ml_result = self.category_classifier.predict(
                    text
                )

            except Exception:

                ml_result = None

        # --------------------------------
        # 3. DUPLICATE
        # --------------------------------

        duplicate_result = None

        if self.duplicate_detector:

            try:

                duplicate_result = (
                    self.duplicate_detector.detect(text)
                )

            except Exception:

                duplicate_result = None

        # --------------------------------
        # 4. SLA
        # --------------------------------

        sla_result = None

        if self.sla_analyzer:

            try:

                sla_result = self.sla_analyzer.calculate(
                    text=text,
                    priority=final_priority,
                    age_hours=0
                )

            except Exception:

                sla_result = None

        # --------------------------------
        # 5. FINAL DECISION
        # --------------------------------

        decision_source = "rule"

        # ML overrides rule only when confidence >= 0.80
        if ml_result:

            ml_confidence = ml_result.get(
                "confidence",
                0
            )

            if ml_confidence >= 0.80:

                final_category = ml_result["category"]

                decision_source = "ml"

        # --------------------------------
        # FINAL RESPONSE
        # --------------------------------

        return {
            "category": final_category,
            "priority": final_priority,
            "decision_source": decision_source,
            "rule_result": rule_result,
            "ml_result": ml_result,
            "duplicate": duplicate_result,
            "sla": sla_result,
            "explanation": explanation
        }