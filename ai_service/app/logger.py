import json
import os
from datetime import datetime


LOG_FILE = "data/ai_decisions.jsonl"


def log_decision(request, response):

    os.makedirs(
        os.path.dirname(LOG_FILE),
        exist_ok=True
    )

    record = {
        "timestamp": datetime.utcnow().isoformat(),

        "input": {
            "title": request.get("title"),
            "description": request.get("description")
        },

        "decision": {
            "category": response.get("category"),
            "priority": response.get("priority"),
            "decision_source": response.get(
                "decision_source"
            )
        },

        "duplicate": response.get(
            "duplicate"
        ),

        "sla": response.get(
            "sla"
        )
    }

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(
                record,
                ensure_ascii=False
            ) + "\n"
        )