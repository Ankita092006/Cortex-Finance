from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="The query to ask the conversational AI assistant.")

class TransactionSchema(BaseModel):
    id: Optional[int] = None
    date: str
    narration: str
    debit: float
    credit: float
    balance: float
    category: str
    is_recurring: int
    is_anomaly: int
    filename: str

class DashboardResponse(BaseModel):
    income: float
    expense: float
    savings: float
    score: int
    categories: dict
    top_merchants: List[dict]
    recurring_payments: List[dict]
    anomalies: List[dict]

class InsightItem(BaseModel):
    type: str = Field(..., description="E.g., info, warning, success")
    message: str
    category: Optional[str] = None

class InsightsResponse(BaseModel):
    summary: str
    insights: List[InsightItem]
