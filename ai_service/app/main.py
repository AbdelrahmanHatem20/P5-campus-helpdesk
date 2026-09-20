# app/main.py

from fastapi import FastAPI

from .schemas import (
    TicketRequest,
    TicketAnalysisResponse
)

from .rule_engine import analyze_ticket


app = FastAPI(
    title="Campus Helpdesk AI Service",
    description="Rule-Based AI service for Campus Helpdesk tickets",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Used by Docker / DevOps / Backend.
    """

    return {
        "status": "ok",
        "service": "ai-service"
    }


@app.post(
    "/ai/analyze",
    response_model=TicketAnalysisResponse
)
def analyze(request: TicketRequest):
    """
    Analyze a campus helpdesk ticket.
    """

    result = analyze_ticket(
        title=request.title,
        description=request.description,
        location=request.location
    )

    return result