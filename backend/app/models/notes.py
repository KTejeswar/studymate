"""
Pydantic schemas for the Notes feature.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# ── Responses ───────────────────────────────────────────────

class NoteOut(BaseModel):
    """A note as returned by the API."""
    id: str = Field(..., description="MongoDB document ID")
    user_id: str
    filename: str
    file_type: Literal["pdf", "txt", "md"]
    subject: str
    page_count: int
    created_at: datetime


class NoteUploadOut(BaseModel):
    """Response after a successful upload."""
    message: str = "Note uploaded successfully"
    note: NoteOut


class NoteListOut(BaseModel):
    """Response for listing notes."""
    notes: list[NoteOut]
    count: int


class NoteDeleteOut(BaseModel):
    """Response after deletion."""
    message: str = "Note deleted successfully"
    id: str
