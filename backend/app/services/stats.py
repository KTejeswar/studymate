"""
Stats and weak-topic analytics service.
"""

from typing import Any
from app.config import settings
from app.database import get_db


async def get_weak_topics_data(
    user_id: str | None = None,
    limit: int = 5,
    min_attempts: int = 1,
) -> list[dict[str, Any]]:
    """
    Returns topics with the highest error rates.
    """
    user_id = user_id or settings.default_user_id
    db = get_db()

    cursor = db.topic_stats.find({
        "user_id": user_id,
        "total_attempts": {"$gte": min_attempts},
    })
    raw_stats = await cursor.to_list(length=100)

    calculated: list[dict[str, Any]] = []
    for s in raw_stats:
        total = s.get("total_attempts", 0)
        wrong = s.get("wrong", 0)
        correct = s.get("correct", 0)

        error_rate = round((wrong / total) * 100, 1) if total > 0 else 0.0
        accuracy = round((correct / total) * 100, 1) if total > 0 else 0.0

        calculated.append({
            "topic": s.get("topic", "General"),
            "subject": s.get("subject", "General"),
            "total_attempts": total,
            "correct": correct,
            "wrong": wrong,
            "error_rate": error_rate,
            "accuracy": accuracy,
        })

    # Sort descending by error rate (weakest topics first), then by total wrong
    calculated.sort(key=lambda x: (x["error_rate"], x["wrong"]), reverse=True)
    return calculated[:limit]


async def get_dashboard_summary_data(user_id: str | None = None) -> dict[str, Any]:
    """
    Aggregates high-level metrics for the dashboard:
    Total notes, total quizzes taken, average score %, total questions answered.
    """
    user_id = user_id or settings.default_user_id
    db = get_db()

    total_notes = await db.notes.count_documents({"user_id": user_id})

    # Aggregate from attempts
    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": None,
                "total_quizzes": {"$sum": 1},
                "total_questions": {"$sum": "$total_questions"},
                "avg_score": {"$avg": "$score_percentage"},
            }
        },
    ]

    agg = await db.attempts.aggregate(pipeline).to_list(length=1)

    if agg:
        total_quizzes = agg[0].get("total_quizzes", 0)
        total_questions = agg[0].get("total_questions", 0)
        avg_score = round(float(agg[0].get("avg_score", 0.0)), 1)
    else:
        total_quizzes = 0
        total_questions = 0
        avg_score = 0.0

    return {
        "total_notes": total_notes,
        "total_quizzes_taken": total_quizzes,
        "average_score": avg_score,
        "total_questions_answered": total_questions,
    }
