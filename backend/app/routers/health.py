"""
Health-check router.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.database import get_db

router = APIRouter(tags=["health"])


@router.get("/api/health")
async def health_check():
    """Returns server status and a MongoDB ping."""
    db = get_db()
    try:
        await db.command("ping")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "ok",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
