"""
Stats router – endpoints for weak-topics breakdown and dashboard overview.
"""

from fastapi import APIRouter
from app.models.stats import (
    WeakTopicsResponse,
    TopicStatItem,
    DashboardSummaryResponse,
)
from app.services.stats import get_weak_topics_data, get_dashboard_summary_data
from app.config import settings

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/weak-topics", response_model=WeakTopicsResponse)
async def get_weak_topics():
    """
    Get the student's weakest topics, ranked by error rate.
    Used for dashboard charts and auto-generating practice quizzes.
    """
    data = await get_weak_topics_data(user_id=settings.default_user_id)
    items = [TopicStatItem(**d) for d in data]
    return WeakTopicsResponse(weak_topics=items, count=len(items))


@router.get("/summary", response_model=DashboardSummaryResponse)
async def get_summary():
    """
    Get high-level dashboard metrics:
    Total notes, total quizzes taken, average score %, total questions answered.
    """
    summary = await get_dashboard_summary_data(user_id=settings.default_user_id)
    return DashboardSummaryResponse(**summary)
