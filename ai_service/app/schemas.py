from typing import Optional, List, Dict, Any

from pydantic import BaseModel


class TicketRequest(BaseModel):

    title: str

    description: str

    location: Optional[str] = None

    urgency: Optional[str] = "Medium"


class DuplicateResponse(BaseModel):

    is_duplicate: bool

    similarity: float

    matched_ticket_id: Optional[str] = None


class TicketAnalysisResponse(BaseModel):

    category: str

    priority: str

    decision_source: str

    rule_result: Dict[str, Any]

    ml_result: Optional[Dict[str, Any]]

    duplicate: Optional[Dict[str, Any]]

    sla: Optional[Dict[str, Any]]

    explanation: List[str]