"""
Pydantic schemas for the Chat feature.
"""

from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field


class CitationOut(BaseModel):
    filename: str
    page: int
    subject: str = "General"
    snippet: str = ""


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Student question")
    subject: str | None = Field(default=None, description="Optional subject filter")


class ChatResponse(BaseModel):
    answer: str
    citations: list[CitationOut] = []
    steps: list[str] = []
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
