"""
Pydantic schemas for the Quiz feature.
"""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class QuestionOption(BaseModel):
    id: str = Field(..., description="'A', 'B', 'C', or 'D'")
    text: str


class QuizQuestionOut(BaseModel):
    id: int
    question: str
    options: list[QuestionOption]
    topic: str
    citation: str | None = None


class QuizGenerateRequest(BaseModel):
    subject: str = Field(default="General", description="Subject to generate quiz for")
    topic: str | None = Field(default=None, description="Optional specific sub-topic")
    num_questions: int = Field(default=3, ge=1, le=10, description="Number of questions (1-10)")


class QuizOut(BaseModel):
    id: str
    subject: str
    topic: str | None
    num_questions: int
    questions: list[QuizQuestionOut]
    created_at: datetime


class AnswerSubmission(BaseModel):
    question_id: int
    selected_option: str = Field(..., description="'A', 'B', 'C', or 'D'")


class QuizSubmitRequest(BaseModel):
    answers: list[AnswerSubmission]


class QuestionResult(BaseModel):
    question_id: int
    question: str
    selected_option: str
    correct_option: str
    is_correct: bool
    explanation: str
    topic: str


class QuizSubmitResult(BaseModel):
    attempt_id: str
    quiz_id: str
    total_questions: int
    correct_count: int
    wrong_count: int
    score_percentage: float
    results: list[QuestionResult]
    submitted_at: datetime
