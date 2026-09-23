# app/schemas.py

from typing import List, Optional

from pydantic import BaseModel, Field


class TicketRequest(BaseModel):
    """
    Data received from the Backend.
    """

    title: str = Field(
        ...,
        description="Ticket title"
    )

    description: str = Field(
        ...,
        description="Detailed ticket description"
    )

    location: Optional[str] = Field(
        None,
        description="Ticket location"
    )


class TicketAnalysisResponse(BaseModel):
    """
    AI analysis returned to the Backend.
    """

    category: str

    priority: str

    sla_risk: str

    confidence: float

    explanation: List[str]

    method: str