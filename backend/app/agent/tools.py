"""
Allow-listed tools with Pydantic argument validation for LangGraph.
"""

from typing import Any
from pydantic import BaseModel, Field

from app.services.retrieval import search_chunks
from app.services.stats import get_weak_topics_data


class SearchNotesInput(BaseModel):
    query: str = Field(..., description="The search query or concept to search for in notes.")
    subject: str | None = Field(default=None, description="Optional subject to filter by (e.g. 'Physics').")
    top_k: int = Field(default=4, ge=1, le=8, description="Number of chunks to return.")


class GetWeakTopicsInput(BaseModel):
    limit: int = Field(default=5, ge=1, le=10, description="Max number of weak topics to return.")


async def search_notes(args: SearchNotesInput, user_id: str = "demo") -> list[dict[str, Any]]:
    """
    Search student notes using vector semantic similarity.
    Returns matched chunks with text, filename, page, and similarity score.
    """
    return await search_chunks(
        query=args.query,
        subject=args.subject,
        user_id=user_id,
        top_k=args.top_k,
    )


async def get_weak_topics(args: GetWeakTopicsInput, user_id: str = "demo") -> list[dict[str, Any]]:
    """
    Retrieve the student's weakest topics sorted by error rate.
    """
    return await get_weak_topics_data(
        user_id=user_id,
        limit=args.limit,
    )
