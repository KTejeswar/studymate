"""
Pydantic schemas for student statistics and weak topic analysis.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class TopicStatItem(BaseModel):
    topic: str
    subject: str = "General"
    total_attempts: int
    correct: int
    wrong: int
    error_rate: float = Field(..., description="Percentage of wrong answers (0-100)")
    accuracy: float = Field(..., description="Percentage of correct answers (0-100)")


class WeakTopicsResponse(BaseModel):
    weak_topics: list[TopicStatItem]
    count: int


class DashboardSummaryResponse(BaseModel):
    total_notes: int
    total_quizzes_taken: int
    average_score: float
    total_questions_answered: int
