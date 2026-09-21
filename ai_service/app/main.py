from fastapi import FastAPI

from app.schemas import (
    TicketRequest,
    TicketAnalysisResponse
)

from app.rule_engine import RuleEngine
from app.duplicate_detector import DuplicateDetector
from app.category_classifier import CategoryClassifier
from app.sla_risk import SLARiskAnalyzer
from app.decision_engine import DecisionEngine
from app.model_registry import ModelRegistry
from app.logger import log_decision


app = FastAPI(
    title="Campus Helpdesk AI Service",
    version="1.0.0"
)


# ==========================================
# COMPONENTS
# ==========================================

rule_engine = RuleEngine()

duplicate_detector = DuplicateDetector(
    threshold=0.90
)

category_classifier = CategoryClassifier()

sla_analyzer = SLARiskAnalyzer()

model_registry = ModelRegistry()


# ==========================================
# LOAD MODELS
# ==========================================

try:

    category_classifier.load(
        "models"
    )

except Exception:

    category_classifier = None


# ==========================================
# LOAD HISTORICAL TICKETS
# ==========================================

historical_tickets = [
    {
        "id": "T001",
        "text": "wifi is not working in computer lab"
    },
    {
        "id": "T002",
        "text": "unable to login to university email"
    },
    {
        "id": "T003",
        "text": "printer is not working"
    }
]


duplicate_detector.fit(
    historical_tickets
)


# ==========================================
# DECISION ENGINE
# ==========================================

decision_engine = DecisionEngine(
    rule_engine=rule_engine,
    category_classifier=category_classifier,
    duplicate_detector=duplicate_detector,
    sla_analyzer=sla_analyzer
)


# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "ai-service"
    }


# ==========================================
# AI ANALYSIS
# ==========================================

@app.post(
    "/ai/analyze",
    response_model=TicketAnalysisResponse
)
def analyze(
    request: TicketRequest
):

    result = decision_engine.analyze(

    title=request.title,

    description=request.description,

    location=request.location,

    urgency=request.urgency
)
    log_decision(
        request.dict(),
        result
    )

    return result


# ==========================================
# MODEL VERSIONS
# ==========================================

@app.get("/ai/models")
def model_versions():

    return model_registry.get_versions()